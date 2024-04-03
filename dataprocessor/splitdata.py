import os
import shutil
import random
from tqdm import tqdm
import sys

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
    for i,filepath in tqdm(enumerate(filepaths)):
        if filepath in train_paths:
            shutil.copy2(filepath,traindir)
        else:
            shutil.copy2(filepath,testdir)
    print(f"split finished")

if __name__ == "__main__":
    inputdir = r"E:\dataset\屏显\屏显分类验证\train_huaxing\guigenei"
    outputdir = r"E:\dataset\屏显\屏显分类验证\train_huaxing_split\guigenei"
    split_data(inputdir, outputdir, 506)

