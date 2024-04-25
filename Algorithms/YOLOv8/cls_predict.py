from re import T
import sys; sys.path.append(".")
from UtilsHub._utils import *
from ultralytics import YOLO
import os


class YOLO_Predictor:
    def load_clsModel(self, modelpath):
        self.model = YOLO(modelpath)

    def classify_dir(self, dirPath, imgsz):
        """_summary_

        Args:
            dirPath (str): _description_
            imgsz (int or Tuple): _description_

        Returns:
            list: [[cls,conf,path], ]
        """
        results = self.model.predict(source=dirPath, 
                                imgsz=imgsz, 
                                device=7,
                                save= False,
                                save_txt = False,
                                save_conf = False,
                                name = "cls")

        cls_results = []  # [[cls,conf,path], ]
        for result in results:
            path = result.path
            top1_cls = result.names[result.probs.top1]
            top1_conf = result.probs.top1conf.cpu().item()
            cls_results.append([top1_cls,top1_conf,path])

        return cls_results

def analysis_clsdirs(only_save_error=False, move_root_error=False):
    # Load a model
    model_path = 'runs/classify/train/screen_adc/base_data_v1_cls6/weights/best0.951.pt'
    rootpath = "data/boe/boe_v1"
    imgsize = 256
    save_root = os.path.join("results", f"{os.path.split(rootpath)[-1]}")


    if os.path.exists(save_root): shutil.rmtree(save_root)
    os.makedirs(save_root)
    copy_dirs(rootpath, save_root)

    clsPaths = []
    for dirpath, dirnames, filenames in os.walk(rootpath):
        for filename in filenames:
            if os.path.splitext(filename)[-1] not in constant().IMG_EXTENSION:
                continue
            if dirpath not in clsPaths:
                clsPaths.append(dirpath)

    predictor = YOLO_Predictor()
    predictor.load_clsModel(modelpath=model_path)
    
    for clsPath in clsPaths:
        clslabel = os.path.split(clsPath)[-1]
        results = predictor.classify_dir(clsPath, imgsz=imgsize)
        for cls,conf,path in results:

            dirname, name = os.path.split(path)
            newname = str(cls)+"_"+str(round(conf,4))+"-"+name
            newpath = os.path.join(dirname, newname).replace(rootpath,save_root)
            if cls != clslabel:  # error
                if move_root_error:
                    shutil.move(path,newpath)  # move  error
                else:
                    shutil.copy(path,newpath)  # copy  error
                print(f"error-{path} : {cls} , {conf}")
            else:  # correct
                if not only_save_error:
                    shutil.copy(path,newpath)  # copy  correct
    show_dir_tree(save_root)


def analysis_guoloujian():
    # rootpath -normal -defect
    # Load a model
    model_path = 'runs/classify/train/screen_adc/dt3_hx2_lb2_cls52/weights/best.pt'
    rootpath = "data/Test_CX_DPT_LB"
    imgsize = 256
    save_root = os.path.join("results", f"{os.path.split(rootpath)[-1]}")
    labelmap = {"defect":["defect","line","point"],"nomal":["nomal", "dirty"]}

    if os.path.exists(save_root): shutil.rmtree(save_root)
    os.makedirs(save_root)
    copy_dirs(rootpath, save_root)

    clsPaths = []
    for dirpath, dirnames, filenames in os.walk(rootpath):
        for filename in filenames:
            if os.path.splitext(filename)[-1] not in constant().IMG_EXTENSION:
                continue
            if dirpath not in clsPaths:
                clsPaths.append(dirpath)

    predictor = YOLO_Predictor()
    predictor.load_clsModel(modelpath=model_path)
    
    for clsPath in clsPaths:
        dirlabel = os.path.split(clsPath)[-1]
        results = predictor.classify_dir(clsPath, imgsz=imgsize)
        for cls,conf,path in results:
            if cls in labelmap["defect"]: bincls="defect"
            else: bincls="normal"
            if bincls != dirlabel:  # dirlable is from dirname
                dirname, name = os.path.split(path)
                newname = str(cls)+"_"+str(round(conf,4))+"-"+name
                newpath = os.path.join(dirname, newname).replace(rootpath,save_root)
                shutil.copy(path,newpath)  # move
                print(f"{path} : {cls} , {conf}")  
    show_dir_tree(save_root)


if __name__ == '__main__':

    analysis_clsdirs()
    #analysis_guoloujian()


    

