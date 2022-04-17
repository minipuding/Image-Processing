import numpy as np
import cv2 as cv
import Utils
import Config


#######################
# Processing Functions
#######################
def CheckFilter(filter):
    """
    this function is used to check the form of filter, insuring that:
        - the size is odd number
        - value has normalized
    :param filter: source filter
    :return: checked filter
    """
    ## check normalized
    if np.sum(filter[:]) != 0:
        filter = filter / np.sum(filter[:])
    else:
        filter = filter / (np.sum(abs(filter)) / 2)

    ## check size
    if filter.shape[0] % 2 == 0:
        checked_filter = np.zeros((filter.shape[0] + 1, filter.shape[1] + 1))
        checked_filter[0:filter.shape[0], 0:filter.shape[1]] = filter
        filter = checked_filter
    return filter

def CheckImage(image, mode ='cut'):
    """
    this function is used to check ourput image, insuring that:
        - all of values are between 0 and 255
    :param image: output image
    :return: checked image
    """
    if mode == 'cut':
        image[image[:] > 255] = 255
        image[image[:] < 0] = 0
        image = np.uint8(image)
    elif mode == 'norm':
        image = np.uint8(image / (np.max(image[:]) - np.min(image[:])) * 255)
    return image

def CalcMeanFilter(size):
    return np.ones((size, size))

def CalcGaussianFilter(size, sigma):
    half_size = int((size-1)/2)
    gaussian_filter = np.zeros((size, size))
    x_index, y_index = np.meshgrid(range(-half_size,half_size+1), range(-half_size,half_size+1))
    gaussian_filter = np.around((1 /(2*Config.PI*sigma**2))*np.exp(-(x_index**2+y_index**2)/(2*sigma**2)), 3)
    return gaussian_filter


def Convolution(image, filter, mode ='opencv'):
    """
    do convolution between image and filter
    :param image: source image
    :param filter: a small block like 3x3 or 5x5, note that the size should be odd number
    :return: filtered image
    """
    if mode == 'mine':
        ## preparing
        pad_size = int(filter.shape[0] / 2)
        pad_image = np.pad(image, pad_width=pad_size) # padding
        rows = pad_image.shape[0]
        cols = pad_image.shape[1]
        filter = filter[::-1, ::-1] # overturn
        ## doing convolution
        filtered_image = np.zeros(pad_image.shape)
        for x_index in range(pad_size, cols - pad_size):
            for y_index in range(pad_size, rows - pad_size):
                cropped = pad_image[y_index - pad_size: y_index + pad_size + 1, x_index - pad_size : x_index + pad_size + 1]
                filtered_image[y_index][x_index] = np.sum(cropped * filter)
        filtered_image = filtered_image[pad_size: rows - pad_size, pad_size: cols - pad_size] # depadding
    elif mode == 'opencv':
        filtered_image = cv.filter2D(image, -1, filter)
    return filtered_image

def MedianFiltering(image, filter_size,mode = 'opencv'):
    if mode == 'mine':
        ## preparing
        pad_size = int(filter_size / 2)
        pad_image = np.pad(image, pad_width=pad_size) # padding
        rows = pad_image.shape[0]
        cols = pad_image.shape[1]
        ## doing median filtering
        filtered_image = np.zeros(pad_image.shape)
        for x_index in range(pad_size, cols - pad_size):
            for y_index in range(pad_size, rows - pad_size):
                cropped = pad_image[y_index - pad_size: y_index + pad_size + 1, x_index - pad_size : x_index + pad_size + 1]
                filtered_image[y_index][x_index] = np.median(cropped)
        filtered_image = filtered_image[pad_size: rows - pad_size, pad_size: cols - pad_size] # depadding
    elif mode == 'opencv':
        filtered_image = cv.medianBlur(image, filter_size)

    return filtered_image

#######################
# Debug
#######################
if __name__ == '__main__':
    file_path = "D:\SelfDatas\SJTU\研一\研一下学期\高级医学图像处理\大作业\Homework01\images\yellowlily_small.jpg"
    source_image,_ = Utils.LoadImage(file_path)
    filter = np.array([[-1,0, 1],[-2,0, 2],[-1,0,1]])
    filter = CheckFilter(filter)
    print(filter)
    filtered_image = Convolution(source_image, filter)
    filtered_image = CheckImage(filtered_image)
    cv.imshow('test', filtered_image)
    cv.waitKey(0)
