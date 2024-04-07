import cv2, os
import numpy as np

def cv2_imread(imagePath):
    """chinese path patch of cv2.imread
    """
    return cv2.imdecode(np.fromfile(imagePath,dtype=np.uint8),-1)

def cv2_imwrite(path, image):
    """chinese path patch of cv2.imwrite
    """
    cv2.imencode(os.path.splitext(path)[-1], image)[1].tofile(path)