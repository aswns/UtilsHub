'''
按比例改变图像尺寸与标注尺寸
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

    if os.path.exists(save_path):shutil.rmtree(save_path)
    # 确保输出图片文件夹存在
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)

    # 确保输出标签文件夹存在
    if not os.path.exists(output_labels_folder):
        os.makedirs(output_labels_folder)

    # 遍历输入图片文件夹中的所有文件
    for filename in os.listdir(input_images_folder):
        # 拼接输入图片文件的完整路径
        input_image_path = os.path.join(input_images_folder, filename)

        # 检查是否为图片文件
        if os.path.isfile(input_image_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 打开图片文件
            image = Image.open(input_image_path)

            # 调整图片分辨率为640x640
            resized_image = image.resize((w, h))

            # 构造输出图片文件的完整路径
            output_image_path = os.path.join(output_images_folder, filename)

            # 保存调整分辨率后的图片
            resized_image.save(output_image_path)

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
                width = int(size.find('width').text)
                height = int(size.find('height').text)
                size.find('width').text = str(w)
                size.find('height').text = str(h)

                # 调整标签文件中的位置信息
                scale_x = w / width
                scale_y = h / height

                for obj in root.findall('object'):
                    bbox = obj.find('bndbox')
                    xmin = int(float(bbox.find('xmin').text))
                    ymin = int(float(bbox.find('ymin').text))
                    xmax = int(float(bbox.find('xmax').text))
                    ymax = int(float(bbox.find('ymax').text))

                    bbox.find('xmin').text = str(int(xmin * scale_x))
                    bbox.find('ymin').text = str(int(ymin * scale_y))
                    bbox.find('xmax').text = str(int(xmax * scale_x))
                    bbox.find('ymax').text = str(int(ymax * scale_y))

                # 保存调整后的标签文件
                tree.write(output_label_path)

            print(f"已处理: {filename}")

    print("图片分辨率和标签文件调整完成！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Center Crop img and xml", add_help=True)
    parser.add_argument("--input_path", type=str, default="./inputs")
    parser.add_argument("--save_path", type=str, default="./scaling_outputs")
    parser.add_argument("--img_size", type=int, nargs="+", default=(400, 400))
    args = parser.parse_args()
    xml_img_scaling(args.input_path, args.save_path, *args.img_size)




