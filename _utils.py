import cv2, os, shutil
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
    if not os.path.exists(savedir): print(f"{savedir} not exist")
    for dirpath,dirnames,filenames in os.walk(rootdir):
        for dirname in dirnames:
            oldpath = os.path.join(dirpath,dirname)
            new_dirpath = oldpath.replace(rootdir,savedir)
            os.makedirs(new_dirpath)
            print(f"[func_info-copy_dirs]:{new_dirpath} created")
    print("******[func_info-copy_dirs]:copy dirs finished******")
    return 0

def show_dir_tree(root_directory, indent='', _print_file=False):  # 递归
    "显示目录树状图及文件数"
    for item in os.listdir(root_directory):
        item_path = os.path.join(root_directory, item)
        if os.path.isdir(item_path):
            print(f"{indent}|--- {item} : {len(os.listdir(item_path))}")
            show_dir_tree(item_path, indent + '    ')
        elif _print_file:
            print(indent + '|--- ' + item)


class constant:
    IMG_EXTENSION = [".jpg", ".jpeg", ".png", ".bmp"]

if __name__ == "__main__":
    show_dir_tree("data/changxing/datasetV1_cls5")