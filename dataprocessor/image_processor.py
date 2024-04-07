import cv2
import os, shutil, numpy

def lanczos(image,new_w_h):
    """ quality of image upsampling :
         INTER_LANCZOS4>INTER_LINEAR(双线性)>INTER_NEAREST
    Args:
        image : bgr
    """

    new_image = cv2.resize(image, new_w_h, interpolation=cv2.INTER_LANCZOS4)
    return new_image









if __name__ == "__main__":
    inputdir = r"E:\dataset\屏显\屏显分类验证\train_huaxing_split\guigenei"
    outputdir = ""
    for dirpath, dirnames, filenames in os.walk(inputdir):
        for filename in filenames:
            if os.path.splitext(filename)[-1] in [".jpg", ".png", ".bmp", ".jpeg"]:
                imagePath = os.path.join(dirpath, filename)
                newdirpath = dirpath + "_lanczos512"
                if not os.path.exists(newdirpath): os.makedirs(newdirpath)
                image = cv2.imdecode(numpy.fromfile(imagePath,dtype=numpy.uint8),-1)
                new_image = lanczos(image, (512, 512))
                cv2.imencode(os.path.splitext(filename)[-1], new_image)[1].tofile(os.path.join(newdirpath,filename))
                print(f"{filename} resized and saved")

