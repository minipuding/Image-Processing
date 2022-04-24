import numpy as np
import cv2 as cv
import os
import time
import Utils
import Config

def CheckSE(forcalc_se):
    height, width = forcalc_se.shape
    size = np.maximum(height, width)
    forshow_se = -np.ones((size, size))
    if height > width:
        offset = (int((size - width) / 2), 0)
    elif height < width:
        offset = (0, int((size - height) / 2))
    else:
        offset = (0, 0)
    forshow_se[offset[1] : offset[1] + height, offset[0] : offset[0] + width] = forcalc_se
    return forshow_se

#######################
# OpenCV Method
#######################
def cv_getStructureElement(se_type, ksize, origin = (-1, -1), mask = None):
    if se_type == 0:
        structure_element = cv.getStructuringElement(cv.MORPH_RECT, ksize, origin)
    elif se_type == 1:
        structure_element = cv.getStructuringElement(cv.MORPH_CROSS, ksize, origin)
    elif se_type == 2:
        structure_element = cv.getStructuringElement(cv.MORPH_ELLIPSE, ksize, origin)
    elif se_type == 3:
        structure_element = mask
    return structure_element

def cv_Dilation(source_image, structure_element):
    morph_image = np.zeros(source_image.shape)
    morph_image = cv.dilate(source_image, structure_element)
    return morph_image

def cv_Erosion(source_image, structure_element):
    morph_image = np.zeros(source_image.shape)
    morph_image = cv.erode(source_image, structure_element)
    return morph_image

def cv_Open(source_image, structure_element):
    morph_image = np.zeros(source_image.shape)
    morph_image = cv.morphologyEx(source_image, cv.MORPH_OPEN, structure_element)
    return morph_image

def cv_Close(source_image, structure_element):
    morph_image = np.zeros(source_image.shape)
    morph_image = cv.morphologyEx(source_image, cv.MORPH_CLOSE, structure_element)
    return morph_image

#######################
# My Method
#######################
def mine_getStructureElement(se_type, ksize):
    if se_type == 0:
        structure_element = cv.getStructuringElement(cv.MORPH_RECT, ksize)
    elif se_type == 1:
        structure_element = cv.getStructuringElement(cv.MORPH_CROSS, ksize)
    elif se_type == 2:
        structure_element = cv.getStructuringElement(cv.MORPH_ELLIPSE, ksize)
    else:
        return
    return structure_element

def mine_Dilation(source_image, structure_element, origin = (-1,-1)):
    morph_image = np.zeros(source_image.shape)
    image_height = source_image.shape[0]
    image_width = source_image.shape[1]
    if origin == (-1,-1):
        x_offset = int((structure_element.shape[0] - 1) / 2)
        y_offset = int((structure_element.shape[1] - 1) / 2)
    else:
        x_offset = origin[1] # x是横向
        y_offset = origin[0] # y是纵向
    X = np.array(np.where(structure_element==1)[0]) - x_offset
    Y = np.array(np.where(structure_element==1)[1]) - y_offset
    for x,y in zip(list(X), list(Y)):
        if x >= 0 and y >= 0:
            temp_image = np.pad(source_image, ((abs(y), 0), (abs(x), 0)), constant_values = (0, 0))
            temp_image = temp_image[0:image_height, 0:image_width]
        elif x >= 0 and y < 0:
            temp_image = np.pad(source_image, ((0, abs(y)), (abs(x), 0)), constant_values = (0, 0))
            temp_image = temp_image[abs(y):image_height+abs(y), 0:image_width]
        elif x < 0 and y >= 0:
            temp_image = np.pad(source_image, ((abs(y), 0), (0, abs(x))), constant_values = (0, 0))
            temp_image = temp_image[0:image_height, abs(x):image_width+abs(x)]
        elif x < 0 and y < 0:
            temp_image = np.pad(source_image, ((0, abs(y)), (0, abs(x))), constant_values = (0, 0))
            temp_image = temp_image[abs(y):image_height+abs(y), abs(x):image_width+abs(x)]
        morph_image = np.maximum(morph_image, temp_image)

    morph_image = morph_image.astype(np.uint8)
    return morph_image

def mine_Erosion(source_image, structure_element, origin = (-1,-1)):
    source_image = cv.bitwise_not(source_image)
    structure_element = cv.flip(structure_element, -1)
    morph_image = mine_Dilation(source_image, structure_element, origin)
    morph_image = cv.bitwise_not(morph_image)
    return morph_image

def mine_Open(source_image, structure_element, origin = (-1,-1)):
    morph_image = mine_Erosion(source_image, structure_element, origin=(-1, -1))
    morph_image = mine_Dilation(morph_image, structure_element, origin=(-1, -1))
    return morph_image

def mine_Close(source_image, structure_element, origin = (-1,-1)):
    morph_image = mine_Dilation(source_image, structure_element, origin=(-1, -1))
    morph_image = mine_Erosion(morph_image, structure_element, origin=(-1, -1))
    return morph_image

#######################
# Debug
#######################
if __name__ == '__main__':
    file_path = ".\\images\\hand.png"
    source_image, _ = Utils.LoadImage(file_path)
    structure_element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15,15))

    ## test dialation
    # start = time.time()
    # for i in range(5):
    #     morph_image1 = cv_Dilation(source_image, structure_element)
    # end = time.time()
    # print('总共的时间为:', round(end - start, 6),'secs')
    # start = time.time()
    # for i in range(5):
    #     morph_image2 = mine_Dilation(source_image, structure_element)
    # end = time.time()
    # print('总共的时间为:', round(end - start, 6),'secs')
    # print(np.sum(np.abs(morph_image2-morph_image1)[:]))
    # cv.imshow('test', abs(morph_image1-morph_image2))

    ## test erosion
    morph_image = mine_Close(source_image, structure_element)
    cv.imshow('test', morph_image)
    cv.waitKey(0)