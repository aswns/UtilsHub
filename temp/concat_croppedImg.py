import sys; sys.path.append(".")
import os
import cv2
import numpy as np
import shutil
from _utils import *

def concatSingleImg(croppedImgs, ori_w=25000, ori_h=16384):
    """concat cropped images of one single ori Img
    Args:
        croppedImgs (List): [(part_img, x_pixel, y_pixel)]
    """
    
    oriImg = np.zeros((ori_w, ori_h,3), dtype=np.uint8)

    for partImg_infor in croppedImgs:
         part_img, realStartX, realStartY = partImg_infor
         realPartWidth, realPartHeight = part_img.shape[:2]
         oriImg[realStartX:realStartX + realPartWidth, realStartY:realStartY + realPartHeight] = part_img
    return oriImg


if __name__ == "__main__":
    

    imgDir = r"E:\dataset\屏显\屏显外观IC基板检测验证\0308莱宝缺陷图\1053问题反馈\屏显基板检测测试-偏暗_检测结果图"
    saveDir = imgDir+"_concat"
    
    if os.path.exists(saveDir):
        shutil.rmtree(saveDir)
    os.makedirs(saveDir)
    
    imgNames = os.listdir(imgDir)
    oriImgDict = {}  # {oriImageName:[img, x, y]}
    for imgName in imgNames:
        img = cv2_imread(os.path.join(imgDir, imgName))
        img = cv2.resize(img,(1024, 1024))
        x, y_ = imgName.split("_")[-2:]
        y, _ = y_.split(".")
        oriImgName = imgName.replace("_".join(["",x, y_]),".png")
        if oriImgName not in oriImgDict.keys():
            oriImgDict[oriImgName] = [[img, int(x), int(y)]]
        else: oriImgDict[oriImgName].append([img, int(x), int(y)])

    for oriImgName in oriImgDict.keys():
        oriImg = concatSingleImg(oriImgDict[oriImgName])
        cv2_imwrite(os.path.join(saveDir,oriImgName), oriImg)
        print(f"concating&saving {oriImgName}")