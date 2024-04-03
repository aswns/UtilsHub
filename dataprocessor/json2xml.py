# -*- coding: utf-8 -*-
# time: 2024/3/13 11:31
# file: json_to_xml.py
# author: ina


import json
import xml.etree.ElementTree as ET
import os

def convert_labelme_folder_to_labelimg(json_folder, output_folder):
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_folder, json_file)
            xml_file = os.path.join(output_folder, json_file.replace(".json", ".xml"))
            convert_labelme_to_labelimg(json_path, xml_file)

def convert_labelme_to_labelimg(json_file, xml_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    root = ET.Element("annotation")

    folder = ET.SubElement(root, "folder")
    folder.text = "images"

    filename = ET.SubElement(root, "filename")
    filename.text = data["imagePath"]

    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    height = ET.SubElement(size, "height")
    depth = ET.SubElement(size, "depth")
    width.text = str(data["imageWidth"])
    height.text = str(data["imageHeight"])
    depth.text = "3"

    for shape in data["shapes"]:
        object_elem = ET.SubElement(root, "object")
        name = ET.SubElement(object_elem, "name")
        name.text = shape["label"]
        bndbox = ET.SubElement(object_elem, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        ymin = ET.SubElement(bndbox, "ymin")
        xmax = ET.SubElement(bndbox, "xmax")
        ymax = ET.SubElement(bndbox, "ymax")
        xmin.text = str(int(min([point[0] for point in shape["points"]])))
        ymin.text = str(int(min([point[1] for point in shape["points"]])))
        xmax.text = str(int(max([point[0] for point in shape["points"]])))
        ymax.text = str(int(max([point[1] for point in shape["points"]])))

    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8')


if __name__ == "__main__":
    json_folder = r"E:\dataset\屏显\屏显分类验证\train_huaxing_split\guigewai\分割数据集V2\json_mark"
    output_folder = r"E:\dataset\屏显\屏显分类验证\train_huaxing_split\guigewai\分割数据集V2\xml"
    os.makedirs(output_folder, exist_ok=True)
    convert_labelme_folder_to_labelimg(json_folder, output_folder)

