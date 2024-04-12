# 用于电测分离、拼接图片通道
import sys ; sys.path.append('.')
from _utils import *
import os, sys, cv2, shutil
import numpy as np 




def main():
    rootdir = r"E:\dataset\屏显\屏显分类验证\莱宝AI小图-10890张\3月屏显电测数据集汇总"
    savedir = r"E:\dataset\屏显\屏显分类验证\莱宝AI小图-10890张\3月屏显电测数据集汇总-vis"
    if os.path.exists(savedir): shutil.rmtree(savedir)
    copy_dirs(rootdir=rootdir,savedir=savedir)

    for dirpath,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            if os.path.splitext(filename)[-1] in constant.IMG_EXTENSION:
                try:
                    img_path = os.path.join(dirpath, filename)
                    print(f"{img_path} processing")
                    img = cv2_imread(imagePath=img_path)
                    if len(img.shape) != 3:
                        print(f"ERROR : {img_path} shape: {img.shape}")
                        continue
                    b, g, r = cv2.split(img)
                    concat_img = np.concatenate([b,g],axis=1)
                    new_path = img_path.replace(rootdir, savedir)
                    cv2_imwrite(new_path, concat_img)  
                    print(f"{new_path} processed")
                except Exception as e:
                    print(e)


if __name__ == "__main__":

    main()
