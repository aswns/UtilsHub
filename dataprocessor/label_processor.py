import cv2
import os
import numpy as np
import base64
import json
import shutil

def resize_segjson_anno(input_json_path, output_json_path, ori_wh, new_wh):
    """resize and save seg annotation of labelme format
    """
    w_ratio = new_wh[0]/ori_wh[0]
    h_ratio = new_wh[1]/ori_wh[1]
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)   
    data["imageWidth"], data["imageHeight"]= new_wh
    shapes = data["shapes"]

    for shape in shapes:
        points = shape["points"]
        for i, pt in enumerate(points):
            pt = [pt[0] * w_ratio, pt[1] * h_ratio]
            points[i] = pt
        shape["points"] = points
    data["shapes"] = shapes
    with open(output_json_path, "w", encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"json_path edited!:{output_json_path}")

if __name__ == "__main__":
    input_jsondir = "E:\dataset\屏显\屏显分类验证\huaxing_spot256-数据集-20240407101539\json_mark"
    out_jsondir = input_jsondir+"_resized512"
    if os.path.exists(out_jsondir):shutil.rmtree(out_jsondir)
    os.makedirs(out_jsondir)
    for file in os.listdir(input_jsondir):
        filepath = os.path.join(input_jsondir, file)
        savepath = os.path.join(out_jsondir, file)
        resize_segjson_anno(filepath,savepath,(256,256),(512,512))
    
