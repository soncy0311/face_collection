import sys
import os
import numpy as np
import cv2
import dlib
from glob import glob
from tqdm import tqdm

from utils.tools import zoom, liquify
from utils.config import CFG

def face_collect(path:str,config:CFG) :
    '''
    path: 이미지가 저장된 경로
        ex) path = "./data/001_origin.jpg"
    config: 성형 비율 파라미터 값
    '''
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')

    ALL = list(range(0, 68))
    RIGHT_EYEBROW = list(range(17, 22)) 
    LEFT_EYEBROW = list(range(22, 27)) 
    RIGHT_EYE = list(range(36, 42)) 
    LEFT_EYE = list(range(42, 48)) 
    NOSE = list(range(27, 36)) 
    MOUTH_OUTLINE = list(range(48, 61)) 
    MOUTH_INNER = list(range(61, 68))
    JAWLINE = list(range(0, 17))

    index = ALL

    image = cv2.imread(path)

    result = image.copy()
    img_gray = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)

    dets = detector(img_gray)

    for face in dets :
        shape = predictor(result, face)

        list_points = []
        for p in shape.parts() :
            list_points.append([p.x,p.y])

        list_points = np.array(list_points)

    # Change Right Eye
    y1,x1 = np.min(list_points[RIGHT_EYE],axis=0)
    y2,x2 = np.max(list_points[RIGHT_EYE],axis=0)
    result_right = zoom(result,x1,x2,y1,y2,exp=config.eye_ratio,scale=config.eye_scale)

    # Change Left Eye
    y1,x1 = np.min(list_points[LEFT_EYE],axis=0)
    y2,x2 = np.max(list_points[LEFT_EYE],axis=0)
    result_eye = zoom(result_right,x1,x2,y1,y2,exp=config.eye_ratio,scale=config.eye_scale)

    # Change nose
    x1,_ = np.min(list_points[NOSE],axis=0)
    x2,y = np.max(list_points[NOSE],axis=0)
    result_left_nose = liquify(result_eye,x1,y,-config.left_nose,0,config.nose_ratio)
    result = liquify(result_left_nose,x2,y,config.right_nose,0,config.nose_ratio)
    
    return result

if __name__ == "__main__" :
    config = CFG()

    current_path = os.getcwd()
    os.makedirs(current_path+"/result",exist_ok=True)

    image_path = [current_path+"/data/"+file for file in os.listdir(current_path+"/data/")
                    if file.endswith(".jpg") or file.endswith(".png")]
    result_path = current_path+"/result/"

    for path in tqdm(image_path) :
        image_name = path.split("/")[-1]
        result = face_collect(path,config)
        cv2.imwrite(result_path+image_name,result)