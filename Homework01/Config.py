import numpy as np
import cv2 as cv

DEFAULT_IMAGE = cv.imread('resource/empty.png', flags=0)

PI = 3.1415926
DEFAULT_THRESHOLD = 50


## Filters
MEAN_FILTER = np.array([[1,1,1],[1,1,1],[1,1,1]])
ROBERTS_OPERATOR_DIR01 = np.array([[0,1],[-1,0]])
ROBERTS_OPERATOR_DIR02 = np.array([[1,0],[0,-1]])
PREWITT_OPERATOE_DIR01 = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
PREWITT_OPERATOE_DIR02 = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
SOBEL_OPERATOR_DIR01 = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
SOBEL_OPERATOR_DIR02 = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
MAX_ALPHA = 160

DEFAULT_FILTER_SIZE = 3
DEFAULT_GAUSSIAN_SIGMA = 1.2

## Morph Operation
DEFAULT_SE_SIZE = 5
DEFAULT_SE_WIDTH = 5
DEFAULT_SE_HEIGHT = 5
DEFAULT_SE_ORIGIN = (-1, -1)
DEFAULT_SE = np.ones((DEFAULT_SE_WIDTH, DEFAULT_SE_HEIGHT))
CV_SE_SHAPE = {
    'CV_SHAPE_RECT':0,
    'CV_SHAPE_CROSS':1,
    'CV_SHAPE_ELLIPSE':2,
    'CV_SHAPE_CUSTOM':3
}

MINE_SE_SHAPE = {

}
BASIC_SE = {
    'MORPH_RECT' : lambda shape:np.zeros(shape),
    'MORPH_SQUARE' : np.uint8([[1,1,1],[1,1,1],[1,1,1]]),
    'MORPH_CROSS' : np.uint8([[0,1,0],[1,1,1],[0,1,0]]),
    'MORPH_DISK' : np.uint8([[0,1,1,1,0],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0]])
}

## Morph Function
DEFAULT_DISTANCE_TRANS_MODE = 'CHESSBOARD'
DISTANCE_TRANS_MODE = {
    'CHESSBOARD': BASIC_SE['MORPH_SQUARE'],
    'CITYBLOCK' : BASIC_SE['MORPH_CROSS'],
    # 'EUCLIDEAN' : BASIC_SE['MORPH_DISK']
    'EUCLIDEAN' : [BASIC_SE['MORPH_CROSS'], BASIC_SE['MORPH_SQUARE']]
}
DEFAULT_EDGE_DETECTION_MODE = 'STANDARD'
DEFAULT_GRADIENT_MODE = 'EXTERNAL'
COMBOBOX_MORPH_RECONSTRUCTUTION_ITEMS = {'BW':['Con-Dilation (WB)'],'GRAY':['OBR (Gray)','CBR (Gray)']}