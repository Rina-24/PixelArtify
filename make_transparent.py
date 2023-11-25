
# from flask import Flask, render_template, request
# import cv2
# import numpy as np

# app = Flask(__name__)

# def make_transparent(img, target_color):
#     # BGR形式でのターゲット色
#     target_color_bgr = np.array(target_color[::-1])

#     # # ターゲット色以外のピクセルを抽出
#     # mask = np.all(img[:, :, :3] == target_color_bgr, axis=-1)

#     # # ターゲット色と一致する場合はそのまま返す
#     # if np.all(target_color_bgr == np.array([255, 255, 255])):
#     #     return img

#     # Point 1: 白色部分に対応するマスク画像を生成
#     mask = np.all(img[:,:,:] == [255, 255, 255], axis=-1)
#     # Point 2: 元画像をBGR形式からBGRA形式に変換
#     al = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

#     # Point3: マスク画像をもとに、白色部分を透明化
#     dst[mask,3] = 0

#     # 透過チャンネルを作成
#     alpha_channel = np.ones_like(mask, dtype=np.uint8) * 255
#     alpha_channel[mask] = 0

#     print("mask shape:", mask.shape)
#     print("alpha_channel shape:", alpha_channel.shape)

#     # アルファチャンネルを追加
#     img_with_alpha = np.dstack([img, alpha_channel])

#     print("img_with_alpha shape:", img_with_alpha.shape)

#     return img_with_alpha

# @app.route('/upload', methods=['POST'])
# def upload():
#     # フォームから送信されたファイルを取得
#     uploaded_file = request.files['file']

#     # ユーザーが指定したピクセルサイズを取得
#     pixel_size = int(request.form['pixel_size'])

#     # ユーザーが選択したファイルフォーマットを取得
#     file_format = request.form['file_format']

#     # 画像を透過させる処理（PNGの場合のみ）
#     if file_format == 'png':
#         img = cv2.imread(uploaded_file.filename, cv2.IMREAD_UNCHANGED)

#         # 透過させる処理（make_transparent関数を利用）
#         img_with_alpha = make_transparent(img, [255, 255, 255])

#         # 画像保存
#         cv2.imwrite("output.png", img_with_alpha)

#     # その他の処理（JPGの場合など）

#     return render_template('result.html', result_message='変換が完了しました。')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
import cv2
import numpy as np

app = Flask(__name__)

def make_transparent(img, target_color):
    # BGR形式でのターゲット色
    target_color_bgr = np.array(target_color[::-1])

    # 白色部分に対応するマスク画像を生成
    mask = np.all(img[:, :, :3] == [255, 255, 255], axis=-1)

    # 元画像をBGR形式からBGRA形式に変換
    img_with_alpha = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # マスク画像をもとに、白色部分を透明化
    img_with_alpha[mask, 3] = 0

    return img_with_alpha

@app.route('/upload', methods=['POST'])
def upload():
    # フォームから送信されたファイルを取得
    uploaded_file = request.files['file']

    # ユーザーが指定したピクセルサイズを取得
    pixel_size = int(request.form['pixel_size'])

    # ユーザーが選択したファイルフォーマットを取得
    file_format = request.form['file_format']

    # 画像を透過させる処理（PNGの場合のみ）
    if file_format == 'png':
        img = cv2.imread(uploaded_file.filename, cv2.IMREAD_UNCHANGED)

        # 透過させる処理（make_transparent関数を利用）
        img_with_alpha = make_transparent(img, [255, 255, 255])

        # 画像保存
        cv2.imwrite("output.png", img_with_alpha)

    # その他の処理（JPGの場合など）

    return render_template('result.html', result_message='変換が完了しました。')

if __name__ == '__main__':
    app.run(debug=True)
