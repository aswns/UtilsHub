import cv2, os
import numpy as np

def cv2_imread(imagePath):
    """chinese path patch of cv2.imread
    """
    return cv2.imdecode(np.fromfile(imagePath,dtype=np.uint8),-1)

def cv2_imwrite(path, image):
    """chinese path patch of cv2.imwrite
    """
    cv2.imencode(os.path.splitext(path)[-1], image)[1].tofile(path)

def copy_dirs(rootdir, savedir):
    os.makedirs(savedir,exist_ok=False) if not os.path.exists(savedir) else print(f"savedir existed")
    for dirpath,dirnames,filenames in os.walk(rootdir):
        for dirname in dirnames:
            oldpath = os.path.join(dirpath,dirname)
            new_dirpath = oldpath.replace(rootdir,savedir)
            os.makedirs(new_dirpath)
            print(f"{new_dirpath} created")
    print("******copy dirs finished******")
    return 0



class constant:
    IMG_EXTENSION = [".jpg", ".jpeg", ".png", ".bmp"]

if __name__ == "__main__":
    rootdir = "E:\dataset\屏显\屏显分类验证\天马AI小图-38614张"
    savedir = "E:\dataset\屏显\屏显分类验证\天马AI小图-38614张_vis"
    copy_dirs(rootdir=rootdir,savedir=savedir)