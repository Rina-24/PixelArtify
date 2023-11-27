from flask import Flask, render_template, request
import cv2
import numpy as np

app = Flask(__name__)

# 他の関数やファイルから make_transparent を呼び出せるようにする
def make_transparent(img):
    # アルファチャンネルを持っていない場合は作成する
    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # 白い部分を検知してマスクを作成(whitesmoke[245,245,245])
    white_mask = np.all(img[:, :, :3] >= [245, 245, 245], axis=-1)
    
    # 白い部分を無色透明にする
    img[white_mask] = [0, 0, 0, 0]
    return img
