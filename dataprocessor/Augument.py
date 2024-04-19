import os
from Augmentor.Operations import Flip, Rotate, CropPercentage
from PIL import Image
import xml.etree.ElementTree as ET
import argparse

def aug_image(aug_func):
    def wrapper(image_path, **kwargs):
        pil_img = Image.open(image_path)
        augged_img = aug_func([pil_img], **kwargs)
        return augged_img[0]

    return wrapper


def aug_xml(aug_func):
    def wrapper(xml_path, new_xml_name,**kwargs):
        root, domTree = readxml(xml_path)
        defect_object_list = root.findall("object")
        size = root.find("size")
        filename = root.find("filename")
        height = int(size.findtext("height"))
        width = int(size.findtext("width"))


        if filename.text != new_xml_name:
            filename.text = new_xml_name

        del_defect_list_index = []

        for index, defect_object in enumerate(defect_object_list):
            bndbox = defect_object.find("bndbox")
            bbox = get_bbox(bndbox)

            augged_bbox, augged_image_height, augged_image_width = aug_func(bbox, height, width, **kwargs)

            size.find("height").text = str(augged_image_height)
            size.find("width").text = str(augged_image_width)

            # 获取出界的标注
            if augged_bbox == -1:
                del_defect_list_index.append(index)
                continue
            set_bbox(bndbox, augged_bbox)

        # 删除出界的标注
        del_defect_list_index.sort(reverse=True)
        for index in del_defect_list_index:
            obj = defect_object_list.pop(index)
            root.remove(obj)

        return domTree

    return wrapper


@aug_image
def crop_image(images, percentage_area, reset_canter=None):
    """
    centre True center not change; False center random change
    randomise_percentage_area True means percentage_area random from [0,percentage_area]
    """

    cp_ins = CropPercentage(probability=1, percentage_area=percentage_area, centre=True,
                            randomise_percentage_area=False)
    cropped_images = cp_ins.perform_operation(images, reset_canter)
    return cropped_images


@aug_image
def rotate_image(images, rotation):
    """
    rotation must in [90,180,270]
    """
    rotate_ins = Rotate(probability=1, rotation=rotation)
    rotated_images = rotate_ins.perform_operation(images)
    return rotated_images


@aug_image
def flip_image(images, top_bottom_left_right):
    """
    top_bottom_left_right must in ``LEFT_RIGHT``, ``TOP_BOTTOM``, or ``RANDOM``.
    """
    flip_ins = Flip(probability=1, top_bottom_left_right=top_bottom_left_right)
    flipped_images = flip_ins.perform_operation(images)
    return flipped_images


@aug_xml
def crop_xml(bbox, image_height, image_width, percentage_area,reset_center=None):  # reset_center:(w,h)
    cropped_image_height = int(image_height * percentage_area)
    cropped_image_width = int(image_width * percentage_area)

    # 计算长和宽的单侧偏移量
    if reset_center:
        offset_height = int(reset_center[1] - cropped_image_height / 2)
        offset_width = int(reset_center[0] - cropped_image_width / 2)
    else:
        offset_height = int((image_height - cropped_image_height) / 2)
        offset_width = int((image_width - cropped_image_width) / 2)


    ori_xmin, ori_ymin, ori_xmax, ori_ymax = bbox

    # 出界缺陷
    # 如果原缺陷 左侧X坐标大于crop image对应的原图右侧X坐标 or 右测X坐标小于crop image对应原图左侧X坐标
    if ori_xmin >= (image_width - offset_width) or ori_xmax <= offset_width:
        cropped_bbox = -1
    # 如果原缺陷 底部Y坐标小于crop image对应的原图顶部Y坐标 or 顶部Y坐标大于crop image对应原图底部Y坐标
    elif ori_ymax <= offset_height or ori_ymin >= (image_height - offset_height):
        cropped_bbox = -1
    else:
        cropped_xmin = max(ori_xmin - offset_width, 0)
        cropped_ymin = max(ori_ymin - offset_height, 0)

        cropped_xmax = min(ori_xmax - offset_width, cropped_image_width)
        cropped_ymax = min(ori_ymax - offset_height, cropped_image_height)

        cropped_bbox = [cropped_xmin, cropped_ymin, cropped_xmax, cropped_ymax]

    return cropped_bbox, cropped_image_height, cropped_image_width


@aug_xml
def flip_xml(bbox, image_height, image_width, top_bottom_left_right):
    flipped_image_height = image_height
    flipped_image_width = image_width

    ori_xmin, ori_ymin, ori_xmax, ori_ymax = bbox
    defect_height = ori_ymax - ori_ymin
    defect_width = ori_xmax - ori_xmin

    if top_bottom_left_right == "LEFT_RIGHT":
        flip_xmin = image_width - ori_xmax
        flip_ymin = ori_ymin

    else:  # top_bottom_left_right == "TOP_BOTTOM":
        flip_xmin = ori_xmin
        flip_ymin = image_height - ori_ymax

    flipped_bbox = [flip_xmin, flip_ymin, flip_xmin + defect_width, flip_ymin + defect_height]

    return flipped_bbox, flipped_image_height, flipped_image_width


@aug_xml
def rotate_xml(bbox, image_height, image_width, rotation):
    ori_xmin, ori_ymin, ori_xmax, ori_ymax = bbox
    defect_height = ori_ymax - ori_ymin
    defect_width = ori_xmax - ori_xmin

    assert rotation in (90, 180, 270)
    if rotation == 90:
        new_xmin = ori_ymin
        new_ymin = image_width - ori_xmax
        new_defect_width = defect_height
        new_defect_height = defect_width
        new_image_width = image_height
        new_image_height = image_width

    elif rotation == 180:
        new_xmin = image_width - ori_xmax
        new_ymin = image_height - ori_ymax
        new_defect_width = defect_width
        new_defect_height = defect_height
        new_image_width = image_width
        new_image_height = image_height

    else:  # rotation == 270:
        new_xmin = image_height - ori_ymax
        new_ymin = ori_xmin
        new_defect_width = defect_height
        new_defect_height = defect_width
        new_image_width = image_height
        new_image_height = image_width

    rotated_bbox = [new_xmin, new_ymin, new_xmin + new_defect_width, new_ymin + new_defect_height]
    rotated_image_height = new_image_height
    rotated_image_width = new_image_width

    return rotated_bbox, rotated_image_height, rotated_image_width


def readxml(xml_path):
    domTree = ET.ElementTree(file=xml_path)
    root = domTree.getroot()
    return root, domTree


def get_bbox(bndbox):
    xmin = int(float(bndbox.findtext("xmin")))
    ymin = int(float(bndbox.findtext("ymin")))
    xmax = int(float(bndbox.findtext("xmax")))
    ymax = int(float(bndbox.findtext("ymax")))
    return [xmin, ymin, xmax, ymax]


def set_bbox(bndbox, cropped_bbox):
    cropped_xmin, cropped_ymin, cropped_xmax, cropped_ymax = cropped_bbox
    bndbox.find("xmin").text = str(cropped_xmin)
    bndbox.find("ymin").text = str(cropped_ymin)
    bndbox.find("xmax").text = str(cropped_xmax)
    bndbox.find("ymax").text = str(cropped_ymax)


if __name__ == "__main__":


    image_dir = r"D:\Code\Dataset\士兰微\士兰微数据增强后\士兰微训练集-数据集-20231205112753\images"
    xml_dir = r"D:\Code\Dataset\士兰微\士兰微数据增强后\士兰微训练集-数据集-20231205112753\annotations"

    save_dir = r"D:\Code\Dataset\士兰微\士兰微数据增强后\output"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for image_file in os.listdir(image_dir):
        if not image_file.endswith(("bmp", "BMP", "png", "PNG", "jpg", "JPG")):
            continue
        image_path = os.path.join(image_dir, image_file)
        pil_img = Image.open(image_path)

        image_name = ".".join(image_file.split(".")[:-1])
        xml_path = os.path.join(xml_dir, image_name + ".xml")


        # crop
        percentage_area = 0.5
        cropped_img = crop_image(image_path, percentage_area=percentage_area,reset_canter=None)
        

        new_xml_name = "{}_crop_{}.xml".format(image_name, percentage_area)
        new_image_name = "{}_crop_{}.jpg".format(image_name, percentage_area)

        domTree = crop_xml(xml_path, new_xml_name, percentage_area=percentage_area, reset_center=None)
        new_xml = os.path.join(save_dir, new_xml_name)
        new_img = os.path.join(save_dir, new_image_name)
        cropped_img.save(new_img)
        domTree.write(new_xml, encoding="utf-8")

        """ 
        # # flip
        # top_bottom_left_right = "TOP_BOTTOM"  # or LEFT_RIGHT,TOP_BOTTOM
        # flipped_img = flip_image(image_path, top_bottom_left_right=top_bottom_left_right)
        #
        # new_xml_name = "{}_flipped_{}.xml".format(image_name, top_bottom_left_right)
        # new_image_name = "{}_flipped_{}.jpg".format(image_name, top_bottom_left_right)
        #
        # new_xml = os.path.join(save_dir,new_xml_name )
        # new_img = os.path.join(save_dir,new_image_name )
        #
        # domTree = flip_xml(xml_path, new_xml_name, top_bottom_left_right=top_bottom_left_right)
        #
        # flipped_img.save(new_img)
        # domTree.write(new_xml, encoding="utf-8")

        # rotate
        rotation = 270
        rotated_img = rotate_image(image_path, rotation=rotation)

        new_xml_name = "{}_rotated_{}.xml".format(image_name, rotation)
        new_image_name "{}_rotated_{}.jpg".format(image_name, rotation)

        new_xml = os.path.join(save_dir, new_xml_name)
        new_img = os.path.join(save_dir,new_image_name )

        domTree = rotate_xml(xml_path,new_xml_name,rotation=rotation)
        rotated_img.save(new_img)
        domTree.write(new_xml, encoding="utf-8")
        """


