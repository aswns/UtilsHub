'''
按xml中的object 面积大小 重命名缺陷
'''

from PIL import Image
import os
import shutil
import xml.etree.ElementTree as ET
import argparse


def xml_img_scaling(input_path, save_path, w, h):
    # 获取输入图片文件夹路径
    input_images_folder = os.path.join(input_path, "images")

    # 获取输入标签文件夹路径
    input_labels_folder = os.path.join(input_path, "annotations")

    # 获取输出图片文件夹路径
    output_images_folder = os.path.join(save_path, "images")

    # 获取输出标签文件夹路径
    output_labels_folder = os.path.join(save_path, "annotations")

    if os.path.exists(save_path): shutil.rmtree(save_path)
    # 确保输出图片文件夹存在
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)

    # 确保输出标签文件夹存在
    if not os.path.exists(output_labels_folder):
        os.makedirs(output_labels_folder)

    defectname = {"7_Scratch":[], "10_Small_Scratch":[],"4_Metal_defect":[], "9_Small_Metal_defect":[]}


    # 遍历输入图片文件夹中的所有文件,搜索记录mean area
    for filename in os.listdir(input_images_folder):
        # 拼接输入图片文件的完整路径
        input_image_path = os.path.join(input_images_folder, filename)

        # 检查是否为图片文件
        if os.path.isfile(input_image_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 构造对应的标签文件路径
            label_filename = os.path.splitext(filename)[0] + ".xml"
            input_label_path = os.path.join(input_labels_folder, label_filename)
            output_label_path = os.path.join(output_labels_folder, label_filename)

            # 如果标签文件存在，则复制并调整其内容
            if os.path.isfile(input_label_path):
                # 打开输入标签文件
                tree = ET.parse(input_label_path)
                root = tree.getroot()
                # 调整标签文件中的尺寸信息
                size = root.find('size')

                size.find('width').text = str(w)
                size.find('height').text = str(h)

                for obj in root.findall('object'):
                    name = obj.find('name').text
                    if name in defectname:
                        bbox = obj.find('bndbox')
                        xmin = int(float(bbox.find('xmin').text))
                        ymin = int(float(bbox.find('ymin').text))
                        xmax = int(float(bbox.find('xmax').text))
                        ymax = int(float(bbox.find('ymax').text))
                        area = (xmax-xmin)*(ymax-ymin)
                        defectname[name].append(area)


    for key in defectname.keys():
        print(f"{key} 数量统计 : {len(defectname[key])}")
        defectname[key] = sum(defectname[key])/len(defectname[key])

    threshold_Area = {"scratch":0,"Metal_defect":0}
    threshold_Area["scratch"] = (defectname["7_Scratch"] + defectname["10_Small_Scratch"])/2
    threshold_Area["Metal_defect"] = (defectname["4_Metal_defect"] + defectname["9_Small_Metal_defect"])/2


    defectname = {"7_Scratch":[], "10_Small_Scratch":[],"4_Metal_defect":[], "9_Small_Metal_defect":[]}
    # 遍历输入图片文件夹中的所有文件,搜索记录mean area
    for filename in os.listdir(input_images_folder):
        # 拼接输入图片文件的完整路径
        input_image_path = os.path.join(input_images_folder, filename)
        # 检查是否为图片文件
        if os.path.isfile(input_image_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            shutil.copy2(input_image_path, output_images_folder)

            # 构造对应的标签文件路径
            label_filename = os.path.splitext(filename)[0] + ".xml"
            input_label_path = os.path.join(input_labels_folder, label_filename)
            output_label_path = os.path.join(output_labels_folder, label_filename)

            # 如果标签文件存在，则复制并调整其内容
            if os.path.isfile(input_label_path):
                # 打开输入标签文件
                tree = ET.parse(input_label_path)
                root = tree.getroot()

                for obj in root.findall('object'):
                    name = obj.find('name').text
                    if name in ["7_Scratch", "10_Small_Scratch"]:
                        bbox = obj.find('bndbox')
                        xmin = int(float(bbox.find('xmin').text))
                        ymin = int(float(bbox.find('ymin').text))
                        xmax = int(float(bbox.find('xmax').text))
                        ymax = int(float(bbox.find('ymax').text))
                        area = (xmax - xmin) * (ymax - ymin)
                        if area < threshold_Area["scratch"]:
                            obj.find('name').text = "10_Small_Scratch"
                        else:
                            obj.find('name').text = "7_Scratch"
                    if name in ["4_Metal_defect", "9_Small_Metal_defect"]:
                        bbox = obj.find('bndbox')
                        xmin = int(float(bbox.find('xmin').text))
                        ymin = int(float(bbox.find('ymin').text))
                        xmax = int(float(bbox.find('xmax').text))
                        ymax = int(float(bbox.find('ymax').text))
                        area = (xmax - xmin) * (ymax - ymin)
                        if area < threshold_Area["Metal_defect"]:
                            obj.find('name').text = "9_Small_Metal_defect"
                        else:
                            obj.find('name').text = "4_Metal_defect"
                # 保存调整后的标签文件
                tree.write(output_label_path)

            #print(f"已处理: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Center Crop img and xml", add_help=True)
    parser.add_argument("--input_path", type=str, default=r"D:\Code\Dataset\华润微\12A模型问题12月1日\数据与模型\104\104\dataset_scaled")
    parser.add_argument("--save_path", type=str, default="./object_classify_output")

    parser.add_argument("--img_size", type=int, nargs="+", default=(400, 400))
    args = parser.parse_args()
    xml_img_scaling(args.input_path, args.save_path, *args.img_size)





# import xml.etree.ElementTree as ET
# import os
# import shutil
# # 修改自己的路径
# template_file = r'E:\dataset\IC基板检测验证\产品二\产品二bmp\dataset\annotations'  #这里是存放xml文件的文件夹
# xmllist = os.listdir(template_file)

# origin_name_list = []

# for xml in xmllist:
#     name = ""
#     #print(xml)
#     tree = ET.parse(os.path.join(template_file,xml))
#     root = tree.getroot() # 获取根节点
#     filename_element = root.find('filename')
#     filename_element.text = filename_element.text.replace(".jpg",".bmp")


#     #         child.tag = xml.replace(".xml",".png")
#     tree=ET.ElementTree(root)
#     tree.write(os.path.join(template_file, xml))

    
"""
批量修改xml文件中的缺陷类别名称
当有多个物体时，多个物体的名称均能被修改
"""


import xml.etree.ElementTree as ET
import os
import shutil
# 修改自己的路径
template_file = r"E:\dataset\屏显\屏显外观IC基板检测验证\0308莱宝缺陷图\第二款产品\ng品\NG_0201row9col6-重度偏右上-train\photo_cropped"  #xml文件 dir
xmllist = os.listdir(template_file)

origin_name_list = []


# ## 删除空标注
# for xml in xmllist:
#     name = ""
#     #print(xml)
#     tree = ET.parse(os.path.join(template_file,xml))
#     root = tree.getroot() # 获取根节点
#     for child in root:
#         if child.tag == 'object':
#             name = child.find('name').text
#             if name not in origin_name_list: origin_name_list.append(name)
#     if name != "":  #空标注
#         xmlpath = os.path.join(template_file,xml)
#         imgpath = os.path.join(r"D:\Code\Dataset\华磊\gocheck\待迭代数据\dataset\images",xml.replace(".xml",".png"))
#         shutil.copy(xmlpath,r"D:\Code\Dataset\华磊\gocheck\待迭代数据\dataset删除空标注\annotations")
#         #shutil.copy(imgpath, r"D:\Code\Dataset\华磊\gocheck\待迭代数据\dataset删除空标注\images")
# print(origin_name_list)


## 修改xml label 名
mapDict = {'线路短路':'环形短路'}

for xml in xmllist:
    if ".xml" not in xml:continue
    tree = ET.parse(os.path.join(template_file,xml))
    root = tree.getroot() # 获取根节点
    for child in root:
        if child.tag == 'object':
            name = child.find('name').text
            if name in mapDict.keys():
                child.find('name').text = mapDict[name]
                tree=ET.ElementTree(root)
    tree.write(os.path.join(template_file, xml))