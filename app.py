from flask import Flask, render_template, request, send_from_directory
import cv2
import os
import numpy as np
from make_transparent import make_transparent
from img_change import mosaic, decreaseColor

# Flaskアプリを作成し、アップロードされたファイルの保存先ディレクトリを設定。
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/') は / ルートに対するリクエストを処理するためのデコレータ。
# デコレータは、関数やメソッドの前に付けることで、その関数やメソッドの振る舞いを変更する。
# ルート（root)はWebアプリケーションのエントリーポイントや最上位のURLパスを指す。通常、スラッシュ (/) で表す
# つまり、このFlaskアプリを作動したら最初に動く。
@app.route('/')
# render_template('upload.html') を呼び出して、upload.html テンプレートをレンダリング
def index():
    return render_template('upload.html')

# @app.route('/upload', methods=['POST']) によって定義されており、HTTPメソッドがPOSTであるリクエストに対応
@app.route('/upload', methods=['POST'])
def upload():
    # フォームからのファイルがない場合のエラー処理
    if 'file' not in request.files:
        return "No file part"
    # ファイルが選択されていない場合のエラー処理
    file = request.files['file']
    # ファイルが選択されているか確認。（選択されたファイルが空ではないことを確認）
    if file.filename == '':
        return "No selected file"

    if file:
        # ファイルの保存(ユーザーがアップロードしたファイルがサーバー上の特定のディレクトリに保存)
        """ app.config['UPLOAD_FOLDER'] は、Flaskアプリケーションの設定からアップロード先のディレクトリを指定している。
            このディレクトリは、アプリケーションがアップロードされたファイルを保存する場所
            os.path.join() を使用して、指定されたディレクトリとファイル名を結合して完全なファイルパスを作成しています。
            ここでは、'uploaded_image.' + request.form['file_format'] で、アップロードされたファイルに追加される名前の一部を構築"""
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.' + request.form['file_format'])
        
        """アップロードされたファイルを作成した完全なファイルパスに保存しています。
            これにより、サーバー上の指定されたディレクトリにアップロードされたファイルが保存"""
        file.save(filename)

        # 画像の読み込みと処理
        """ cv2.imread() は、指定されたファイルから画像を読み込み
            img は、OpenCVのNumPy配列として画像が格納"""
        img = cv2.imread(filename)

        """request.form['pixel_size'] は、アップロードされたフォームデータからピクセルサイズに関する値を取得。
            この値はフォームから送信されたもので、ユーザーが指定したピクセルサイズを表します。
            int() を使って文字列から整数に変換。
            alpha は、後続の処理で使用される透明度の値"""
        pixel_size = int(request.form['pixel_size'])
        alpha = pixel_size / 100.0

        # jpgかpngに応じて処理の分岐
        if request.form['file_format'] == 'jpg':
            # モザイク処理と減色処理
            mosaic_img = mosaic(img, alpha)
            dc_img = decreaseColor(mosaic_img)

        elif request.form['file_format'] == 'png':
            # 透過処理も追加（未完成）
            img_with_alpha = make_transparent(img, (255, 255, 255))
            mosaic_img = mosaic(img_with_alpha, alpha)
            dc_img = decreaseColor(mosaic_img)

        # 処理結果の保存
        result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result_image.' + request.form['file_format'])
        
        """cv2.imwrite() は、指定されたファイルパスに画像を保存します。
            ここでは、処理された画像 dc_img を result_filename で指定されたファイルパスに保存"""
        cv2.imwrite(result_filename, dc_img)

        # 処理結果のファイルをクライアントに送信。send_from_directory 関数は、指定されたディレクトリから指定されたファイルを返すために使用
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'result_image.' + request.form['file_format'])

"""Pythonスクリプトが直接実行された場合に、Flaskアプリを起動するためのもの
    app.run(debug=True) は、Flaskアプリケーションをデバッグモードで実行するためのメソッド
    このコードの目的は、スクリプトが直接実行されるときに、Flaskアプリケーションを起動すること。
    通常、開発段階では debug=True を使用して簡単にデバッグできるようにし、本番環境では debug=False や app.run() を省略して運用が推奨"""
if __name__ == '__main__':
    app.run(debug=True)
