import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import Utils

#######################
# Processing Functions
#######################
def Otsu(prob_list):
    """
    Otsu algorithm
    :param histgram_list: the histgram of source image, length = 256.
    :return: calculated Otsu threshold.
    """
    max_eta = 0
    otsu_thres = 0
    probability = np.array(prob_list)
    total_mean = np.sum(probability * np.array(range(0,256))) / np.sum(probability)
    total_sigma_square = np.sum(probability * (np.array(range(0,256)) - total_mean) ** 2)
    for index in range(1, 255):
        prob_left = np.sum(probability[0:index])
        mean_left = np.sum(probability[0:index] * np.array(range(0, index))) / (np.sum(probability[0:index]) + 1e-12)
        prob_right = np.sum(probability[index:256])
        mean_right = np.sum(probability[index:256] * np.array(range(index, 256))) / (np.sum(probability[index:256])+1e-12)
        sigma_square = prob_left * prob_right * ((mean_left - mean_right) ** 2)
        eta = sigma_square / total_sigma_square
        if eta > max_eta:
            max_eta = eta
            otsu_thres = index
    return otsu_thres

def Entropy(prob_list):
    """
    Max Entropy segmentation algorithm
    :param prob_list: probabilities of each gray levels, length = 256.
    :return: calculated Entropy threshold
    """
    probability = np.array(prob_list)
    max_entropy = 0
    entropy_thres = 0
    for index in range(1, 255):
        prob_left = probability[0:index] / np.sum(probability[0:index] + 1e-12)
        prob_right = probability[index:256] / np.sum(probability[index:256] + 1e-12)
        entropy_left = -np.sum(prob_left * np.log(prob_left + 1e-12))
        entropy_right = -np.sum(prob_right * np.log(prob_right + 1e-12))
        entropy = entropy_left + entropy_right
        if entropy > max_entropy:
            max_entropy = entropy
            entropy_thres = index
    return entropy_thres

#######################
# Showing Functions
#######################

def Histgram(source_image):
    """
    Calculating histgram of source image
    :param source_image: source gray image
    :return: histgram list and corresponding probabilities list
    """
    histgram_list = 256 * [0]
    test = 0
    for x_index in range(source_image.shape[1]):
        for y_index in range(source_image.shape[0]):
            histgram_list[source_image[y_index, x_index]] += 1
    prob_list = list(np.array(histgram_list) / source_image.size)
    return histgram_list, prob_list

def Threshold(source_image, thres):
    """
    Generating binary image by given threshold
    :param source_image: source gray image
    :param thres: given threshold
    :return: binary image
    """
    binary_image = 255 * np.uint8(source_image < thres)
    return binary_image

#######################
# Debug
#######################
if __name__ == '__main__':
    file_path = "D:\SelfDatas\SJTU\研一\研一下学期\高级医学图像处理\大作业\Homework01\images\yellowlily_small.jpg"
    source_image,_ = Utils.LoadImage(file_path)
    image_size = source_image.size
    histgram_list, prob_list = Histgram(source_image)
    otsu_thres = Otsu(prob_list)
    # entropy_thres = Entropy(prob_list)

    binary_image = Threshold(source_image, otsu_thres)
    cv.imshow('test', binary_image)
    cv.waitKey(0)
    plt.bar(range(0,256),histgram_list)
    plt.show()


