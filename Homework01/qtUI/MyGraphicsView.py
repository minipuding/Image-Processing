import numpy as np
import cv2 as cv
import PyQt5
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import Config
import Utils

class MyGraphicsView(qw.QGraphicsView):
    pressed_signal = qc.pyqtSignal()
    def __init__(self, *__args):
        super().__init__()
        self.image_width = 0
        self.image_height = 0
        self.mask = None
        self.marker = None
        self.morph_funs_marker = None
        self.qitem_morph_funs_marker = None
        self.is_setting_marker = False
        self.marker_shape_type = 'DISK'
        self.marker_shape_disk_size = 2
        self.marker_shape = Config.DEFAULT_MARKER_SHAPE
        self.moveX = 0
        self.moveY = 0
        self.pressedX = 0
        self.pressedY = 0

        self.setMouseTracking(True)
        # self.myscene = self.scene()

    def _update_marker_graphics(self):
        fusion_image = cv.addWeighted(cv.cvtColor(self.mask, cv.COLOR_GRAY2RGB), 0.8, self.marker, 0.8, 0)
        self.qitem_morph_funs_marker, qscene_morph_funs_marker = Utils.show_on_graphview(fusion_image)
        self.setScene(qscene_morph_funs_marker)
        self.fitInView(self.qitem_morph_funs_marker, qc.Qt.IgnoreAspectRatio)

    def _update_marker(self, color_channel = 1):
        if self.marker_shape_type == 'DISK':
            self.marker = np.zeros((self.image_height + 2 * self.marker_shape_disk_size,
                                    self.image_width  + 2 * self.marker_shape_disk_size, 3))
            self.marker[self.moveY : self.moveY + 2 * self.marker_shape_disk_size + 1,
                        self.moveX : self.moveX + 2 * self.marker_shape_disk_size + 1, color_channel] = self.marker_shape * 255
            self.marker = self.marker[self.marker_shape_disk_size : self.image_height + self.marker_shape_disk_size,
                                      self.marker_shape_disk_size : self.image_width  + self.marker_shape_disk_size]
        elif self.marker_shape_type == 'V_LINE':
            self.marker = np.zeros((self.image_height, self.image_width, 3))
            self.marker[:, self.moveX, color_channel] = 255
        elif self.marker_shape_type == 'H_LINE':
            self.marker = np.zeros((self.image_height, self.image_width, 3))
            self.marker[self.moveY, :, color_channel] = 255
        self.marker = np.uint8(self.marker)

    def mousePressEvent(self, event):
        if self.is_setting_marker == False:
            return
        self.pressedX = int(event.x() / (self.width() -2) * self.image_width)
        self.pressedY = int(event.y() / (self.height()-2) * self.image_height)
        self._update_marker(color_channel=0)
        self._update_marker_graphics()

        self.morph_funs_marker = cv.cvtColor(self.marker, cv.COLOR_RGB2GRAY)
        self.morph_funs_marker = np.uint8((self.morph_funs_marker > 0)*255)
        self.is_setting_marker = False
        self.pressed_signal.emit()

    def mouseMoveEvent(self, event):
        if self.is_setting_marker == False:
            return
        self.moveX = int(event.x() / (self.width() -2) * self.image_width)
        self.moveY = int(event.y() / (self.height()-2) * self.image_height)
        self._update_marker()
        self._update_marker_graphics()

        # print(self.moveX, self.moveY)
        # cv.imshow('test', self.marker)
        # cv.waitKey(1)

    def wheelEvent(self, event):
        if self.is_setting_marker == False:
            return
        if self.marker_shape_type == 'DISK':
            if event.angleDelta().y() > 0:
                self.marker_shape_disk_size += 1
                self.marker_shape = Utils.generateDiskSE(self.marker_shape_disk_size)
            elif event.angleDelta().y() < 0 and self.marker_shape_disk_size >= 1:
                self.marker_shape_disk_size -= 1
                self.marker_shape = Utils.generateDiskSE(self.marker_shape_disk_size)
        self._update_marker(color_channel=1)
        self._update_marker_graphics()
            # print(event.angleDelta().y())