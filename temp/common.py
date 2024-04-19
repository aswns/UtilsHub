#!/user/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2022/11/10 14:22
# @Author  : Ina
# @File    : common.py

import cv2
import numpy as np
import random as rd
import os
from xml.dom.minidom import Document
from PIL import Image
from base64 import b64encode
from io import BytesIO
from skimage import measure
import json
import shutil


# from pandas import DataFrame


def mkdir_or_exist(dir_name, mode=0o777):
    """
    brief: 创建文件夹，如果有先删除
    param {*}
    return {*}
    """
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    if dir_name == '':
        return
    # dir_name = os.path.expanduser(dir_name)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, mode=mode)


def mkdir_or_exist_not_remove(dir_name, mode=0o777):
    """
    brief: 创建文件夹，如果有直接返回
    param {*}
    return {*}
    """
    if os.path.exists(dir_name):
        return
    if dir_name == '':
        return
    # dir_name = os.path.expanduser(dir_name)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, mode=mode)


def component_polygon_area(poly):
    """Compute the area of a component of a polygon.
    Args:
        :param poly:
        x (ndarray): x coordinates of the component
        y (ndarray): y coordinates of the component

    Return:
        float: the area of the component
    """
    x = poly[:, 0]
    y = poly[:, 1]
    return 0.5 * np.abs(
        np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))  # np.roll 意即“滚动”，类似移位操作
    # 注意这里的np.dot表示一维向量相乘


def get_nums(n, pts_list):
    poly_area = [component_polygon_area(np.array(polygon)) for polygon in pts_list]
    # max_index = poly_area.index(max(poly_area))
    total_area = sum(poly_area)
    p_nums = [round(n * area / total_area) for area in poly_area]
    if sum(p_nums) < n:
        p_nums[min(p_nums)] += n - sum(p_nums)
    elif sum(p_nums) > n:
        p_nums[max(p_nums)] -= sum(p_nums) - n
    return p_nums


# def get_pts_list_2(file):
#     with open(file, mode='r', encoding='utf-8') as load_f:  # 导入json标签的地址
#         load_dict = json.load(load_f)
#     load_f.close()
#     shapes = load_dict['shapes']
#     df_shapes = DataFrame(data=shapes)
#     df_res = df_shapes.groupby(['label'])['points'].sum()
#     pts_list = [{i: j} for i, j in df_res.items()]
#     return pts_list


def get_pts_list(file):
    pts_list = []
    with open(file, mode='r', encoding='utf-8') as load_f:  # 导入json标签的地址
        load_dict = json.load(load_f)
    load_f.close()
    shapes = load_dict['shapes']
    for shape in shapes:
        pts = shape["points"]
        pts_list.append(pts)
    return pts_list


def img_to_byte(img, ext):
    # 类型转换 重要代码
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ENCODING = 'utf-8'
    img_byte = BytesIO()
    if ext in ['.jpg', '.jpeg']:
        format = 'JPEG'
    else:
        format = 'PNG'
    img_pil.save(img_byte, format=format)
    binary_str2 = img_byte.getvalue()
    imageData = b64encode(binary_str2)
    base64_string = imageData.decode(ENCODING)
    return base64_string


def close_contour(contour):
    if not np.array_equal(contour[0], contour[-1]):
        contour = np.vstack((contour, contour[0]))
    return contour


def binary_mask_to_polygon(binary_mask, tolerance=0):
    """Converts a binary mask to COCO polygon representation
    Args:
        binary_mask: a 2D binary numpy array where '1's represent the object
        tolerance: Maximum distance from original points of polygon to approximated
            polygonal chain. If tolerance is 0, the original coordinate array is returned.
    """
    polygons = []
    # pad mask to close contours of shapes which start and end at an edge
    padded_binary_mask = np.pad(binary_mask, pad_width=1, mode='constant', constant_values=0)
    contours = measure.find_contours(padded_binary_mask, 0.5)
    # contours = np.subtract(contours, 1)
    for contour in contours:
        contour -= 1
        contour = close_contour(contour)
        contour = measure.approximate_polygon(contour, tolerance)
        if len(contour) < 3:
            continue
        contour = np.flip(contour, axis=1)
        segmentation = contour.ravel().tolist()
        # after padding and subtracting 1 we may get -0.5 points in our segmentation
        segmentation = [0 if i < 0 else i for i in segmentation]
        polygons.append(segmentation)

    return polygons


def get_operated_mask(img):
    t, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    se = cv2.morphologyEx(se, cv2.MORPH_CLOSE, (2, 2))
    mask = cv2.dilate(binary, se)
    # contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # binary_3 = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    # area = []
    # for k in range(len(contours)):
    #     area.append(cv2.contourArea(contours[k]))
    # # 轮廓索引
    # max_idx = np.argsort(np.array(area))
    # # 按轮廓索引填充颜色
    # filled = cv2.drawContours(binary_3, contours, max_idx[-1], (0, 0, 255), cv2.FILLED)
    # mask = np.zeros_like(binary)
    # mask[(filled[:, :, 0] == 0) & (filled[:, :, 1] == 0) & (filled[:, :, 2] == 255)] = 255
    mask_inv = cv2.bitwise_not(mask)
    return mask_inv, mask


def get_scaled_mask(img):
    t, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    se = cv2.morphologyEx(se, cv2.MORPH_CLOSE, (2, 2))
    mask = cv2.erode(binary, se)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    t, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    return mask, mask_inv


def get_depressing_mask(fg):
    depr_mask = 255 * np.zeros(fg.shape, fg.dtype)
    depr_mask[0:5, 0:5] = 1
    return depr_mask


def is_inside_polygon(pt, poly):
    c = False
    i = -1
    length = len(poly)
    if length == 0:
        return False
    else:
        j = length - 1
        while i < length - 1:
            i += 1
            if ((poly[i][0] <= pt[0] < poly[j][0]) or (
                    poly[j][0] <= pt[0] < poly[i][0])):
                if (pt[1] < (poly[j][1] - poly[i][1]) * (pt[0] - poly[i][0]) / (
                        poly[j][0] - poly[i][0]) + poly[i][1]):
                    c = not c
            j = i
        return c


def get_location(fg_shape, bg_shape, polygon):
    h1, w1 = fg_shape
    h2, w2 = bg_shape
    while len(polygon) != 0:
        x = rd.randint(0, w2)
        y = rd.randint(0, h2)
        if (x + w1) > w2:
            x = w2 - w1
        if (y + h1) > h2:
            y = h2 - h1
        c_x = int(x + w1 / 2)
        c_y = int(y + h1 / 2)
        point = [c_x, c_y]
        if is_inside_polygon(point, polygon) is True:
            return [x, y]


def select_files(file_dir, num):
    files_list = []
    dic = {}
    dirs = os.listdir(file_dir)
    for index, folder in enumerate(dirs):
        path_file = os.listdir(os.path.join(file_dir, folder))
        pick_number = min(num, len(path_file))
        files = rd.sample(path_file, pick_number)
        files_path = [os.path.join(file_dir, folder, file) for file in files]
        files_list.extend(files_path)
        dic[str(index)] = folder
    return files_list, dic


def get_points(fg_shape, p):
    h1, w1 = fg_shape
    x_min, y_min = p
    x_max, y_max = p[0] + w1, p[1] + h1
    points = [[x_min, y_min], [x_min, y_max], [x_max, y_max], [x_max, y_min]]
    return points


def get_box(fg_shape, bg_shape, p):
    h1, w1 = fg_shape
    h2, w2 = bg_shape
    x, y = p
    c_x = int(x + w1 / 2)
    c_y = int(y + h1 / 2)

    x_ = c_x / w2
    y_ = c_y / h2
    w_ = w1 / w2
    h_ = h1 / h2

    return x_, y_, w_, h_


# chinese
def cv2_imread(path, flags=1):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), flags)


def cv2_imwrite(path, img):
    _, form = os.path.splitext(path)
    cv2.imencode(form, img)[1].tofile(path)


def make_xml(img_path, dic, txt_path, xml_path):  # txt所在文件夹路径，xml文件保存路径，图片所在文件夹路径
    try:
        dir, file = os.path.split(img_path)
        name, form = os.path.splitext(file)
        img = cv2_imread(img_path, flags=-1)
        if img.ndim == 2:
            img = np.expand_dims(img, axis=-1)

        xml_builder = Document()
        annotation = xml_builder.createElement("annotation")  # 创建annotation标签
        xml_builder.appendChild(annotation)
        txt_file = open(txt_path + '/' + name + '.txt')
        txt_list = txt_file.readlines()
        pheight, pwidth, pdepth = img.shape

        folder = xml_builder.createElement("folder")  # folder标签
        foldercontent = xml_builder.createTextNode("smart_annotations")
        folder.appendChild(foldercontent)
        annotation.appendChild(folder)  # folder标签结束

        filename = xml_builder.createElement("filename")  # filename标签
        filenamecontent = xml_builder.createTextNode(file)
        filename.appendChild(filenamecontent)
        annotation.appendChild(filename)  # filename标签结束

        size = xml_builder.createElement("size")  # size标签
        width = xml_builder.createElement("width")  # size子标签width
        widthcontent = xml_builder.createTextNode(str(pwidth))
        width.appendChild(widthcontent)
        size.appendChild(width)  # size子标签width结束

        height = xml_builder.createElement("height")  # size子标签height
        heightcontent = xml_builder.createTextNode(str(pheight))
        height.appendChild(heightcontent)
        size.appendChild(height)  # size子标签height结束

        depth = xml_builder.createElement("depth")  # size子标签depth
        depthcontent = xml_builder.createTextNode(str(pdepth))
        depth.appendChild(depthcontent)
        size.appendChild(depth)  # size子标签depth结束

        annotation.appendChild(size)  # size标签结束

        for j in txt_list:
            oneline = j.strip().split(" ")
            object = xml_builder.createElement("object")  # object 标签
            picname = xml_builder.createElement("name")  # name标签
            namecontent = xml_builder.createTextNode(dic[oneline[0]])
            picname.appendChild(namecontent)
            object.appendChild(picname)  # name标签结束

            pose = xml_builder.createElement("pose")  # pose标签
            posecontent = xml_builder.createTextNode("Unspecified")
            pose.appendChild(posecontent)
            object.appendChild(pose)  # pose标签结束

            truncated = xml_builder.createElement("truncated")  # truncated标签
            truncated_content = xml_builder.createTextNode("0")
            truncated.appendChild(truncated_content)
            object.appendChild(truncated)  # truncated标签结束

            difficult = xml_builder.createElement("difficult")  # difficult标签
            difficultcontent = xml_builder.createTextNode("0")
            difficult.appendChild(difficultcontent)
            object.appendChild(difficult)  # difficult标签结束

            bndbox = xml_builder.createElement("bndbox")  # bndbox标签
            xmin = xml_builder.createElement("xmin")  # xmin标签
            math_data = int(((float(oneline[1])) * pwidth + 1) - (float(oneline[3])) * 0.5 * pwidth)
            xmin_content = xml_builder.createTextNode(str(math_data))
            xmin.appendChild(xmin_content)
            bndbox.appendChild(xmin)  # xmin标签结束

            ymin = xml_builder.createElement("ymin")  # ymin标签
            math_data = int(((float(oneline[2])) * pheight + 1) - (float(oneline[4])) * 0.5 * pheight)
            ymin_content = xml_builder.createTextNode(str(math_data))
            ymin.appendChild(ymin_content)
            bndbox.appendChild(ymin)  # ymin标签结束

            xmax = xml_builder.createElement("xmax")  # xmax标签
            math_data = int(((float(oneline[1])) * pwidth + 1) + (float(oneline[3])) * 0.5 * pwidth)
            xmax_content = xml_builder.createTextNode(str(math_data))
            xmax.appendChild(xmax_content)
            bndbox.appendChild(xmax)  # xmax标签结束

            ymax = xml_builder.createElement("ymax")  # ymax标签
            math_data = int(((float(oneline[2])) * pheight + 1) + (float(oneline[4])) * 0.5 * pheight)
            ymax_content = xml_builder.createTextNode(str(math_data))
            ymax.appendChild(ymax_content)
            bndbox.appendChild(ymax)  # ymax标签结束

            object.appendChild(bndbox)  # bndbox标签结束

            annotation.appendChild(object)  # object标签结束

        with open(xml_path + '/' + name + ".xml", mode='w', encoding='utf-8') as f:
            xml_builder.writexml(f, encoding='utf-8')
        f.close()
    except Exception as e:
        print('%s: %s' % (e, name))

# if __name__ == '__main__':
# img_path = 'data/results/extract/defect_masks/5_keliwu/1666833763761665_1.jpg'
# img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
# mask, mask_inv = get_scaled_mask(img)
# cv2.imwrite('mask.png', mask)
