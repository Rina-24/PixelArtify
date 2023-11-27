import cv2
import numpy as np
 # mosaic 関数では、まず画像を縮小し、その後に cv2.INTER_NEAREST を用いて最近傍補間法で再拡大。
 # これにより、モザイク処理が行われる。alpha パラメータは縮小率を制御する。
def mosaic(img, alpha):
    """ img.shape: これはNumPy配列の形状を示す属性。
    通常、画像データは高さ x 幅 x チャンネル数（もしカラー画像ならばRGBやBGRAの3または4）の形状を持つ。
    h, w, ch = img.shape: これは複数の変数に同時に代入を行う構文で、img.shape の返り値を高さ h、幅 w、およびチャンネル数 ch にそれぞれ代入。
    したがって、この行の結果として、変数 h には画像の高さ、w には画像の幅、ch には画像のチャンネル数が代入"""
    h, w, ch = img.shape
    
    # 画像を縮小
    img = cv2.resize(img, (int(w * alpha), int(h * alpha)))

     # 縮小した画像を再拡大（モザイク処理）
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)
    return img


# decreaseColor関数:画像の各ピクセルの色を特定の範囲ごとに変更して減色処理を行う。各色の範囲は32ごとに設定されている。
# 例えば、0から32の範囲の色は16に、32から64の範囲の色は48に変更されます。
# def decreaseColor(img):
#     # dst:Destination（宛先）の略。処理の結果を格納
#     dst = img.copy()

#     # 各色の範囲ごとに値を変更
#     for i in range(1, 8):
#         idx = np.where((32 * i <= img) & (32 * (i + 1) > img))
#         dst[idx] = 32 * i + 16
    
#     # 以下の計算と同意
#         # idx = np.where((0<=img) & (32>img))
#         # dst[idx] = 16
#         # idx = np.where((32<=img) & (64>img))
#         # dst[idx] = 48
#         # idx = np.where((64<=img) & (96>img))
#         # dst[idx] = 80
#         # idx = np.where((96<=img) & (128>img))
#         # dst[idx] = 112
#         # idx = np.where((128<=img) & (160>img))
#         # dst[idx] = 144
#         # idx = np.where((160<=img) & (192>img))
#         # dst[idx] = 176
#         # idx = np.where((192<=img) & (224>img))
#         # dst[idx] = 208
#         # idx = np.where((224<=img) & (256>=img))
#         # dst[idx] = 

def decreaseColor(img):
    dst = img.copy()
    for i in range(1, 8):
        idx = np.where((32 * i <= img) & (32 * (i + 1) > img))
        dst[idx] = 32 * i + 16
    return dst
