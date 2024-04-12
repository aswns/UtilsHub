# coding:utf-8
"""
crop an image by sliding windows
"""


import cv2
import os
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = None

def Img_crop01(imgPath, partWidth, partHeight, savePath):
    img = np.array(Image.open(imgPath))
    imgName = os.path.split(imgPath)[1]
    imgNameSplitSet = imgName.split(".")
    # name,end = imgName.split
    name = ".".join(imgNameSplitSet[:-1])
    # print(name)
    # end = imgNameSplitSet[-1]
    end = "jpg"


    width = img.shape[0]
    height = img.shape[1]


    if width % partWidth > 0:
        widthNum = width // partWidth + 1
    else:
        widthNum = width // partWidth

    if height % partHeight > 0:
        heightNum = height // partHeight + 1
    else:
        heightNum = height // partHeight


    for i in range(heightNum):
        for j in range(widthNum):
            startX = partWidth * j
            startY = partHeight * i

            if startX + partWidth <= width and startY + partHeight <= height:  # cropped image在原图内部
                realStartX = startX
                realStartY = startY

                realPartWidth = partWidth
                realPartHeight = partHeight
            elif startX + partWidth > width and startY + partHeight <= height:  # width超出，则realStartX = width - partWidth
                # realPartWidth = width - startX
                realStartX = width - partWidth
                realStartY = startY

                realPartWidth = partWidth
                realPartHeight = partHeight
            elif startX + partWidth <= width and startY + partHeight > height:

                realStartX = startX
                realStartY = height - partHeight

                realPartWidth = partWidth
                realPartHeight = partHeight
                # realPartHeight = height - startY
            elif startX + partWidth > width and startY + partHeight > height:
                # realPartWidth = width - startX
                # realPartHeight = height - startY

                realStartX = width - partWidth
                realStartY = height - partHeight

                realPartWidth = partWidth
                realPartHeight = partHeight


            partImg = img[realStartX:realStartX + realPartWidth, realStartY:realStartY + realPartHeight]
            partImage = Image.fromarray(partImg)
            partImage.save(os.path.join(savePath, "%s_%d_%d.%s" % (name, realStartX, realStartY, end)))


def clipImg(dataset_name, imgPath, unitSize, savePath):
    img = np.array(Image.open(imgPath))
    imgName = os.path.split(imgPath)[1]
    imgNameSplitSet = imgName.split(".")
    # name,end = imgName.split
    name = ".".join(imgNameSplitSet[:-1])
    # print(name)
    # end = imgNameSplitSet[-1]
    end = "jpg"


    width = img.shape[0]
    height = img.shape[1]

    partWidth = partHeight = unitSize

    if width % partWidth > 0:
        widthNum = width // partWidth + 1
    else:
        widthNum = width // partWidth

    if height % partHeight > 0:
        heightNum = height // partHeight + 1
    else:
        heightNum = height // partHeight


    for i in range(heightNum):
        for j in range(widthNum):
            startX = partWidth * j
            startY = partHeight * i

            if startX + partWidth <= width and startY + partHeight <= height:  # cropped image在原图内部
                realStartX = startX
                realStartY = startY

                realPartWidth = partWidth
                realPartHeight = partHeight
            elif startX + partWidth > width and startY + partHeight <= height:  # width超出，则realStartX = width - partWidth
                # realPartWidth = width - startX
                realStartX = width - partWidth
                realStartY = startY

                realPartWidth = partWidth
                realPartHeight = partHeight
            elif startX + partWidth <= width and startY + partHeight > height:

                realStartX = startX
                realStartY = height - partHeight

                realPartWidth = partWidth
                realPartHeight = partHeight
                # realPartHeight = height - startY
            elif startX + partWidth > width and startY + partHeight > height:
                # realPartWidth = width - startX
                # realPartHeight = height - startY

                realStartX = width - partWidth
                realStartY = height - partHeight

                realPartWidth = partWidth
                realPartHeight = partHeight
            path_position = os.path.join(savePath,f"{dataset_name}_{realStartX}_{realStartY}")
            if not os.path.exists(path_position):
                os.mkdir(path_position)

            partImg = img[realStartX:realStartX + realPartWidth, realStartY:realStartY + realPartHeight]
            partImgDir = os.path.join(path_position, "test", "good")
            if not os.path.exists(partImgDir): os.makedirs(partImgDir)
            partImage = Image.fromarray(partImg)
            partImage.save(os.path.join(partImgDir, "%s_%d_%d.%s" % (name, realStartX, realStartY, end)))

def clipImg_withMask(dataset_name, imgPath, maskDir, unitSize, savePath):
    img = np.array(Image.open(imgPath))
    imgName = os.path.split(imgPath)[1]
    imgNameSplitSet = imgName.split(".")
    # name,end = imgName.split
    name = ".".join(imgNameSplitSet[:-1])
    # print(name)
    # end = imgNameSplitSet[-1]
    end = "png"

    mask = np.array(Image.open(os.path.join(maskDir,f"{name}_mask.png")))

    width = img.shape[0]
    height = img.shape[1]

    partWidth = partHeight = unitSize

    if width % partWidth > 0:
        widthNum = width // partWidth + 1
    else:
        widthNum = width // partWidth

    if height % partHeight > 0:
        heightNum = height // partHeight + 1
    else:
        heightNum = height // partHeight


    for i in range(heightNum):
        for j in range(widthNum):
            startX = partWidth * j
            startY = partHeight * i

            if startX + partWidth <= width and startY + partHeight <= height:  # cropped image在原图内部
                realStartX = startX
                realStartY = startY

                realPartWidth = partWidth
                realPartHeight = partHeight
            elif startX + partWidth > width and startY + partHeight <= height:  # width超出，则realStartX = width - partWidth
                # realPartWidth = width - startX
                realStartX = width - partWidth
                realStartY = startY

                realPartWidth = partWidth
                realPartHeight = partHeight
            elif startX + partWidth <= width and startY + partHeight > height:

                realStartX = startX
                realStartY = height - partHeight

                realPartWidth = partWidth
                realPartHeight = partHeight
                # realPartHeight = height - startY
            elif startX + partWidth > width and startY + partHeight > height:
                # realPartWidth = width - startX
                # realPartHeight = height - startY

                realStartX = width - partWidth
                realStartY = height - partHeight

                realPartWidth = partWidth
                realPartHeight = partHeight
            path_position = os.path.join(savePath,f"{dataset_name}_{realStartX}_{realStartY}")
            if not os.path.exists(path_position):
                os.mkdir(path_position)

            partImg = img[realStartX:realStartX + realPartWidth, realStartY:realStartY + realPartHeight]
            partMask = mask[realStartX:realStartX + realPartWidth, realStartY:realStartY + realPartHeight]
            # cv2.imshow("a",partImg)
            # cv2.waitKey(0)
            if (partMask == 255).any(): # 存在mask
                partImgDir = os.path.join(path_position, "test", "bad")
                partMaskDir = os.path.join(path_position, "ground_truth", "bad")
                if not os.path.exists(partImgDir): os.makedirs(partImgDir)
                if not os.path.exists(partMaskDir): os.makedirs(partMaskDir)
                partImage = Image.fromarray(partImg)
                partImage.save(os.path.join(partImgDir, "%s_%d_%d.%s" % (name, realStartX, realStartY, end)))
                partMask = Image.fromarray(partMask)
                partMask.save(os.path.join(partMaskDir, "%s_%d_%d_mask.%s" % (name, realStartX, realStartY, end)))
            else:
                partImgDir = os.path.join(path_position, "test", "good")
                if not os.path.exists(partImgDir): os.makedirs(partImgDir)
                partImage = Image.fromarray(partImg)
                partImage.save(os.path.join(partImgDir, "%s_%d_%d.%s" % (name, realStartX, realStartY, end)))

def sliding_crop():

    dataset_name = "taike"
    fromDir = r"E:\dataset\屏显\屏显外观IC基板检测验证\0308莱宝缺陷图\第一款产品\NG_0201row7col8\photo"  # img dir path
    fromPath = r"E:\dataset\屏显\屏显外观IC基板检测验证\0308莱宝缺陷图\1053问题反馈\NG_ATPMFHMLVOCLUrow1col1\NG_ATPMFHMLVOCLUrow1col1\photo2\Main.IMAGE_ID_Line1.jpg"
    maskDir = r"E:\dataset\屏显\屏显外观IC基板检测验证\第一款产品\NG_0201row8col3\croppedImg"  # mask path
    partWidth, partHeight = 1024,1024
    saveDir = os.path.dirname(fromPath)+"_cropped"
    crop_withMask = False  # if crop with mask

    if not os.path.exists(saveDir): os.makedirs(saveDir)
    # for root, _, files in os.walk(fromDir):
    #     for file in files:
    #         if file.endswith(("jpg", "bmp", "png", "jpeg")):
    #             imgPath = os.path.join(root, file)
    #     #         if crop_withMask:
    #     #             clipImg_withMask(dataset_name,imgPath, maskDir,clipSize, saveDir)
    #     #         else:clipImg(dataset_name,imgPath,clipSize, saveDir)
    #     #         print(f"cropping {file}")

        
    #             Img_crop01(imgPath,clipSize, saveDir)
    #             print(f"cropping {file}")
    Img_crop01(fromPath, partWidth, partHeight, saveDir)


if __name__ == "__main__":
    sliding_crop()



