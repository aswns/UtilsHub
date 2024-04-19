# 20230807 将labelme打标得到的json文件转换为mask (label：彩色、黑白)
# 输出：bin_mask 为mvTec格式中ground truth文件夹下的黑白mask； O_image 放入test文件夹下异常图像文件夹与mask图像相对应

import os
import json
import base64
import imgviz
import PIL.Image
import os.path as osp
import numpy as np
from tqdm import tqdm
from labelme import utils
from threading import Thread
import matplotlib.pyplot as plt
import cv2
from shutil import copy, rmtree

def mk_file(file_path: str):
    if os.path.exists(file_path):
        # 如果文件夹存在，则先删除原文件夹在重新创建
        rmtree(file_path)
    os.makedirs(file_path)

def ConvertOne(labelme_dir, json_file, save_dir, label_name_to_value, BinaryMaskColor=True, imgcount=0):
    O_imagepath = os.path.join(save_dir,'O_image')
    maskPath = os.path.join(save_dir,'mask')
    VisPath = os.path.join(save_dir,'VisImg')
    imageName = json_file.replace(".json", "")

    json_path = osp.join(labelme_dir, json_file)
    with open(json_path, "r") as jf:
        data = json.load(jf)
        imageData = data.get("imageData")

        # labelme 的图像数据编码以及返回处理格式--------------------------------------------
        if not imageData:
            imagePath = os.path.join(r"D:\Code\Projects\defect_generation\data\results\syn\images", data["imagePath"])
            with open(imagePath, "rb") as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode("utf-8")
        img = utils.img_b64_to_arr(imageData)

        lbl, _ = utils.shapes_to_label(
            img.shape, data["shapes"], label_name_to_value)  # 灰度图，其中每个像素代表标签值

        label_names = [None] * (max(label_name_to_value.values()) + 1)  # label_names={'_background_','line','border'}



        for name, value in label_name_to_value.items():
            label_names[value] = name
        lbl_viz = imgviz.label2rgb(lbl, imgviz.asgray(img), label_names=label_names, loc="rb")  # 不同标签对应不同颜色


        # PIL.Image.fromarray(img).save(osp.join(out_dir, "img.png"))  # 2-----------------保存原图
        utils.lblsave(osp.join(maskPath, imageName + ".png"), lbl)  # #      2--------------------保存标签图片(RGB)


        Vis_image = PIL.Image.fromarray(lbl_viz)
        # Vis_image.show()
        Vis_image.save(osp.join(VisPath, imageName + ".png"))  # 3----------------保存带标签的可视化图像


        # with open(osp.join(out_dir, "label_names.txt"), "w") as f:
        #     for lbl_name in label_names:
        #         f.write(lbl_name + "\n")
        if BinaryMaskColor == True:
            binMaskpath = os.path.join(save_dir,'bin_mask')
            if not os.path.exists(binMaskpath):
                os.makedirs(binMaskpath)
            Mask = cv2.imread(osp.join(maskPath, imageName + ".png"))
            gray_image = cv2.cvtColor(Mask, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)  # 大于0即为255(Mask区域)
            white_image = np.ones_like(Mask) * 255
            result = cv2.bitwise_and(white_image, white_image, mask=mask)

            white_pixels = cv2.countNonZero(mask)  # 白色区域像素数
            white_area = white_pixels
            # 计算白色区域面积相对于整张图像面积的比例
            total_area = mask.shape[0] * mask.shape[1]
            white_area_ratio = white_area / total_area  # mask的比例(缺陷区域的面积)
            print('label_area:{}'.format(white_area))
            if total_area == 0: print(f"{imageName} found no label area")
            # if total_area >= 2987110:  # ---------------------------------------------------------------------mask的 像素 面积
            #     cv2.imwrite(osp.join(binMaskpath, str(1000+imgcount)[1:]+'_mask' + ".png"), result)  # 1------------------------保存BinaryMask图像
            #     PIL.Image.fromarray(img).save(osp.join(O_imagepath, str(1000+imgcount)[1:] + ".png"))  # 2-----------------保存原图

            # cv2.imwrite(osp.join(binMaskpath, str(1000 + imgcount)[1:] + '_mask' + ".png"),
            #             result)  # 1------------------------保存BinaryMask图像
            # PIL.Image.fromarray(img).save(
            #     osp.join(O_imagepath, str(1000 + imgcount)[1:] + ".png"))  # 2-----------------保存原图

            cv2.imwrite(osp.join(binMaskpath, imageName + '_mask' + ".png"),
                        result)  # 1------------------------保存BinaryMask图像
            PIL.Image.fromarray(img).save(
                osp.join(O_imagepath, imageName + ".png"))  # 2-----------------保存原图


def main():
    labelme_dir = r'D:\Code\Projects\defect_generation\data\results\syn\json'  # json文件所在文件夹
    save_dir = r'.\output012'  # 结果文件夹

    # 删除或合并标签，删除某类时,mask映射为0即可,0代表背景；需要的缺陷前景设置为1
    class_names = {
        '_background_': 0,
        "heidian": 1,
        'heixian': 1,
        'wuran': 1,
        'baidian': 1,
        'heiban' : 1,
        'shuiji' : 1,
        'baiban' : 1
    }

    file_list = os.listdir(labelme_dir)
    json_list = []
    [json_list.append(x) for x in file_list if x.endswith(".json")]

    O_imagepath = os.path.join(save_dir,'O_image')
    maskPath = os.path.join(save_dir,'mask')
    VisPath = os.path.join(save_dir,'VisImg')
    binmaskPath = os.path.join(save_dir, 'bin_mask')

    mk_file(O_imagepath)
    mk_file(maskPath)
    mk_file(VisPath)
    mk_file(binmaskPath)

    for count,json_file in enumerate(tqdm(json_list)):
        ConvertOne(labelme_dir, json_file, save_dir, class_names,BinaryMaskColor=True,imgcount=count)


if __name__ == "__main__":
    main()