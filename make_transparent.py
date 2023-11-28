from flask import Flask, render_template, request
import cv2
import numpy as np

app = Flask(__name__)

# # 他の関数やファイルから make_transparent を呼び出せるようにする
def make_transparent(img):
    original_img = img.copy()

    # グレースケールに変換
    gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    # 2値化
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # 輪郭抽出
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # アルファチャンネルを持っていない場合は作成する
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # マスクを作成してアルファチャンネルに適用
    # zeros_like は、元画像と同じサイズで全ての要素が0の行列（画像）を生成
    mask = np.zeros_like(img)

    # 輪郭を描画し内部を白くする
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # マスクを調整(各pixelのドットを反転。これで輪郭の内側を黒く、外を白くする。)
    mask = cv2.bitwise_not(mask)

   # 白い部分を透明にする（色の範囲指定）
    """ここに指定した色が透過するので白をつかったイラストの場合は注意。240以下の白であればOK.カラーコードで透過したい色を指定すればいい"""
    lower_white = np.array([240, 240, 240, 0], dtype=np.uint8)
    upper_white = np.array([255, 255, 255, 255], dtype=np.uint8)

    # マスクを使って条件を適用
    white_pixels = np.all((img >= lower_white) & (img <= upper_white), axis=-1)
    img[white_pixels] = [0, 0, 0, 0]

    return img
