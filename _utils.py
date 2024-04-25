import cv2, os, shutil, sys, random, sys, random
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
    """need to touch savedir first

    Args:
        rootdir (_type_): _description_
        savedir (_type_): _description_

    Returns:
        _type_: _description_
    """
    if not os.path.exists(savedir): print(f"{savedir} not exist")
    for dirpath,dirnames,filenames in os.walk(rootdir):
        for dirname in dirnames:
            oldpath = os.path.join(dirpath,dirname)
            new_dirpath = oldpath.replace(rootdir,savedir)
            os.makedirs(new_dirpath,exist_ok=True)
            print(f"[func_info-copy_dirs]:{new_dirpath} created")
    print("******[func_info-copy_dirs]:copy dirs finished******")
    return 0


# def _show_dir_tree(root_directory, indent='', _print_file=False, filenum=0):  # 递归
#     "显示目录树状图及文件数"
#     for item in os.listdir(root_directory):
#         item_path = os.path.join(root_directory, item)
#         if os.path.isdir(item_path):
#             print(f"{indent}|--- {item} : {len(os.listdir(item_path))}")
#             filenum=_show_dir_tree(item_path, indent + '    ',filenum)
#             return filenum
#         elif _print_file:
#             filenum += 1
#             print(indent + '|--- ' + item)

# def show_dir_tree(root):
#     print(f"---{os.path.split(root)[-1]}:{len(os.listdir(root))}")
#     filenum = _show_dir_tree(root, indent='   ', _print_file=False)
#     print(filenum)

def _show_dir_tree(root_directory, indent='', _print_file=False, filenum=0):  
    "显示目录树状图及文件数"
    for item in os.listdir(root_directory):
        item_path = os.path.join(root_directory, item)
        if os.path.isdir(item_path):
            print(f"{indent}|--- {item} : {len(os.listdir(item_path))}")
            filenum = _show_dir_tree(item_path, indent + '    ', _print_file, filenum)
        else:
            filenum += 1
            if _print_file:
                print(indent + '|--- ' + item)
    return filenum

def show_dir_tree(root):
    print(f"|--- {os.path.split(root)[-1]}:{len(os.listdir(root))}")
    filenum = _show_dir_tree(root, indent='   ', _print_file=False)
    print("Total files:", filenum)



def del_samefiles(root, lookup_root):
    """删除同名文件(不区分文件夹)

    Args:
        root (_type_): _description_
        lookup_root (_type_): _description_
    """
    lookup_filenames = []
    for dirpath, dirnames, pathnames in os.walk(lookup_root):
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

def conver_imgForm(root, to_convertForm="bmp"):
    """save root = root +"_"+ to_convertForm

    Args:
        root (_type_): _description_
        to_convert (str, optional): _description_. Defaults to "bmp".
    """
    to_convertForm=to_convertForm.lower()
    if to_convertForm not in ["png", "bmp"]:
        print("error:to_convertForm not in [png, bmp]")
        sys.exit()
    saveroot = root+"_"+ to_convertForm
    os.makedirs(saveroot,exist_ok=True)
    copy_dirs(rootdir=root,savedir=saveroot)
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if os.path.splitext(filename)[-1] not in constant().IMG_EXTENSION:
                continue
            oldpath = os.path.join(dirpath, filename)
            img = cv2_imread(oldpath)
            newpath = os.path.splitext(oldpath.replace(root,saveroot))[0]+"."+to_convertForm
            cv2_imwrite(newpath,img)
            print(f"Saved : {newpath}")

def _rename_recursion(path):
    if os.path.exists(path):  # 存在path则往后加_
        name, ext = os.path.splitext(path)
        new_path = name + "_" +ext
        return _rename_recursion(new_path)
    else:  # 直到不存在 递归 return
        return path

def copy_rename_files(rootdir,savedir):
    """_summary_

    Args:
        root (_type_): _description_
    """
    copy_dirs(rootdir=rootdir,savedir=savedir)

    for dirpath, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            
            new_filename = filename.split("-")[-1]  # *** 重命名规则
            
            old_path = os.path.join(dirpath, filename)
            new_path = os.path.join(dirpath,new_filename)
            
            new_path = new_path.replace(rootdir, savedir)
            new_path = _rename_recursion(new_path) # 防重

            shutil.copy2(old_path, new_path)
            print(f"copy and renamed{new_path}")

    show_dir_tree(savedir)
    


if __name__ == "__main__":
    show_dir_tree(r"data/boe/boe_v1")



    # root = r"E:\dataset\屏显\屏显分类验证\屏显分类基础模型\德普特数据\deputeV2_huaxingV2_cleaned"
    # savepath = root+"_renamed"
    # if os.path.exists(savepath):shutil.rmtree(savepath)
    # copy_rename_files(root,savepath)


    # root = r"E:\dataset\屏显\屏显分类验证\屏显分类基础模型\德普特数据\原始数据0613_datasets_dpt_raiden"
    # lookup_root = r"E:\dataset\屏显\屏显分类验证\屏显分类基础模型\德普特数据\deputeV2_huaxingV2_cleaned_renamed"
    # del_samefiles(root, lookup_root)


    # todir_map = {"NG":          r"E:\dataset\屏显\屏显分类验证\历史数据\天马\天马原始数据\NG",
    #              "OK":          r"E:\dataset\屏显\屏显分类验证\历史数据\天马\天马原始数据\OK",
    #              "scratch_NG":  r"E:\dataset\屏显\屏显分类验证\历史数据\天马\天马原始数据\scratch_NG",
    #              "scratch_OK":  r"E:\dataset\屏显\屏显分类验证\历史数据\天马\天马原始数据\scratch_OK"}

    # fromdir = r"E:\dataset\屏显\屏显分类验证\历史数据\天马\天马AI小图-38614张-画面图\天马小图-0309\缺陷\无划痕defect"
    # todir = todir_map["NG"]

    # fileNames = os.listdir(fromdir)
    # for fileName in fileNames:
    #     filepath = os.path.join(fromdir,fileName)
    #     newpath = os.path.join(todir,fileName)
        
    #     newpath = _rename_recursion(newpath)  # 防止重名
    #     shutil.copy(filepath,newpath)
    #     print(f"Copyed : {newpath}")

 

