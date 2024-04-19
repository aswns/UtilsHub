'''
对比测试集的标签xml与预测结果xml,分析过检、漏检、错检
suspended : platform output image and xml names different from upload image names
'''
import cv2
import random
from PIL import Image, ImageDraw, ImageFont
import os
import shutil
import xml.etree.ElementTree as ET
import argparse

def make_out_path(test_results):
    save_path = os.path.join(test_results,"analysis")
    if os.path.exists(save_path): shutil.rmtree(save_path)
    # 确保输出图片文件夹存在
    guojian_path = os.path.join(save_path, "过检")
    loujian_path = os.path.join(save_path, "漏检")
    cuojian_path = os.path.join(save_path, "错检")
    os.makedirs(guojian_path)
    os.makedirs(loujian_path)
    os.makedirs(cuojian_path)
    return guojian_path,loujian_path,cuojian_path


def draw_detections(boxes,names,img):
    print("boxes:",len(boxes))
    print("names:",len(names))
    colors = []
    for j in range(0, len(names)):
        a = random.randint(0, 255)
        colors.append(a)
    for box,color,name in zip(boxes,colors,names):
        print(box)
        print(name)
        xmin, ymin, xmax, ymax = box[0],box[1],box[2],box[3]
        print(xmin, ymin, xmax, ymax)
        cv2.rectangle(img,(xmin, ymin),(xmax, ymax),color,2)
        cv2.putText(img, name, (xmin, ymin - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2,lineType=cv2.LINE_AA)
    return img

def draw_detections_pil(boxes,names,img1):
    imgshow = Image.fromarray(img1)
    draw = ImageDraw.Draw(imgshow)
    print("boxes:", len(boxes))
    print("names:", len(names))

    for box, name in zip(boxes,names):
        xmin, ymin, xmax, ymax = box[0],box[1],box[2],box[3]
        print(xmin, ymin, xmax, ymax)
        # color=tuple(color.astype(np.uint8).tolist())
        draw.rectangle([xmin, ymin,xmax, ymax],outline=(255,0,0), width=3)
        font = ImageFont.truetype('Arial.Unicode.ttf', 20)
        text = name
        text_width, text_height = draw.textsize(text, font=font)
        draw.text((xmin+5, ymin - text_height), text, font=font, fill=(255,0,0))
    return imgshow


def GetObjectsFromXml(xml_path):
    '''
    从XML文件获取{cls:x1y1x2y2}
    '''
    ObjectDict={}
    tree_org = ET.parse(xml_path)
    ObjectDict['filename'] = tree_org.find("filename").text
    ObjectDict['width'] = tree_org.find('size').find('width').text
    ObjectDict['height'] = tree_org.find('size').find('height').text
    ObjectDict['object']=[]
    objs = tree_org.findall('object')
    for i, obj in enumerate(objs):
        cls_name = obj.find('name').text
        box_x1y1x2y2=[int(obj.find('bndbox').find('xmin').text),int(obj.find('bndbox').find('ymin').text),
                  int(obj.find('bndbox').find('xmax').text),int(obj.find('bndbox').find('ymax').text)]
        if cls_name not in ObjectDict.keys():
            ObjectDict[cls_name] = [box_x1y1x2y2]
        else: ObjectDict[cls_name].append(box_x1y1x2y2)
    return ObjectDict

def draw_detections(boxes,names,img):
    print("boxes:",len(boxes))
    print("names:",len(names))
    colors = []
    for j in range(0, len(names)):
        a = random.randint(0, 255)
        colors.append(a)
    for box,color,name in zip(boxes,colors,names):
        print(box)
        print(name)
        xmin, ymin, xmax, ymax = box[0],box[1],box[2],box[3]
        print(xmin, ymin, xmax, ymax)
        cv2.rectangle(img,(xmin, ymin),(xmax, ymax),color,2)
        cv2.putText(img, name, (xmin, ymin - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2,lineType=cv2.LINE_AA)
    return img


def Analysis_xmls(test_data, test_results):
    # 获取输入图片文件夹路径
    test_images_folder = os.path.join(test_results, "images")
    # 获取输入标签文件夹路径
    test_labels_folder = os.path.join(test_data, "annotations")
    result_xml_folder = os.path.join(test_results,"annotations")

    guojian_path,loujian_path,cuojian_path = make_out_path(test_results)

    loujian_count,guojian_count,cuojian_count = 0, 0, 0

    for filename in os.listdir(test_images_folder):

        input_image_path = os.path.join(test_images_folder, filename)

        # 检查是否为图片文件
        if os.path.isfile(input_image_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png', 'bmp')):
            # 构造对应的标签文件路径
            label_filename = os.path.splitext(filename)[0] + ".xml"
            label_path = os.path.join(test_labels_folder, label_filename)
            pred_path = os.path.join(result_xml_folder, label_filename)

            labels = GetObjectsFromXml(label_path)
            preds = GetObjectsFromXml(label_path)

            if len(preds.keys())==0 and len(labels.keys())>0:  # 漏检
                #img = cv2.imread(input_image_path)
                objs = labels
                new_name = ""
                for name in objs.keys():
                    new_name += (name+ "_")
                loujian_count += 1
                new_name = new_name + str(loujian_count) + os.path.splitext(filename)[1]
                shutil.copy(input_image_path,os.path.join(loujian_path,new_name))
                print(f"漏检 : {input_image_path}")
            # elif len(preds.keys())>0 and len(labels.keys())==0:  # 过检




            #for pred_cls in preds.keys():






if __name__ == "__main__":
    parser = argparse.ArgumentParser("Analysis_tested_xmls", add_help=True)
    parser.add_argument("--test_data", type=str, default=r"D:\Code\00data\乾照\测试集_乾照数据1220训练样本-数据集-20231221112048")
    parser.add_argument("--test_results", type=str, default=r"D:\Code\00data\乾照\旧数据模型_测试集智能标注0.1")
    """
    inputs:
    test_data,test_results
        -images - .jpg
        -annotations - .xml
    
    outputs:
    os.path.join(test_results,"analysis")
    del old dir if exits
    """

    args = parser.parse_args()
    Analysis_xmls(args.test_data, args.test_results)
