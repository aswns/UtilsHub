import os, random
import shutil
import random
import sys; sys.path.append(".")
from UtilsHub._utils import *


def split_data(inputdir, outputdir, train_rate):
    """Split imgdir to train and val dir by train rate or num

    Args:
        inputdir (str): image dir support [".jpg",".png",".bmp", ".jpeg"]
        outputdir (str): dir_path of splited train and val dir
        train_rate (float or int): train num [>1] or train rate [<=1]
    """
    
    filenames = os.listdir(inputdir)
    filepaths = []
    for filename in filenames:
        if os.path.splitext(filename)[-1] in [".jpg",".png",".bmp", ".jpeg"]:
            filepaths.append(os.path.join(inputdir,filename))

    if train_rate <=1:
        train_num = int(len(filepaths)*train_rate)
    else:
        train_num = train_rate
        
    if train_num > len(filepaths):
        print(f"train num: {train_num} > image num :{len(filepaths)}")
        sys.exit()

    input_dir_name = os.path.split(inputdir)[-1]
    train_dir_name = input_dir_name + "_train_" + str(train_num)
    test_dir_name = input_dir_name + "_test_" + str(len(filepaths)-train_num)
    traindir = os.path.join(outputdir, train_dir_name)
    testdir = os.path.join(outputdir, test_dir_name)

    if os.path.exists(traindir) : shutil.rmtree(traindir)
    if os.path.exists(testdir):shutil.rmtree(testdir)
    os.makedirs(traindir)
    os.makedirs(testdir)

    train_paths = random.sample(filepaths,train_num)
    for i,filepath in enumerate(filepaths):
        if filepath in train_paths:
            shutil.copy2(filepath,traindir)
        else:
            shutil.copy2(filepath,testdir)
    print(f"split finished")

def split_cls_data(input_root,trainValtest_rate=[0.6,0.2,0.2]):
    """input_root : -clses -> output_root: input_root "_cls_clsnum" -train-clses -val-clses -test-clses

    Args:
        input_root (_type_): _description_
        output_root (_type_): _description_
    """

    save_root = input_root + f"_cls{len(os.listdir(input_root))}"
    os.makedirs(save_root, exist_ok=False)

    Sampled_list = {"train":{}, "val":{}, "test":{}}  # {"train":{cls:[paths],}, "val":[]}
    for  clsName in os.listdir(input_root):
        for key in Sampled_list.keys():Sampled_list[key][clsName]=[]
        dirpath = os.path.join(input_root, clsName)
        clsfiles = os.listdir(dirpath)
        clspaths = [os.path.join(dirpath,fileName) for fileName in clsfiles]
        clsNum = len(clspaths)
        train_num, val_num = int(clsNum*trainValtest_rate[0]),int(clsNum*trainValtest_rate[1]) 
        Sampled_list["train"][clsName] = random.sample(clspaths, train_num)
        remain_files = [file for file in clspaths if file not in Sampled_list["train"][clsName]]
        Sampled_list["val"][clsName] = random.sample(remain_files, val_num)
        test_files = [file for file in remain_files if file not in Sampled_list["val"][clsName]]
        Sampled_list["test"][clsName] = test_files
    


    for dirName in Sampled_list.keys():
        new_dirPath =os.path.join(save_root, dirName)  # saveroot-trian -val -test
        for cls in Sampled_list[dirName].keys():
            new_clsPath = os.path.join(new_dirPath,cls)
            os.makedirs(new_clsPath)
            for path in Sampled_list[dirName][cls]:
                shutil.copy2(path, new_clsPath)
                print(f"{path} copyed")


if __name__ == "__main__":
    # inputdir = r"E:\dataset\屏显\屏显分类验证\train_huaxing\guigenei"
    # outputdir = r"E:\dataset\屏显\屏显分类验证\train_huaxing_split\guigenei"
    # split_data(inputdir, outputdir, 506)
    split_cls_data("data/changxing/datasetV1_clean", [0.7,0.3,0])
