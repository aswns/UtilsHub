 
# 根据yolo检出的txt 将测试集分为检出和未检出
   # savePath = os.path.join("/home/disk/YC/Projects/yolov8/segment/workspace",project,sorted(os.listdir(os.path.join("/home/disk/YC/Projects/yolov8/segment/workspace",project)))[-1])
    # os.makedirs(os.path.join(savePath,"is_defect"))
    # os.makedirs(os.path.join(savePath,"not_defect"))
    # txts = os.listdir(os.path.join(savePath,"labels"))
    # is_defect = [txt.replace(".txt",".png") for txt in txts]

    # for defect_num,imageName in enumerate(is_defect):
    #     file = os.path.join(savePath,imageName)
    #     shutil.move(file, os.path.join(savePath,"is_defect"))
    
    # all_files = os.listdir(savePath)
    # not_defects = [file for file in all_files if file.endswith(('png'))]

    # for not_defect_num, imageName in enumerate(not_defects):
    #     file = os.path.join(savePath,imageName)
    #     shutil.move(file, os.path.join(savePath,"not_defect"))
    
    # with open(os.path.join(savePath,"result.txt"),"w") as f:
    #     f.write(f"is_defect:{defect_num+1} ; not_defect:{not_defect_num+1}")
    # print(f"is_defect:{defect_num+1} ; not_defect:{not_defect_num+1}")