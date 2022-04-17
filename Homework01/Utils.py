import numpy as np
import cv2 as cv
import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc
import PyQt5.QtChart as qch
import os
import Config

#######################
# I/O Functions
#######################
def LoadImage(file_path):
    """
    Loading image from given path
    :param file_path: image path
    :return: gray source image
    """
    # source_image = cv.imread(file_path, flags=0)
    source_image = cv.imdecode(np.fromfile(file_path,dtype=np.uint8), 0)
    if  np.logical_and(source_image < 255, source_image > 0).any():
        image_type = 'GRAY'
    else:
        image_type = 'BW'
    return source_image, image_type

def SaveImage(result_image, file_path):
    try:
        # cv.imwrite(file_path, result_image)
        cv.imencode(os.path.splitext(file_path)[-1], result_image)[1].tofile(file_path)
        return True
    except:
        return False

#######################
# Display Functions
#######################
def show_on_graphview(image):
    if image.ndim == 2:
        qimage = qg.QImage(image.data, image.shape[1], image.shape[0], image.shape[1], qg.QImage.Format_Grayscale8)# the forth parameter is 'bytesPerLine'
    elif image.ndim == 3:
        qimage = qg.QImage(image.data, image.shape[1], image.shape[0], image.shape[1]*3, qg.QImage.Format_RGB888)
    # qimage.scaled(image.shape[1], image.shape[0], qc.Qt.KeepAspectRatio, qc.Qt.SmoothTransformation)
    qpixmap = qg.QPixmap.fromImage(qimage)
    qitem = qw.QGraphicsPixmapItem(qpixmap)
    qscene = qw.QGraphicsScene()
    qscene.addItem(qitem)
    return qitem, qscene

def show_on_chartview(data_list, thres, isInit = 'y'):
    qchart_histgram = qch.QChart()
    qbar_sets_histgram = qch.QBarSet('Histgram')
    qbar_sets_histgram.setColor(qg.QColor(0, 0, 0))

    qbar_series_histgram = qch.QBarSeries()
    qbar_series_histgram.setBarWidth(1)

    qpen_threshold = qg.QPen()
    qpen_threshold.setWidth(2)
    qpen_threshold.setStyle(qc.Qt.DashLine)
    qline_series_threshold = qch.QLineSeries(qchart_histgram)
    qline_series_threshold.setPen(qpen_threshold)
    qline_series_threshold.append(thres, 0)
    qline_series_threshold.append(thres, np.max(np.array(data_list)))

    qbar_sets_histgram.append(data_list)
    qbar_series_histgram.append(qbar_sets_histgram)

    # 设置坐标轴
    x_axis = qch.QValueAxis()
    x_axis.setLabelFormat("%d")
    x_axis.setTickCount(9)
    x_axis.setMinorTickCount(0)

    y_axis = qch.QValueAxis()
    y_axis.setLabelFormat("%d")
    y_axis.setTickCount(8)
    y_axis.setMinorTickCount(0)

    if isInit == 'y':
        qchart_histgram.setAnimationOptions(qch.QChart.SeriesAnimations)

    qchart_histgram.addSeries(qbar_series_histgram)
    qchart_histgram.addSeries(qline_series_threshold)
    qchart_histgram.setAxisX(x_axis, qline_series_threshold)
    qchart_histgram.setAxisX(x_axis, qbar_series_histgram)
    qchart_histgram.setAxisY(y_axis, qline_series_threshold)
    qchart_histgram.setAxisY(y_axis, qbar_series_histgram)
    x_axis.setRange(0, 255)  # This code must be put after axis setting
    return qchart_histgram