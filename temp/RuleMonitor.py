# 华星规则卡控

'''
led 网格大小7x7
'''


import json, os, sys, shutil, cv2
sys.path.append('.')
import UtilsHub.dataprocessor.graphPlotter as myplot
from scipy.spatial.distance import cdist
import numpy as np
from UtilsHub.Algorithms.point_Metrics import point_Metrics
from UtilsHub._utils import *

class Rule:
    def __init__(self) -> None:
        self.ok_dist = []
        self.ng_dist = []

    def is_defect(self, mask_areas, min_dist, max_area=68.23520029336215,count_area=15, ng=None):  # 15
        if max(mask_areas)>max_area:  # 大于max阈值为缺陷
            return True
        areas = [area for area in mask_areas if area>count_area] 
        if len(areas)>1:  # 存在两个及两个以上大于count_area的为缺陷
            if ng==True: self.ng_dist.append(min_dist)
            else: self.ok_dist.append(min_dist)  # record

            # if min_dist<144.864438780425:
            #     return True
            return True
        return False
    
    def is_defect_seg(self, mask_areas, min_dist, max_area=40.375,count_area=0, ng=None):  # 15
        if max(mask_areas)>max_area:  # 大于max阈值为缺陷
            return True
        areas = [area for area in mask_areas if area>count_area] 
        if len(areas)>1:  # 存在两个及两个以上大于count_area的为缺陷
            if ng==True: self.ng_dist.append(min_dist)
            else: self.ok_dist.append(min_dist)  # record

            # if min_dist<144.864438780425:
            #     return True
            return True
        return False

def save_result(savedir, yoloresultpath,sourcedir,mask_areas, mindist):
    imgName = os.path.split(yoloresultpath)[-1]
    source_imgpath = os.path.join(sourcedir, imgName)
    result_img, source_img = cv2_imread(yoloresultpath), cv2_imread(source_imgpath)
    areas = [round(area, 2) for area in mask_areas]
    if len(areas)>1:mindist= round(mindist, 2)
    else: mindist = None
    concat_img = np.concatenate((result_img,source_img), axis=1)
    cv2.putText(concat_img,"area:"+str(areas)+"  mindist:"+str(mindist),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),1)
    cv2_imwrite(os.path.join(savedir,imgName),concat_img)

def plot_segarea_histogram():
    with open("./result/data_guizewai0.2_box.json", 'r') as f:
        data_ng = json.load(f)
    with open("./result/data_guizenei0.2_box.json", 'r') as f:
        data_ok = json.load(f)


    ok_mask_areas, ng_mask_areas = [], []

    correct, guojian, loujian = [], [],[]
    rule = Rule()
    for path in data_ok.keys():
        mask_areas = data_ok[path]["mask_areas"]
        masks_xys = data_ok[path]["mask_xys"]

        if len(mask_areas)==0:
            #print(f"未检出：{path}")
            continue
    
        centers = []
        for mask_xys in masks_xys:
            if mask_xys:
                centers.append(point_Metrics.center_point(mask_xys)) 
        min_dist = point_Metrics.min_pair_dist(centers)
        
        if len(mask_areas)<=1:
            ok_mask_areas.append(max(mask_areas))
        if rule.is_defect_seg(mask_areas,min_dist,ng=False):
            print(f"规则内->规则外: {path},area {mask_areas}, min_dist {min_dist}")
            guojian.append([path, mask_areas, min_dist])
        else:
            correct.append([path, mask_areas, min_dist])
        



    for path in data_ng.keys():
        mask_areas = data_ng[path]["mask_areas"]
        masks_xys = data_ng[path]["mask_xys"]
        if len(mask_areas)==0:
            #print(f"未检出：{path}")
            continue
        
        centers = []

        for mask_xys in masks_xys:
            if mask_xys:
                centers.append(point_Metrics.center_point(mask_xys)) 
        min_dist = point_Metrics.min_pair_dist(centers)
        
        mask_areas = [area if area<160 else 160 for area in mask_areas]  # for PLOT
        if len(mask_areas)<=1:
            ng_mask_areas.append(max(mask_areas))

        if not rule.is_defect_seg(mask_areas,min_dist, ng=True):
            print(f"规则外->规则内: {path},area {mask_areas}, mindist {min_dist}")
            loujian.append([path, mask_areas, min_dist])
        else:
            correct.append([path, mask_areas, min_dist])
    
    print(f"过检：{len(guojian)}; 漏检：{len(loujian)}")

    auto_maxArea_th = sorted(ok_mask_areas + ng_mask_areas)[len(ok_mask_areas)]
    print(f"auto_maxArea_th : {auto_maxArea_th}")

    ok_dist, ng_dist = rule.ok_dist, rule.ng_dist
    auto_mindist_th = sorted(ok_dist + ng_dist)[len(ng_dist)]+0.0001
    print(f"auto_mindist_th : {auto_mindist_th}")


    myplot.drawHistogram(ok_mask_areas,ng_mask_areas, "result/seg_histogram0.2.jpg")
    # myplot.drawHistogram(ok_mask_areas, ng_mask_areas)
    
    save_guojian_dir, save_loujian_dir, correct_path = "result/seg_guojian", "result/seg_loujian", "result/seg_correct"
    if os.path.exists(save_guojian_dir):shutil.rmtree(save_guojian_dir)
    if os.path.exists(save_loujian_dir):shutil.rmtree(save_loujian_dir)
    if os.path.exists(correct_path):shutil.rmtree(correct_path)

    os.makedirs(save_guojian_dir)
    os.makedirs(save_loujian_dir)
    os.makedirs(correct_path)

    for yoloresult_path, mask_areas, min_dist in loujian:
        save_result(savedir=save_loujian_dir, yoloresultpath=yoloresult_path, sourcedir="data/huaxing/jiangeandguigewai_test_200", mask_areas=mask_areas,mindist=min_dist)
    for yoloresult_path,mask_areas, min_dist in guojian:
        save_result(savedir=save_guojian_dir, yoloresultpath=yoloresult_path, sourcedir="data/huaxing/guigenei_test_200", mask_areas=mask_areas,mindist=min_dist)
    for yoloresult_path,mask_areas, min_dist in correct:
        if "guigewai" in os.path.split(yoloresult_path)[-1]: sourcedir = "data/huaxing/jiangeandguigewai_test_200"
        else: sourcedir = "data/huaxing/guigenei_test_200"
        save_result(savedir=correct_path, yoloresultpath=yoloresult_path, sourcedir=sourcedir, mask_areas=mask_areas,mindist=min_dist)
    print("finished")

def test():
    with open("./result/data_guizewai.json", 'r') as f:
        data_ng = json.load(f)
    with open("./result/data_guizenei.json", 'r') as f:
        data_ok = json.load(f)

    path_guojian = "result/guige-面积50num2/过检"
    path_loujian = "result/guige-面积50num2/漏检"
    shutil.rmtree(path_guojian)
    shutil.rmtree(path_loujian)
    os.makedirs(path_guojian, exist_ok=True)
    os.makedirs(path_loujian, exist_ok=True)

    num, area_th = 1, 50
    ok_mask_areas, ng_mask_areas = [], []
    for path in data_ok.keys():
        mask_areas = data_ok[path]["mask_areas"]
        areas = []
        for area in mask_areas:
            if area>=area_th:
                areas.append(area)
        if len(areas)>=1:  # 存在规格外过检
            print(path)
            shutil.copy(path, os.path.join(path_guojian,f"过检-"+os.path.split(path)[-1]))
        ok_mask_areas.extend(areas)

    for path in data_ng.keys():
        mask_areas = data_ng[path]["mask_areas"]
        areas = [area for area in mask_areas if area>=area_th]  # 小于area_th为规格内，忽略
        if len(areas)==0:  #不存在规格外，漏检
            shutil.copy(path, os.path.join(path_loujian,f"漏检-"+os.path.split(path)[-1]))
        #ng_mask_areas.extend(areas)


def plot_boxarea_histogram():
    with open("./result/data_guizewai0.2_box.json", 'r') as f:
        data_ng = json.load(f)
    with open("./result/data_guizenei0.2_box.json", 'r') as f:
        data_ok = json.load(f)


    ok_mask_areas, ng_mask_areas = [], []

    correct, guojian, loujian = [], [],[]
    rule = Rule()
    for path in data_ok.keys():
        mask_areas = data_ok[path]["box_area"]
        masks_xys = data_ok[path]["mask_xys"]

        if len(mask_areas)==0:
            #print(f"未检出：{path}")
            continue
    
        centers = []
        for mask_xys in masks_xys:
            if mask_xys:
                centers.append(point_Metrics.center_point(mask_xys)) 
        min_dist = point_Metrics.min_pair_dist(centers)
        
        if len(mask_areas)<=1:
            ok_mask_areas.append(max(mask_areas))
        if rule.is_defect(mask_areas,min_dist,ng=False):
            print(f"规则内->规则外: {path},area {mask_areas}, min_dist {min_dist}")
            guojian.append([path, mask_areas, min_dist])
        else:
            correct.append([path, mask_areas, min_dist])
        



    for path in data_ng.keys():
        mask_areas = data_ng[path]["box_area"]
        masks_xys = data_ng[path]["mask_xys"]
        if len(mask_areas)==0:
            #print(f"未检出：{path}")
            continue
        
        centers = []

        for mask_xys in masks_xys:
            if mask_xys:
                centers.append(point_Metrics.center_point(mask_xys)) 
        min_dist = point_Metrics.min_pair_dist(centers)
        
        mask_areas = [area if area<200 else 200 for area in mask_areas]  # for PLOT
        if len(mask_areas)<=1:
            ng_mask_areas.append(max(mask_areas))

        if not rule.is_defect(mask_areas,min_dist, ng=True):
            print(f"规则外->规则内: {path},area {mask_areas}, mindist {min_dist}")
            loujian.append([path, mask_areas, min_dist])
        else:
            correct.append([path, mask_areas, min_dist])
    
    print(f"过检：{len(guojian)}; 漏检：{len(loujian)}")

    auto_maxArea_th = sorted(ok_mask_areas + ng_mask_areas)[len(ok_mask_areas)]
    print(f"auto_maxArea_th : {auto_maxArea_th}")

    ok_dist, ng_dist = rule.ok_dist, rule.ng_dist
    auto_mindist_th = sorted(ok_dist + ng_dist)[len(ng_dist)]+0.0001
    print(f"auto_mindist_th : {auto_mindist_th}")


    myplot.drawHistogram(ok_mask_areas,ng_mask_areas, "result/box_histogram0.2.jpg")
    # myplot.drawHistogram(ok_mask_areas, ng_mask_areas)
    
    save_guojian_dir, save_loujian_dir, correct_path = "result/guojian", "result/loujian", "result/correct"
    if os.path.exists(save_guojian_dir):shutil.rmtree(save_guojian_dir)
    if os.path.exists(save_loujian_dir):shutil.rmtree(save_loujian_dir)
    if os.path.exists(correct_path):shutil.rmtree(correct_path)

    os.makedirs(save_guojian_dir)
    os.makedirs(save_loujian_dir)
    os.makedirs(correct_path)

    for yoloresult_path, mask_areas, min_dist in loujian:
        save_result(savedir=save_loujian_dir, yoloresultpath=yoloresult_path, sourcedir="data/huaxing/jiangeandguigewai_test_200", mask_areas=mask_areas,mindist=min_dist)
    for yoloresult_path,mask_areas, min_dist in guojian:
        save_result(savedir=save_guojian_dir, yoloresultpath=yoloresult_path, sourcedir="data/huaxing/guigenei_test_200", mask_areas=mask_areas,mindist=min_dist)
    for yoloresult_path,mask_areas, min_dist in correct:
        if "guigewai" in os.path.split(yoloresult_path)[-1]: sourcedir = "data/huaxing/jiangeandguigewai_test_200"
        else: sourcedir = "data/huaxing/guigenei_test_200"
        save_result(savedir=correct_path, yoloresultpath=yoloresult_path, sourcedir=sourcedir, mask_areas=mask_areas,mindist=min_dist)
    print("finished")



if __name__=="__main__":
    

    # plot_boxarea_histogram()
    plot_segarea_histogram()
