import numpy as np
import cv2

def zoom(image,x1,x2,y1,y2,exp,scale) :
    crop_image = image[x1-10:x2+10,y1-10:y2+10].copy()
    rows,cols = crop_image.shape[:2]
    
    mapy, mapx = np.indices((rows,cols),dtype=np.float32)
    
    mapx = 2*mapx/(cols-1)-1
    mapy = 2*mapy/(rows-1)-1
    
    r,theta = cv2.cartToPolar(mapx, mapy)
    r[r<scale] = r[r<scale]**exp
    
    mapx, mapy = cv2.polarToCart(r,theta)
    
    mapx = ((mapx+1)*cols-1)/2
    mapy = ((mapy+1)*rows-1)/2
    
    distorted = cv2.remap(crop_image,mapx,mapy,cv2.INTER_LINEAR)
    
    zoom_image = image.copy()
    zoom_image[x1-9:x2+9,y1-9:y2+9] = distorted[1:-1,1:-1]
    return zoom_image

def liquify(img, cx1,cy1,x_vec,y_vec,half) :
    cx2, cy2 = cx1-x_vec, cy1-y_vec
    # 대상 영역 좌표와 크기 설정
    x, y, w, h = cx1-half, cy1-half, half*2, half*2
    # 관심 영역 설정
    roi = img[y:y+h, x:x+w].copy()
    out = roi.copy()

    # 관심영역 기준으로 좌표 재 설정
    offset_cx1,offset_cy1 = cx1-x, cy1-y
    offset_cx2,offset_cy2 = cx2-x, cy2-y
    
    # 변환 이전 4개의 삼각형 좌표
    tri1 = [[ (0,0), (w, 0), (offset_cx1, offset_cy1)], # 상,top
            [ [0,0], [0, h], [offset_cx1, offset_cy1]], # 좌,left
            [ [w, 0], [offset_cx1, offset_cy1], [w, h]], # 우, right
            [ [0, h], [offset_cx1, offset_cy1], [w, h]]] # 하, bottom

    # 변환 이후 4개의 삼각형 좌표
    tri2 = [[ [0,0], [w,0], [offset_cx2, offset_cy2]], # 상, top
            [ [0,0], [0, h], [offset_cx2, offset_cy2]], # 좌, left
            [ [w,0], [offset_cx2, offset_cy2], [w, h]], # 우, right
            [ [0,h], [offset_cx2, offset_cy2], [w, h]]] # 하, bottom

    
    for i in range(4):
        # 각각의 삼각형 좌표에 대해 어핀 변환 적용
        matrix = cv2.getAffineTransform( np.float32(tri1[i]), \
                                         np.float32(tri2[i]))
        warped = cv2.warpAffine( roi.copy(), matrix, (w, h), \
            None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        # 삼각형 모양의 마스크 생성
        mask = np.zeros((h, w), dtype = np.uint8)
        cv2.fillConvexPoly(mask, np.int32(tri2[i]), (255,255,255))
        
        # 마스킹 후 합성
        warped = cv2.bitwise_and(warped, warped, mask=mask)
        out = cv2.bitwise_and(out, out, mask=cv2.bitwise_not(mask))
        out = out + warped

    # 관심 영역을 원본 영상에 합성
    img[y:y+h, x:x+w] = out
    return img 

