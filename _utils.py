import cv2, os, shutil, sys, random
import numpy as np


class constant:
    IMG_EXTENSION = [".jpg", ".jpeg", ".png", ".bmp"]


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


def del_samefiles(root, lookup_root):
    """删除同名文件

    Args:
        root (_type_): _description_
        lookup_root (_type_): _description_
    """
    lookup_filenames = []
    for dirpath,dirnames,pathnames in os.walk(lookup_root):
        for pathname in pathnames:
            lookup_filenames.append(pathname)

    for dirpath,dirnames,pathnames in os.walk(root):
        for pathname in pathnames:
            if pathname in lookup_filenames:
                os.remove(os.path.join(dirpath, pathname))
                print(f"removed {pathname}")

def Sample_files(fromdir, todir, num):
    os.makedirs(todir, exist_ok=True)
    if num > len(os.listdir(fromdir)):
        print(f"{fromdir} num < {num}")
        sys.exit()
    frompaths = []
    for dirpath, dirnames, pathnames in os.walk(fromdir):
        for pathname in pathnames:
            frompaths.append(os.path.join(dirpath, pathname))
    sampledpaths = random.sample(frompaths, num)
    for path in sampledpaths:
        shutil.move(path, os.path.join(todir,os.path.split(path)[-1]))
        print(f"{path} copyed")
    


if __name__ == "__main__":
    # fromdir= r"E:\dataset\屏显\屏显分类验证\屏显分类基础模型\长信数据\changxin_remain\jiangeandguigewai_spot"
    # todir = r"E:\dataset\屏显\屏显分类验证\屏显分类基础模型\长信数据\test2000\defect"
    # Sample_files(fromdir, todir, 100)
    show_dir_tree("data/changxin/datasetV2_cls5")