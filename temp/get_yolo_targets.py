# -- coding: utf-8 --
import os
import shutil
from pathlib import Path
import numpy as np
import cv2
from tqdm import tqdm
import sys
from common import *

 
# 坐标转换
def xywh2xyxy(x, w1, h1, img):
    label, x, y, w, h = x
 
    label = int(label)
    label_ind = label
 
    # 边界框反归一化
    x_t = x * w1
    y_t = y * h1
    w_t = w * w1
    h_t = h * h1
 
    # 计算坐标
    top_left_x = x_t - w_t / 2
    top_left_y = y_t - h_t / 2
    bottom_right_x = x_t + w_t / 2
    bottom_right_y = y_t + h_t / 2
 
    p1, p2 = (int(top_left_x), int(top_left_y)), (int(bottom_right_x), int(bottom_right_y))
    # 绘制矩形框
    cv2.rectangle(img, p1, p2, colormap[label_ind+1], thickness=2, lineType=cv2.LINE_AA)
    label = labels[label_ind]

    if label:
        w, h = cv2.getTextSize(label, 0, fontScale=2 / 3, thickness=2)[0]  # text width, height
        outside = p1[1] - h - 3 >= 0  # label fits outside box
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        # 绘制矩形框填充
        cv2.rectangle(img, p1, p2, colormap[label_ind+1], -1, cv2.LINE_AA)
        # 绘制标签
        cv2.putText(img, label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, 2 / 3, colormap[0],
                    thickness=2, lineType=cv2.LINE_AA)
    return img
 
 
if __name__ == '__main__':
    # 修改输入图片文件夹
    img_folder = "E:\\dataset\\浙江瞻芯\\KLA测试数据\\pattern-missing\\细分类别\\MISS3_4\\MISS34\\miss34"
    img_list = os.listdir(img_folder)
    img_list.sort()
    # 修改输入标签文件夹
    label_folder = "E:\\dataset\\浙江瞻芯\\KLA测试数据\\pattern-missing\\细分类别\\MISS3_4\\MISS34\\YOLO_txt"
    label_list = os.listdir(label_folder)
    label_list.sort()
    # 输出图片文件夹位置
    output_folder = './output'
    
    labels = ['MISS_3', 'MISS_4', 'DARKPOINT', 'SCRATCH', 'TRIANGLE', 'PARTICLE2', 'AREADEFECT', 'PR', 'POLYGRAIN', 'PARTICLE1']
    MISS_label =  ['MISS_3', 'MISS_4']  # label index to select from labels

    colormap = [(255, 255, 255), (56, 56, 255), (151, 157, 255)]
    # 创建输出文件夹
    if Path(output_folder).exists():
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    imgNames = os.listdir(img_folder)
    for imgName in imgNames:
        imgPath = os.path.join(img_folder,imgName)
        img = cv2_imread(imgPath)
        # plt_show("img",img)
        img_h, img_w = img.shape[:2]
        labelpath = os.path.join(label_folder,os.path.splitext(imgName)[0]+".txt")
        with open(labelpath, 'r') as f:
            lbs = np.array([x.split() for x in f.read().strip().splitlines()], dtype=np.float32)
            for lb in lbs:
                label_index, x, y, w, h = lb
                labelname = labels[int(label_index)]
                if labelname not in MISS_label: continue
                # 边界框反归一化
                x_t = x * img_w
                y_t = y * img_h
                w_t = w * img_w
                h_t = h * img_h
                # 计算坐标
                top_left_x = int(x_t - w_t / 2)
                top_left_y = int(y_t - h_t / 2)
                bottom_right_x = int(x_t + w_t / 2)
                bottom_right_y = int(y_t + h_t / 2)

                min_y, max_y = 75,550
                if top_left_y< min_y:
                    top_left_y = min_y

                if bottom_right_y > max_y:
                    bottom_right_y = max_y
                
                if bottom_right_y<=top_left_y:continue  # avoid y2<=y1


                p1, p2 = (top_left_x, top_left_y), (bottom_right_x, bottom_right_y)



                target = img[p1[1]:p2[1],p1[0]:p2[0]]
                plt_show("target",target)


                graytarget = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
                # plt_show("GRAY",graytarget)

                blurred = cv2.GaussianBlur(graytarget, (7, 7), 0)
                blurred = cv2.GaussianBlur(blurred, (7, 7), 0)
                blurred = cv2.GaussianBlur(blurred, (7, 7), 0)

                plt_show("blurred",blurred)

                equalized_image = cv2.equalizeHist(blurred)
                plt_show("equalized_image",equalized_image)


                histogram = cv2.calcHist([equalized_image], [0], None, [256], [0, 256])

                # 绘制直方图
                plt.figure()
                plt.title('Grayscale Histogram')
                plt.xlabel('Pixel Intensity')
                plt.ylabel('Frequency')
                plt.plot(histogram, color='gray')
                plt.xlim([0, 256])
                plt.show()

                _, binary_image = cv2.threshold(equalized_image, 80, 255, cv2.THRESH_BINARY)
                # # binary_image = cv2.threshold(equalized_image, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                # #_, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
                # binary_image=cv2.adaptiveThreshold(src=equalized_image,maxValue=127,adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                #                   thresholdType=cv2.THRESH_BINARY,blockSize=21,C=0)
                plt_show('binary_image',binary_image)
                #
                # dilated_image = cv2.dilate(binary_image, kernel = np.ones((5,5),np.uint8), iterations=1)
                # closed_image = cv2.morphologyEx(dilated_image, cv2.MORPH_CLOSE, np.ones((5,5)))
                # closed_image = cv2.morphologyEx(closed_image, cv2.MORPH_CLOSE, np.ones((5,5)))
                # plt_show('closed_image',closed_image)
                #
                #
                contours, hierarchy = cv2.findContours(equalized_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                #
                cv2.drawContours(target,contours,-1,(0,0,255),3)
                #
                plt_show("target", target)
                # # thresh_Contours = binary_image.copy()
                # # # 找到每一个圆圈轮廓
                # # cnts = cv2.findContours(binary_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
                # # cv2.drawContours(thresh_Contours,cnts,-1,(0,0,255),3)
                # # plt_show('thresh_Contours',thresh_Contours)
                # # questionCnts = []


