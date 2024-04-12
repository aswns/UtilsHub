# test temporary
# import sys; sys.path.append(".")
# from _utils import *

# todel_root = r"E:\dataset\屏显\屏显分类验证\屏显分类基础模型\华星规格确认\4_cls_v5"
# accord_del_root = r"E:\dataset\屏显\屏显分类验证\屏显分类基础模型\长信数据\dataset"
# del_names = []
# for dirpath, dirnames, filenames in os.walk(accord_del_root):
#     for fileName in filenames:
#         del_names.append(fileName)

# for dirpath, dirnames, filenames in os.walk(todel_root):
#     for filename in filenames:
#         if filename in del_names:
#             os.remove(os.path.join(dirpath,filename))
#             print(f"{filename} deleted")
import os
root = r"E:\dataset\屏显\屏显外观IC基板检测验证\0308莱宝缺陷图\1053问题反馈\屏显基板检测测试-偏暗_检测结果图"
for fileName in os.listdir(root):
    name, exp = os.path.splitext(fileName)
    new_name = name.split("-")[0]+exp
    os.rename(os.path.join(root,fileName), os.path.join(root,new_name))
    
