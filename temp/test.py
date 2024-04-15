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
# import os
# root = r"E:\dataset\屏显\屏显外观IC基板检测验证\0308莱宝缺陷图\1053问题反馈\屏显基板检测测试-偏暗_检测结果图"
# for fileName in os.listdir(root):
#     name, exp = os.path.splitext(fileName)
#     new_name = name.split("-")[0]+exp
#     os.rename(os.path.join(root,fileName), os.path.join(root,new_name))

import os

def recursion_count(root_directory, indent='', _print_file=False):
    for item in os.listdir(root_directory):
        item_path = os.path.join(root_directory, item)
        if os.path.isdir(item_path):
            print(f"{indent}|--- {item} (文件数: {len(os.listdir(item_path))})")
            recursion_count(item_path, indent + '    ')
        elif _print_file:
            print(indent + '|--- ' + item)

# 示例用法
root_directory = 'data/changxing'
print(root_directory)
display_directory_tree_with_file_count(root_directory)

    
