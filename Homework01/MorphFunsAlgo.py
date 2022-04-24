import numpy as np
import cv2 as cv
import time

import MorphOperAlgo
import Config
import Utils

#######################
# Binary Image Morph Functions
#######################
def DistanceTrans(source_image, mode = 'CHESSBOARD'):
    """
    distance transform algorithm
    :param source_image: input source image
    :param mode: distance mode
                'CHESSBOARD' :
    :return:
    """
    temp_source_image = np.copy(source_image)
    temp_source_image[temp_source_image[:] > 0] = 1
    distance_trans_image = np.copy(temp_source_image)
    structure_element = Config.DISTANCE_TRANS_MODE[mode]
    if mode is not 'EUCLIDEAN':
        while temp_source_image.any() != 0:
            temp_source_image = MorphOperAlgo.mine_Erosion(temp_source_image, structure_element)
            distance_trans_image += temp_source_image
    else:
        temp_count = 0
        while temp_source_image.any() != 0:
            temp_source_image = MorphOperAlgo.mine_Erosion(temp_source_image, structure_element[int(temp_count % 2)])
            distance_trans_image += temp_source_image
            temp_count += 1
    distance_trans_image = np.uint8(distance_trans_image)
    distance_trans_image = np.uint8(distance_trans_image / (np.max(distance_trans_image[:]) - np.min(distance_trans_image[:])) * 255)
    return distance_trans_image

def Skeleton(source_image, mode = 'CITYBLOCK', is_show_animation = False):
    temp_souece_image = np.copy(source_image)
    temp_souece_image[temp_souece_image[:] > 0] = 1
    skeleton_image = np.zeros(temp_souece_image.shape)
    structure_element = Config.DISTANCE_TRANS_MODE[mode]
    SiF = []
    if mode is not 'EUCLIDEAN':
        while temp_souece_image.any() != 0:
            temp_souece_image = MorphOperAlgo.cv_Erosion(temp_souece_image, structure_element)
            skeleton_image = np.logical_or(skeleton_image,temp_souece_image - MorphOperAlgo.cv_Open(temp_souece_image, structure_element))
            SiF += [np.where(temp_souece_image > 0)]
            if is_show_animation == True:
                skeleton_image = np.uint8(skeleton_image)
                skeleton_image = np.uint8(
                    skeleton_image / (np.max(skeleton_image[:]) - np.min(skeleton_image[:])) * 255)
                cv.imshow('Animation', skeleton_image)
                cv.waitKey(Config.ANIMATION_INTER_TIME)
    else:
        temp_count = 0
        while temp_souece_image.any() != 0:
            temp_souece_image = MorphOperAlgo.cv_Erosion(temp_souece_image, structure_element[int(temp_count % 2)])
            skeleton_image =np.logical_or(skeleton_image,temp_souece_image - MorphOperAlgo.cv_Open(temp_souece_image, structure_element[int(temp_count % 2)]))
            SiF += [np.where(temp_souece_image > 0)]
            temp_count += 1
            if is_show_animation == True:
                skeleton_image = np.uint8(skeleton_image)
                skeleton_image = np.uint8(
                    skeleton_image / (np.max(skeleton_image[:]) - np.min(skeleton_image[:])) * 255)
                cv.imshow('Animation', skeleton_image)
                cv.waitKey(Config.ANIMATION_INTER_TIME)
    skeleton_image = np.uint8(skeleton_image)
    skeleton_image = np.uint8(skeleton_image / (np.max(skeleton_image[:]) - np.min(skeleton_image[:])) * 255)
    return skeleton_image, SiF

def SkeletonReconstrctution(SiF, image_shape, mode = 'CITYBLOCK', is_show_animation = False):
    recons_image = np.zeros(image_shape)
    structure_element = Config.DISTANCE_TRANS_MODE[mode]
    if mode is not 'EUCLIDEAN':
        for sif in SiF:
            temp_image = np.zeros(image_shape)
            temp_image[sif] = 1
            recons_image = np.logical_or(recons_image, MorphOperAlgo.cv_Dilation(temp_image, structure_element))
            if is_show_animation == True:
                recons_image = np.uint8(recons_image)
                recons_image = np.uint8(recons_image / (np.max(recons_image[:]) - np.min(recons_image[:])) * 255)
                cv.imshow('Animation', recons_image)
                cv.waitKey(Config.ANIMATION_INTER_TIME)
    else:
        temp_count = 0
        for sif in SiF:
            temp_image = np.zeros(image_shape)
            temp_image[sif] = 1
            recons_image = np.logical_or(recons_image, MorphOperAlgo.cv_Dilation(temp_image, structure_element[int(temp_count % 2)]))
            temp_count += 1
            if is_show_animation == True:
                recons_image = np.uint8(recons_image)
                recons_image = np.uint8(recons_image / (np.max(recons_image[:]) - np.min(recons_image[:])) * 255)
                cv.imshow('Animation', recons_image)
                cv.waitKey(Config.ANIMATION_INTER_TIME)
    recons_image = np.uint8(recons_image)
    recons_image = np.uint8(recons_image / (np.max(recons_image[:]) - np.min(recons_image[:])) * 255)
    return recons_image

def EdgeDetection(source_image, structure_element = Config.BASIC_SE['MORPH_SQUARE'], mode = 'STANDARD'):
    edge_image = np.zeros(source_image.shape)
    if mode == 'STANDARD':
        edge_image = MorphOperAlgo.mine_Dilation(source_image, structure_element)\
                     - MorphOperAlgo.mine_Erosion(source_image, structure_element)
    elif mode == 'EXTERNAL':
        edge_image = MorphOperAlgo.mine_Dilation(source_image, structure_element) - source_image
    elif mode == 'INTERNAL':
        edge_image = source_image - MorphOperAlgo.mine_Erosion(source_image, structure_element)
    return edge_image

def ConditionalDilation(mask, marker, mode = 'MORPH_CROSS', is_show_animation = False):
    con_dilation_image = np.zeros(mask.shape)
    element_struction = Config.BASIC_SE[mode]
    count = 0
    while 1:
        con_dilation_image = np.logical_and(mask, MorphOperAlgo.cv_Dilation(marker, element_struction))
        if (con_dilation_image == np.array(marker, dtype='bool')).all() == True:
            break
        marker = np.uint8(con_dilation_image * 255)
        if is_show_animation == True:
            cv.imshow('Animation', marker)
            cv.waitKey(Config.ANIMATION_INTER_TIME)
    return np.uint8(con_dilation_image * 255)

#######################
# Grayscale Image Morph Functions
#######################
def Gradient(source_image, structure_element=Config.BASIC_SE['MORPH_SQUARE'], mode = 'EXTERNAL'):
    gradient_image = np.zeros(source_image.shape)
    if mode == 'EXTERNAL':
        gradient_image = np.uint8((MorphOperAlgo.mine_Dilation(source_image, structure_element) * 1. - source_image * 1.) / 2)
    elif mode == 'INTERNAL':
        gradient_image = np.uint8((source_image * 1. - MorphOperAlgo.mine_Erosion(source_image, structure_element) * 1.) / 2)
    gradient_image = np.uint8(gradient_image / (np.max(gradient_image[:]) - np.min(gradient_image[:])) * 255)
    return gradient_image


def OCBR(source_image, se_size = 10, mode = 'OBR', is_show_animation = False):
    structure_element = Utils.generateDiskSE(se_size)
    if mode == 'OBR':
        marker = cv.erode(source_image, structure_element)
        marker = cv.dilate(marker, structure_element)
    elif mode == 'CBR':
        marker = cv.dilate(source_image, structure_element)
        marker = cv.erode(marker, structure_element)
    ocbr_image = GrayscaleReconstruction(source_image, marker, mode, is_show_animation=is_show_animation)
    return ocbr_image


def GrayscaleReconstruction(source_image, marker,
                            mode = 'OBR',
                            structure_element = Config.BASIC_SE['MORPH_SQUARE'],
                            is_show_animation = False):
    while 1:
        if mode == 'OBR':
            temp_marker = cv.dilate(marker, structure_element)
            temp_marker = np.minimum(source_image, temp_marker)
        elif mode == 'CBR':
            temp_marker = cv.erode(marker, structure_element)
            temp_marker = np.maximum(source_image, temp_marker)
        if (temp_marker == marker).all() == True:
            break
        marker = temp_marker

        # show animation
        if is_show_animation == True:
            cv.imshow('Animation', marker)
            cv.waitKey(Config.ANIMATION_INTER_TIME)
    return marker

if __name__ == '__main__':
    file_path = ".\\images\\US.png"
    source_image,_ = Utils.LoadImage(file_path)
    # source_image = np.uint8(np.ones((200,300)) * 255)
    # source_image = np.pad(source_image, ((100,100),(100,100)))
    # distance transform
    # start = time.time()
    # distance_trans_image = DistanceTrans(source_image)
    # distance_trans_image = np.uint8(distance_trans_image / (np.max(distance_trans_image[:]) - np.min(distance_trans_image[:])) * 255)
    # end = time.time()
    # print('总共的时间为:', round(end - start, 6), 'secs')

    # skeleton and reconstruction
    # start = time.time()
    # skeleton_image, SiF = Skeleton(source_image,'CITYBLOCK')
    # recons_image = SkeletonReconstrctution(SiF, skeleton_image.shape, 'CITYBLOCK')
    # end = time.time()
    # print('总共的时间为:', round(end - start, 6), 'secs')

    # edge detection
    # edge_image = EdgeDetection(source_image, Config.BASIC_SE['MORPH_SQUARE'], mode='INTERNAL')

    # Conditional Dilation
    # mask = np.zeros(source_image.shape)
    # mask[120, 128] = 255
    # con_dilation_image = ConditionalDilation(source_image, mask)

    # OBR & CBR
    cbr_image = OCBR(source_image, 10)

    cv.imshow('test', cbr_image)
    cv.waitKey(0)