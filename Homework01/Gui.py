import numpy as np
import PyQt5
import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc
import PyQt5.QtChart as qch
from qtUI.MainWindow import Ui_MainWindow
from qtUI.SendToWindow import Ui_Dialog
# import qtUI.MyGraphicsView
import os
import sys
import cv2 as cv
import ThresAlgo
import FilterAlgo
import MorphOperAlgo
import MorphFunsAlgo
import Utils
import Config
# from qtUI.MyGraphicsView import MyGraphicsView

class MainWindow(qw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ## Menber Variables
        self.send_to_window = None
        self.image_type = 'GRAY'

        # threshold related
        self.threshold_source_image = None
        self.binary_image = None
        self.qitem_threshold_source_image = None
        self.qitem_binary_image = None
        self.threshold = Config.DEFAULT_THRESHOLD
        self.histgram_list = []
        self.prob_list = []
        # filter related
        self.filter_source_image = None
        self.filtered_image = None
        self.qitem_filter_source_image = None
        self.qitem_filtered_image = None
        self.forshow_filter = Config.ROBERTS_OPERATOR_DIR01
        self.forcalc_filter = Config.ROBERTS_OPERATOR_DIR01
        self.filter_size = self.forshow_filter.shape[0]
        self.filter_table_font_size = Config.DEFAULT_FILTER_SIZE
        self.gaussian_sigma = Config.DEFAULT_GAUSSIAN_SIGMA
        # morph operation related
        self.morph_oper_source_image = None
        self.morph_oper_image = None
        self.morph_oper_image_diff = None
        self.qitem_morph_oper_source_image = None
        self.qitem_morph_oper_image = None
        self.morph_oper_se_width = Config.DEFAULT_SE_WIDTH
        self.morph_oper_se_height = Config.DEFAULT_SE_HEIGHT
        self.forcalc_se = Config.DEFAULT_SE
        self.se_table_font_size = Config.DEFAULT_SE_SIZE
        self.se_origin = Config.DEFAULT_SE_ORIGIN
        self.morph_oper_type = 0
        self.se_type = 0
        self.table_se_click_mode = 'OFF'
        # morph functions related
        self.morph_funs_source_image = None
        self.morph_funs_image = None
        self.qitem_morph_funs_source_image = None
        self.qitem_morph_funs_image = None
        self.morph_funs_SiF = []
        self.morph_funs_gray_flags = [4,5]
        self.morph_funs_bw_flags = [0,1,2,3,4]
        self.morph_funs_flag = 0 # 0: distance transform
                                 # 1: skeleton
                                 # 2: skeleton reconstruction
                                 # 3: edge detection
                                 # 4: morph reconstruction
                                 # 5: gradient
        self.distance_trans_mode = Config.DEFAULT_DISTANCE_TRANS_MODE
        self.morph_funs_edge_detection_mode = Config.DEFAULT_EDGE_DETECTION_MODE
        self.morph_funs_ocbr_mode = Config.DEFAULT_OCBR_MODE
        self.morph_funs_gradient_mode = Config.DEFAULT_GRADIENT_MODE
        self.morph_funs_is_show_animation = False

        self.is_seperate_between_tabs = True

        ## Load UI
        self.setupUi(self)
        self.frame_filter_size.setEnabled(False)
        self.frame_gaussian_sigma.setEnabled(False)
        self.frame_se_height.setEnabled(False)
        self.frame_se_width.setEnabled(False)
        self.groupbox_morph_funs_processing.setEnabled(False)

        ## Link to Slot Function
        self.tabWidget.currentChanged.connect(self.slot_tabwidget_changed)
        # Threshold Tab
        self.pushbutton_input_path_browser.released.connect(self.slot_pushbutton_choose_image_path)
        self.slider_threshold.valueChanged.connect(self.slot_slider_threshold)
        self.line_edit_threshold.textChanged.connect(self.slot_line_edit_threshold)
        self.pushbutton_otsu.released.connect(self.slot_pushbutton_otsu)
        self.pushbutton_entropy.released.connect(self.slot_pushbutton_entropy)
        self.pushbutton_export_path_browser.released.connect(self.slot_pushbutton_choose_export_path)
        self.pushbutton_export.released.connect(self.slot_pushbutton_export)
        self.pushbutton_sendto1.released.connect(self.slot_pushbutton_send_to)
        self.pushbutton_reset.released.connect(self.slot_pushbutton_reset)
        self.pushbutton_exit.released.connect(self.slot_pushbutton_exit)
        # Filter Tab
        self.pushbutton_input_path_browser2.released.connect(self.slot_pushbutton_choose_image_path)
        self.combobox_filters.currentIndexChanged.connect(self.slot_combobox_filters)
        self.radiobutton_direct01.released.connect(self.slot_radio_button_direc1)
        self.radiobutton_direct02.released.connect(self.slot_radio_button_direc2)
        self.radiobutton_amplitude.released.connect(self.slot_radio_button_amp)
        self.slider_filter_size.valueChanged.connect(self.slot_slider_filter_size)
        self.slider_gaussian_sigma.valueChanged.connect(self.slot_slider_gaussian_sigma)
        self.table_filter.itemSelectionChanged.connect(self.slot_table_filter)
        self.pushbutton_export_path_browser2.released.connect(self.slot_pushbutton_choose_export_path)
        self.pushbutton_export2.released.connect(self.slot_pushbutton_export)
        self.pushbutton_sendto2.released.connect(self.slot_pushbutton_send_to)
        self.pushbutton_reset2.released.connect(self.slot_pushbutton_reset)
        self.pushbutton_exit2.released.connect(self.slot_pushbutton_exit)
        # Morph Operation Tab
        self.pushbutton_input_path_browser3.released.connect(self.slot_pushbutton_choose_image_path)
        self.combobox_morph_oper.currentIndexChanged.connect(self.slot_combobox_morph_oper)
        self.combobox_se.currentIndexChanged.connect(self.slot_combobox_se)
        self.checkbox_show_diff.toggled.connect(self.slot_checkbox_show_diff)
        self.checkbox_se_regular.toggled.connect(self.slot_checkbox_se_regular)
        self.slider_se_width.valueChanged.connect(self.slot_slider_se_width)
        self.slider_se_height.valueChanged.connect(self.slot_slider_se_height)
        self.pushbutton_set_origin.released.connect(self.slot_pushbutton_set_origin)
        self.pushbutton_cancel_set_origin.released.connect(self.slot_pushbutton_cancel_set_origin)
        self.table_se.clicked.connect(self.slot_table_se)
        self.pushbutton_export_path_browser3.released.connect(self.slot_pushbutton_choose_export_path)
        self.pushbutton_reset3.released.connect(self.slot_pushbutton_reset)
        self.pushbutton_sendto3.released.connect(self.slot_pushbutton_send_to)
        self.pushbutton_exit3.released.connect(self.slot_pushbutton_exit)
        self.pushbutton_export3.released.connect(self.slot_pushbutton_export)
        # Morph Funstion Tab
        self.pushbutton_input_path_browser4.released.connect(self.slot_pushbutton_choose_image_path)
        self.combobox_distance_trans_mode.currentIndexChanged.connect(self.slot_combobox_distance_trans_mode)
        self.checkbox_animation.toggled.connect(self.slot_checkbox_animation)
        self.radiobutton_distance_transfrom.clicked.connect(self.slot_radiobutton_distance_trans)
        self.radiobutton_skeleton.clicked.connect(self.slot_radiobutton_skeleton)
        self.radiobutton_skeleton_reconstruction.clicked.connect(self.slot_radiobutton_skeleton_reconstruction)
        self.radiobutton_edge_detection.clicked.connect(self.slot_radiobutton_edge_detection)
        self.radiobutton_morph_reconstruction.clicked.connect(self.slot_radiobutton_morph_reconstruction)
        self.radiobutton_gradient.clicked.connect(self.slot_radiobutton_gradient)
        self.combobox_edge_detection.currentIndexChanged.connect(self.slot_combobox_edge_detection)
        self.combobox_morph_reconstrction.currentIndexChanged.connect(self.slot_combobox_morph_reconstrction)
        self.combobox_gradient.currentIndexChanged.connect(self.slot_combobox_gradient)
        self.combobox_marker_shape.currentIndexChanged.connect(self.slot_combobox_marker_shape)
        self.pushbutton_set_marker.released.connect(self.slot_pushbutton_set_marker)
        self.pushbutton_cancel_set_marker.released.connect(self.slot_pushbutton_cancel_set_marker)
        self.graphics_view_marker.pressed_signal.connect(self.slot_morph_funs_pressed_signal)

        self.pushbutton_export_path_browser4.released.connect(self.slot_pushbutton_choose_export_path)
        self.pushbutton_reset4.released.connect(self.slot_pushbutton_reset)
        self.pushbutton_sendto4.released.connect(self.slot_pushbutton_send_to)
        self.pushbutton_exit4.released.connect(self.slot_pushbutton_exit)
        self.pushbutton_export4.released.connect(self.slot_pushbutton_export)

    #######################
    # Shared Slot Functions
    #######################
    # region
    def slot_pushbutton_choose_image_path(self):
        """
        slot function -- pushbutton -- choose image path
        :return: bool value stand for success or not
        """
        image_path, _ = qw.QFileDialog.getOpenFileName(self, "Select Images", os.getcwd())
        if image_path == '':
            return False
        elif self.is_seperate_between_tabs == True:
            if self.tabWidget.currentIndex() == 0:
                self.line_edit_input_path.setText(image_path)
                self.threshold_source_image, _ = Utils.LoadImage(image_path)
                self._init_threshold_ui()
                return True
            elif self.tabWidget.currentIndex() == 1:
                self.line_edit_input_path2.setText(image_path)
                self.filter_source_image, _ = Utils.LoadImage(image_path)
                self._init_filter_ui()
                return True
            elif self.tabWidget.currentIndex() == 2:
                self.line_edit_input_path3.setText(image_path)
                self.morph_oper_source_image, _ = Utils.LoadImage(image_path)
                self._init_morph_oper_ui()
                return True
            elif self.tabWidget.currentIndex() == 3:
                self.line_edit_input_path4.setText(image_path)
                self.morph_funs_source_image, self.image_type = Utils.LoadImage(image_path)
                self._init_morph_funs_ui()
                return True
        else:
            if self.tabWidget.currentIndex() == 0 or self.tabWidget.currentIndex() == 1:
                self.line_edit_input_path.setText(image_path)
                self.line_edit_input_path2.setText(image_path)
                self.threshold_source_image, _ = Utils.LoadImage(image_path)
                self.filter_source_image, _ = Utils.LoadImage(image_path)

                self._init_threshold_ui()
                self._init_filter_ui()
            elif self.tabWidget.currentIndex() == 2 or self.tabWidget.currentIndex() == 3:
                self.line_edit_input_path3.setText(image_path)
                self.line_edit_input_path4.setText(image_path)
                self.morph_oper_source_image, _ = Utils.LoadImage(image_path)
                self.morph_funs_source_image, self.image_type = Utils.LoadImage(image_path)

                self._init_morph_oper_ui()
                self._init_morph_funs_ui()

    def slot_pushbutton_choose_export_path(self):
        """
        slot function -- pushbutton -- choose export path
        :return: None
        """
        save_path, _ = qw.QFileDialog.getSaveFileName(self, "Select Path", os.getcwd())
        if self.tabWidget.currentIndex() == 0:
            self.line_edit_export_path.setText(save_path)
            self.pushbutton_export.setEnabled(True)
        elif self.tabWidget.currentIndex() == 1:
            self.line_edit_export_path2.setText(save_path)
            self.pushbutton_export2.setEnabled(True)
        elif self.tabWidget.currentIndex() == 2:
            self.line_edit_export_path3.setText(save_path)
            self.pushbutton_export3.setEnabled(True)
        elif self.tabWidget.currentIndex() == 3:
            self.line_edit_export_path4.setText(save_path)
            self.pushbutton_export4.setEnabled(True)

    def slot_pushbutton_export(self):
        """
        slot function -- pushbutton -- export result image to selected path
        :return: None
        """
        if self.tabWidget.currentIndex() == 0:
            save_path = self.line_edit_export_path.text()
            save_image = self.binary_image
        elif self.tabWidget.currentIndex() == 1:
            save_path = self.line_edit_export_path2.text()
            save_image = self.filtered_image
        elif self.tabWidget.currentIndex() == 2:
            save_path = self.line_edit_export_path3.text()
            save_image = self.morph_oper_image
        elif self.tabWidget.currentIndex() == 3:
            save_path = self.line_edit_export_path4.text()
            save_image = self.morph_funs_image
        if save_path == '':
            qw.QMessageBox.warning(self, "Warning", "Choose an export path!")
            return False
        elif Utils.SaveImage(save_image, save_path):
            qw.QMessageBox.information(self, "Inform", "Export Successfully!")
            return True
        else:
            qw.QMessageBox.warning(self, "Error", "Export Unsuccessfully!")
            return False

    def slot_pushbutton_send_to(self):
        self.send_to_window = SendToWindow()
        if self.send_to_window.exec() == qw.QDialog.Accepted:
            temp_tabwidget_current_index = self.tabWidget.currentIndex()
            self.tabWidget.setCurrentIndex(self.send_to_window.selected_tab)
            temp_source_images_list = [self.threshold_source_image, self.filter_source_image,
                                       self.morph_oper_source_image, self.morph_funs_source_image]
            temp_result_images_list = [self.binary_image, self.filtered_image, self.morph_oper_image, self.morph_funs_image]
            temp_source_images_list[self.send_to_window.selected_tab] = temp_result_images_list[temp_tabwidget_current_index]
            if self.send_to_window.selected_tab == 0:
                self.threshold_source_image = temp_source_images_list[0]
                self._init_threshold_ui()
            elif self.send_to_window.selected_tab == 1:
                self.filter_source_image = temp_source_images_list[1]
                self._init_filter_ui()
            elif self.send_to_window.selected_tab == 2:
                self.morph_oper_source_image = temp_source_images_list[2]
                self._init_morph_oper_ui()
            elif self.send_to_window.selected_tab == 3:
                self.morph_funs_source_image = temp_source_images_list[3]
                self.image_type = Utils.ImageType(self.morph_funs_source_image)
                self._init_morph_funs_ui()

    def slot_pushbutton_reset(self):
        """
        slot function -- pushbutton -- reset all paraeter and update UI
        :return: None
        """
        if self.tabWidget.currentIndex() == 0:
            self._set_threshold_in_ui(Config.DEFAULT_THRESHOLD)
        elif self.tabWidget.currentIndex() == 1:
            self.filter_size = int((Config.DEFAULT_FILTER_SIZE - 1) / 2)
            self.gaussian_sigma = Config.DEFAULT_GAUSSIAN_SIGMA
            self.slider_filter_size.setValue(self.filter_size)
            self.slider_gaussian_sigma.setValue(self.gaussian_sigma)
            self.combobox_filters.setCurrentIndex(0)
        elif self.tabWidget.currentIndex() == 2:
            self.morph_oper_se_width = Config.DEFAULT_SE_WIDTH
            self.morph_oper_se_height = Config.DEFAULT_SE_HEIGHT
            self.forcalc_se = Config.DEFAULT_SE
            self.se_table_font_size = Config.DEFAULT_SE_SIZE
            self.se_origin = Config.DEFAULT_SE_ORIGIN
            self.morph_oper_type = 0
            self.se_type = 0
            self.table_se_click_mode = 'OFF'

            self.slider_se_width.setValue(int((self.morph_oper_se_width - 1) / 2))
            self.slider_se_height.setValue(int((self.morph_oper_se_height - 1) / 2))
            self.checkbox_show_diff.setChecked(False)
            self.checkbox_se_regular.setChecked(False)
            self.combobox_morph_oper.setCurrentIndex(0)
            self.combobox_se.setCurrentIndex(0)
        elif self.tabWidget.currentIndex() == 3:
            # reset parameters
            self.morph_funs_SiF = []
            self.morph_funs_flag = 0  # 0: distance transform
                                      # 1: skeleton
                                      # 2: skeleton reconstruction
                                      # 3: edge detection
                                      # 4: morph reconstruction
                                      # 5: gradient
            self.distance_trans_mode = Config.DEFAULT_DISTANCE_TRANS_MODE
            self.morph_funs_edge_detection_mode = Config.DEFAULT_EDGE_DETECTION_MODE
            self.morph_funs_ocbr_mode = Config.DEFAULT_OCBR_MODE
            self.morph_funs_gradient_mode = Config.DEFAULT_GRADIENT_MODE
            self.morph_funs_is_show_animation = False
            # reset ui
            self.combobox_distance_trans_mode.setCurrentIndex(0)
            self.checkbox_animation.setChecked(False)
            self.combobox_edge_detection.setCurrentIndex(0)
            self.combobox_morph_reconstrction.setCurrentIndex(0)
            self.combobox_gradient.setCurrentIndex(0)
            self.combobox_marker_shape.setCurrentIndex(0)
            # reset widget enable
            if self.image_type == 'BW':
                self._set_morph_funs_default_marker()
                self.radiobutton_distance_transfrom.setChecked(True)
                self.slot_radiobutton_distance_trans()
            elif self.image_type == 'GRAY':
                self.radiobutton_morph_reconstruction.setChecked(True)
                self.slot_radiobutton_morph_reconstruction()

    def slot_pushbutton_exit(self):
        """
        slot function -- pushbutton -- exit window
        :return: None
        """
        self.close()
    # endregion

    #######################
    # Threshold Slot Functions
    #######################
    # region
    def slot_slider_threshold(self):
        """
        slot function -- slider -- change threshold value in UI
        :return: None
        """
        self._set_threshold_in_ui(self.slider_threshold.value())

    def slot_line_edit_threshold(self):
        """
        slot function -- line edit -- to get new threshold and update UI
        :return: bool value stand for success or not
        """
        if self.line_edit_threshold.text() == '':
            return False
        elif self.line_edit_threshold.text().isdigit() == False:
            qw.QMessageBox.warning(self, "Warning", "Input a num!")
            self._set_threshold_in_ui(Config.DEFAULT_THRESHOLD)
            return False
        elif int(self.line_edit_threshold.text()) < 0 or int(self.line_edit_threshold.text()) > 255:
            qw.QMessageBox.warning(self, "Warning", "Out of range!")
            self._set_threshold_in_ui(Config.DEFAULT_THRESHOLD)
            return False
        else:
            self._set_threshold_in_ui(self.line_edit_threshold.text())
            self._update_binary_image()
            self._update_chart_histgram('n')
            return True

    def slot_pushbutton_otsu(self):
        """
        slot function -- pushbutton -- apply otsu algotirhm and update UI
        :return: None
        """
        otsu_threshold = ThresAlgo.Otsu(self.prob_list)
        self._set_threshold_in_ui(otsu_threshold)

    def slot_pushbutton_entropy(self):
        """
        slot function -- pushbutton -- apply entropy algorithm and update UI
        :return: None
        """
        entropy_threshold = ThresAlgo.Entropy(self.prob_list)
        self._set_threshold_in_ui(entropy_threshold)

    # endregion

    #######################
    # Filters Slot Functions
    #######################
    # region
    def slot_combobox_filters(self):
        """
        slot function -- combobox -- choose filter and update UI
        :return: None
        """
        self.radiobutton_direct01.setChecked(True)
        current_index = self.combobox_filters.currentIndex()
        self.radiobutton_direct01.setChecked(True)
        if current_index <= 2:
            self.frame_filter_size.setEnabled(False)
            self.radiobutton_direct01.setEnabled(True)
            self.radiobutton_direct02.setEnabled(True)
            self.radiobutton_amplitude.setEnabled(True)
        else:
            self.frame_filter_size.setEnabled(True)
            self.radiobutton_direct01.setEnabled(False)
            self.radiobutton_direct02.setEnabled(False)
            self.radiobutton_amplitude.setEnabled(False)
        if current_index == 5:
            self.frame_gaussian_sigma.setEnabled(True)
        else:
            self.frame_gaussian_sigma.setEnabled(False)
        if current_index == 6:
            self.table_filter.setEnabled(True)
        else:
            self.table_filter.setEnabled(False)

        filter_mode = 'general'
        if current_index == 0:
            self.forshow_filter = Config.ROBERTS_OPERATOR_DIR01
        elif current_index == 1:
            self.forshow_filter = Config.PREWITT_OPERATOE_DIR01
        elif current_index == 2:
            self.forshow_filter = Config.SOBEL_OPERATOR_DIR01
        elif current_index == 3:
            self._mean_filter()
        elif current_index == 4:
            self._median_filter()
            filter_mode = 'fi_med'
        elif current_index == 5:
            self._gaussian_filter()
        elif current_index == 6:
            self._user_definded_filter()
        self._update_filter_image(mode = filter_mode)

    def slot_radio_button_direc1(self):
        """
        slot function -- radio button -- use direct01 filter and update UI
        :return: None
        """
        if self.combobox_filters.currentIndex() == 0:
            self.forshow_filter = Config.ROBERTS_OPERATOR_DIR01
        elif self.combobox_filters.currentIndex() == 1:
            self.forshow_filter = Config.PREWITT_OPERATOE_DIR01
        elif self.combobox_filters.currentIndex() == 2:
            self.forshow_filter = Config.SOBEL_OPERATOR_DIR01
        else:
            pass
        self._update_filter_image()

    def slot_radio_button_direc2(self):
        """
        slot function -- radio button -- use direct01 filter and update UI
        :return: None
        """
        if self.combobox_filters.currentIndex() == 0:
            self.forshow_filter = Config.ROBERTS_OPERATOR_DIR02
        elif self.combobox_filters.currentIndex() == 1:
            self.forshow_filter = Config.PREWITT_OPERATOE_DIR02
        elif self.combobox_filters.currentIndex() == 2:
            self.forshow_filter = Config.SOBEL_OPERATOR_DIR02
        else:
            pass
        self._update_filter_image()

    def slot_radio_button_amp(self):
        """
        slot function -- radio button -- apply amplitude
        :return: None
        """
        if self.combobox_filters.currentIndex() == 0:
            filters = [Config.ROBERTS_OPERATOR_DIR01, Config.ROBERTS_OPERATOR_DIR02]
        elif self.combobox_filters.currentIndex() == 1:
            filters = [Config.PREWITT_OPERATOE_DIR01, Config.PREWITT_OPERATOE_DIR02]
        elif self.combobox_filters.currentIndex() == 2:
            filters = [Config.SOBEL_OPERATOR_DIR01, Config.SOBEL_OPERATOR_DIR02]
        else:
            pass
        self.forshow_filter = np.zeros(filters[0].shape, dtype=int)
        self._update_filter_image('op-amp', filters)

    def slot_slider_filter_size(self):
        """
        slot function -- slider -- change filter size and update UI
        :return: None
        """
        self.filter_size = self.slider_filter_size.value() * 2 + 1
        self.line_edit_filter_size.setText(str(self.filter_size))
        current_index = self.combobox_filters.currentIndex()
        filter_mode = 'general'
        if current_index == 3:
            self._mean_filter()
        elif current_index == 4:
            self._median_filter()
            filter_mode = 'fi_med'
        elif current_index == 5:
            self.gaussian_sigma = self.slider_gaussian_sigma.value() * 0.1
            self._gaussian_filter()
        elif current_index == 6:
            self._user_definded_filter()
        else:
            return
        self._update_filter_image(mode = filter_mode)

    def slot_slider_gaussian_sigma(self):
        """
        slot function -- slider -- change gaussian sigma and update UI
        :return: None
        """
        if self.combobox_filters.currentIndex() == 5:
            self.gaussian_sigma = self.slider_gaussian_sigma.value() * 0.1
            self.line_edit_gaussian_sigma.setText(str(np.around(self.gaussian_sigma,3)))
            self._gaussian_filter()
            self._update_filter_image()
        else:
            return

    def slot_table_filter(self):
        """
        slot function -- slider -- change table item and update UI
        :return: None
        """
        self.table_filter.clearSelection() # avoid interference of selected color
        self.forshow_filter = np.zeros((self.filter_size, self.filter_size))
        for row_index in range(self.filter_size):
            for col_index in range(self.filter_size):
                self.forshow_filter[row_index][col_index] = float(self.table_filter.item(row_index, col_index).text())
        self._update_filter_image()

    def slot_tabwidget_changed(self):
        if self.tabWidget.currentIndex() == 0 and self.line_edit_input_path.text() != '':
            self._fit_view()
        elif self.tabWidget.currentIndex() == 1 and self.line_edit_input_path2.text() != '':
            self._fit_view()
            self._update_table_filter()
        elif self.tabWidget.currentIndex() == 2 and self.line_edit_input_path3.text() != '':
            self._fit_view()
        elif self.tabWidget.currentIndex() == 3 and self.line_edit_input_path4.text() != '':
            self._fit_view()

    # endregion

    #######################
    # Morph Operation Slot Functions
    #######################
    # region
    def slot_combobox_morph_oper(self):
        self.morph_oper_type = self.combobox_morph_oper.currentIndex()
        self._update_morph_oper_image()

    def slot_combobox_se(self):
        self.se_type = self.combobox_se.currentIndex()
        self._update_se()
        self._update_table_se()
        self._update_morph_oper_image()

    def slot_checkbox_show_diff(self):
        self._update_morph_oper_image()

    def slot_checkbox_se_regular(self):
        if self.checkbox_se_regular.isChecked() == True:
            self.morph_oper_se_width = np.maximum(self.morph_oper_se_height, self.morph_oper_se_width)
            self.morph_oper_se_height = np.maximum(self.morph_oper_se_height, self.morph_oper_se_width)
            self.slider_se_width.setValue(int((self.morph_oper_se_width - 1) / 2))
            self.slider_se_height.setValue(int((self.morph_oper_se_height - 1) / 2))

    def slot_slider_se_width(self):
        if self.checkbox_se_regular.isChecked() == False:
            self.morph_oper_se_width = self.slider_se_width.value() * 2 + 1
        else:
            self.morph_oper_se_width = self.slider_se_width.value() * 2 + 1
            self.morph_oper_se_height = self.morph_oper_se_width
            self.slider_se_height.setValue(int((self.morph_oper_se_height - 1) / 2))
        self.line_edit_se_width.setText(str(self.morph_oper_se_width))
        self._update_se()
        self._update_table_se()
        self._update_morph_oper_image()

    def slot_slider_se_height(self):
        if self.checkbox_se_regular.isChecked() == False:
            self.morph_oper_se_height = self.slider_se_height.value() * 2 + 1
        else:
            self.morph_oper_se_height = self.slider_se_height.value() * 2 + 1
            self.morph_oper_se_width = self.morph_oper_se_height
            self.slider_se_width.setValue(int((self.morph_oper_se_width - 1) / 2))
        self.line_edit_se_height.setText(str(self.morph_oper_se_height))
        self._update_se()
        self._update_table_se()
        self._update_morph_oper_image()

    def slot_pushbutton_set_origin(self):
        self.pushbutton_set_origin.setEnabled(False)
        self.pushbutton_cancel_set_origin.setEnabled(True)
        self.frame_morph_oper_function_area.setEnabled(False)
        self.table_se.setEnabled(True)
        self.table_se_click_mode = 'SET_ORIGIN'
        self.table_se.setCursor(qc.Qt.CrossCursor)
        self.table_se.setSelectionMode(qw.QAbstractItemView.SingleSelection)

    def slot_pushbutton_cancel_set_origin(self):
        self.pushbutton_set_origin.setEnabled(True)
        self.pushbutton_cancel_set_origin.setEnabled(False)
        self.frame_morph_oper_function_area.setEnabled(True)
        if self.se_type == 3:
            self.table_se.setEnabled(True)
            self.table_se_click_mode = 'USER_DEFINED_SE'
        else:
            self.table_se.setEnabled(False)
            self.table_se_click_mode = 'OFF'
        self.table_se.setCursor(qc.Qt.ArrowCursor)
        self.table_se.setSelectionMode(qw.QAbstractItemView.ExtendedSelection)

    def slot_table_se(self):
        if self.table_se_click_mode == 'SET_ORIGIN':
            self.se_origin = (self.table_se.selectedIndexes()[0].row(), self.table_se.selectedIndexes()[0].column())
            self.table_se.clearSelection()
            self._update_table_se()
            self._update_morph_oper_image()
        elif self.table_se_click_mode == 'USER_DEFINED_SE':
            current_row = self.table_se.selectedIndexes()[0].row()
            current_col = self.table_se.selectedIndexes()[0].column()
            if self.forcalc_se[current_row, current_col] == 0:
                self.forcalc_se[current_row, current_col] = 1
            elif self.forcalc_se[current_row, current_col] == 1:
                self.forcalc_se[current_row, current_col] = 0
            self.table_se.clearSelection()
            self.forcalc_se = self.forcalc_se
            self._update_table_se()
            self._update_morph_oper_image()
    # endregion

    #######################
    # Morph Functions Slot Functions
    #######################
    # region

    def slot_radiobutton_distance_trans(self):
        self.morph_funs_flag = 0
        self._update_morph_funs_widget_enabled()
        self._update_morph_funs_image()
    def slot_radiobutton_skeleton(self):
        self.morph_funs_flag = 1
        self._update_morph_funs_widget_enabled()
        self._update_morph_funs_image()
    def slot_radiobutton_skeleton_reconstruction(self):
        self.morph_funs_flag = 2
        self._update_morph_funs_widget_enabled()
        self._update_morph_funs_image()
    def slot_radiobutton_edge_detection(self):
        self.morph_funs_flag = 3
        self._update_morph_funs_widget_enabled()
        self._update_morph_funs_image()
    def slot_radiobutton_morph_reconstruction(self):
        self.morph_funs_flag = 4
        self._update_morph_funs_widget_enabled()
        self._update_morph_funs_image()
    def slot_radiobutton_gradient(self):
        self.morph_funs_flag = 5
        self._update_morph_funs_widget_enabled()
        self._update_morph_funs_image()

    def slot_combobox_distance_trans_mode(self):
        if self.combobox_distance_trans_mode.currentIndex() == 0:
            self.distance_trans_mode = 'CHESSBOARD'
        elif self.combobox_distance_trans_mode.currentIndex() == 1:
            self.distance_trans_mode = 'CITYBLOCK'
        elif self.combobox_distance_trans_mode.currentIndex() == 2:
            self.distance_trans_mode = 'EUCLIDEAN'
        self._update_morph_funs_image()

    def slot_checkbox_animation(self):
        self.morph_funs_is_show_animation = self.checkbox_animation.isChecked()
        self._update_morph_funs_image()

    def slot_combobox_edge_detection(self):
        if self.combobox_edge_detection.currentIndex() == 0:
            self.morph_funs_edge_detection_mode = 'STANDARD'
        elif self.combobox_edge_detection.currentIndex() == 1:
            self.morph_funs_edge_detection_mode = 'EXTERNAL'
        elif self.combobox_edge_detection.currentIndex() == 2:
            self.morph_funs_edge_detection_mode = 'INTERNAL'
        self._update_morph_funs_image()

    def slot_combobox_morph_reconstrction(self):
        if self.combobox_morph_reconstrction.currentIndex() == 0:
            self.morph_funs_ocbr_mode = 'OBR'
        elif self.combobox_morph_reconstrction.currentIndex() == 1:
            self.morph_funs_ocbr_mode = 'CBR'
        self._update_morph_funs_image()

    def slot_combobox_gradient(self):
        if self.combobox_gradient.currentIndex() == 0:
            self.morph_funs_gradient_mode = 'EXTERNAL'
        elif self.combobox_gradient.currentIndex() == 1:
            self.morph_funs_gradient_mode = 'INTERNAL'
        self._update_morph_funs_image()

    def slot_combobox_marker_shape(self):
        if self.combobox_marker_shape.currentIndex() == 0:
            self.graphics_view_marker.marker_shape_type = 'DISK'
        if self.combobox_marker_shape.currentIndex() == 1:
            self.graphics_view_marker.marker_shape_type = 'V_LINE'
        if self.combobox_marker_shape.currentIndex() == 2:
            self.graphics_view_marker.marker_shape_type = 'H_LINE'

    def slot_pushbutton_set_marker(self):
        self.graphics_view_marker.is_setting_marker = True
        self.pushbutton_cancel_set_marker.setEnabled(True)
        self.pushbutton_set_marker.setEnabled(False)
        self.combobox_marker_shape.setEnabled(False)
        self.graphics_view_marker.setCursor(qc.Qt.CrossCursor)

    def slot_pushbutton_cancel_set_marker(self):
        self.graphics_view_marker.is_setting_marker = False
        self.pushbutton_cancel_set_marker.setEnabled(False)
        self.pushbutton_set_marker.setEnabled(True)
        self.combobox_marker_shape.setEnabled(True)
        self.graphics_view_marker.setCursor(qc.Qt.ArrowCursor)

    def slot_morph_funs_pressed_signal(self):
        self._update_morph_funs_image()
        self.slot_pushbutton_cancel_set_marker()
    # endregion

    #######################
    # Events
    #######################
    def resizeEvent(self, a0: qg.QResizeEvent) -> None:
        if self.line_edit_input_path.text() != '' or \
                self.line_edit_input_path2.text() != '' or \
                self.line_edit_input_path3.text() != '' or \
                self.line_edit_input_path4.text() != '':
            self._fit_view()


    #######################
    # Utils Functions
    #######################

    def _set_threshold_in_ui(self, thres):
        """
        set the slider to current threshold
        :param thres: current threshold
        :return: None
        """
        self.threshold = int(thres)
        self.line_edit_threshold.setText(str(self.threshold))
        self.slider_threshold.setValue(self.threshold)

    def _update_binary_image(self):
        """
        util function -- update binary image in Threshold Tab
        :return: None
        """
        self.binary_image = ThresAlgo.Threshold(self.threshold_source_image, self.threshold)
        self.qitem_binary_image, qscene_binary_image = Utils.show_on_graphview(self.binary_image)
        self.graphics_view_binary_image.setScene(qscene_binary_image)
        self.graphics_view_binary_image.fitInView(self.qitem_binary_image, qc.Qt.KeepAspectRatio)

    def _update_chart_histgram(self, isInit = 'y'):
        qchart_histgram = Utils.show_on_chartview(self.histgram_list, self.threshold, isInit)
        self.graphics_view_histgram.setChart(qchart_histgram)

    def _update_filter_image(self, mode = 'general', filters = None):
        """
        util function -- update filter image in Filters Tab
        :param mode: filter mode, for specil filters, including:
                    - Operators for Amplitude -- 'op-amp'
                    - Median Filter -- 'fi_med'
                    others are convolution between and filter named 'general'
        :param filters: when mode is 'ap-amp', we need input all filters (list type)
        :return: None
        """
        if mode == 'general':
            self.forcalc_filter = FilterAlgo.CheckFilter(self.forshow_filter)
            self.filtered_image = FilterAlgo.Convolution(self.filter_source_image, self.forcalc_filter)
            self.filtered_image = FilterAlgo.CheckImage(self.filtered_image)
        elif mode == 'op-amp':
            self.filtered_image = np.zeros(self.filter_source_image.shape)
            for filter in filters:
                calc_filter = FilterAlgo.CheckFilter(filter)
                filtered_image = 1.0 * FilterAlgo.Convolution(self.filter_source_image, calc_filter)
                self.filtered_image += (filtered_image ** 2)
            self.filtered_image = np.uint8(np.sqrt(self.filtered_image))
            self.filtered_image = FilterAlgo.CheckImage(self.filtered_image)
        elif mode == 'fi_med':
            self.filtered_image = FilterAlgo.MedianFiltering(self.filter_source_image, self.filter_size)
            self.filtered_image = FilterAlgo.CheckImage(self.filtered_image)

        self.qitem_filtered_image, qscene_filtered_image = Utils.show_on_graphview(self.filtered_image)
        self.graphics_view_filters_image.setScene(qscene_filtered_image)
        self.graphics_view_filters_image.fitInView(self.qitem_filtered_image, qc.Qt.KeepAspectRatio)

        self._update_table_filter()

    def _update_table_filter(self):
        """
        util function -- update table in UI
        :return: None
        """
        self.filter_size = self.forshow_filter.shape[0]
        self.table_filter.setColumnCount(self.filter_size)
        self.table_filter.setRowCount(self.filter_size)
        self.table_filter.verticalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
        self.table_filter.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
        self.filter_table_font_size = int(self.table_filter.columnWidth(0) / 5)
        for col_index in range(self.filter_size):
            for row_index in range(self.filter_size):
                value = self.forshow_filter[col_index][row_index]
                current_table_item = self._get_filter_table_item(value)
                self.table_filter.setItem(col_index, row_index, current_table_item)

    def _update_morph_oper_image(self):
        if self.morph_oper_type == 0:
            self.morph_oper_image = MorphOperAlgo.mine_Dilation(self.morph_oper_source_image, self.forcalc_se, self.se_origin)
        elif self.morph_oper_type == 1:
            self.morph_oper_image = MorphOperAlgo.mine_Erosion(self.morph_oper_source_image, self.forcalc_se, self.se_origin)
        elif self.morph_oper_type == 2:
            self.morph_oper_image = MorphOperAlgo.mine_Open(self.morph_oper_source_image, self.forcalc_se, self.se_origin)
        elif self.morph_oper_type == 3:
            self.morph_oper_image = MorphOperAlgo.mine_Close(self.morph_oper_source_image, self.forcalc_se, self.se_origin)

        if self.checkbox_show_diff.isChecked() == False:
            self.qitem_morph_oper_image, qscene_morph_oper_image = Utils.show_on_graphview(self.morph_oper_image)
            self.graphics_view_morph_oper_image.setScene(qscene_morph_oper_image)
            self.graphics_view_morph_oper_image.fitInView(self.qitem_morph_oper_image, qc.Qt.KeepAspectRatio)
        else:
            self.morph_oper_image_diff = np.copy(self.morph_oper_image)
            self.morph_oper_image_diff = cv.cvtColor(self.morph_oper_image_diff, cv.COLOR_GRAY2RGB)
            diff_three_channel = np.uint8(np.abs(self.morph_oper_source_image / 255 - self.morph_oper_image / 255) * 255)
            diff_three_channel = cv.cvtColor(diff_three_channel, cv.COLOR_GRAY2RGB)

            if self.morph_oper_type == 0:
                diff_three_channel[:,:,0] = 0
                diff_three_channel[:,:,2] = 0
            elif self.morph_oper_type == 1:
                diff_three_channel[:,:,1] = 0
                diff_three_channel[:,:,2] = 0
            elif self.morph_oper_type == 2:
                diff_three_channel[:,:,1] = 0
            elif self.morph_oper_type == 3:
                diff_three_channel[:,:,0] = 0

            self.morph_oper_image_diff = cv.addWeighted(self.morph_oper_image_diff, 0.8, diff_three_channel, 0.8, 0)
            self.qitem_morph_oper_image, qscene_morph_oper_image = Utils.show_on_graphview(self.morph_oper_image_diff)
            self.graphics_view_morph_oper_image.setScene(qscene_morph_oper_image)
            self.graphics_view_morph_oper_image.fitInView(self.qitem_morph_oper_image, qc.Qt.KeepAspectRatio)

    def _update_table_se(self):
        """
        util function -- update table in UI
        :return: None
        """
        se_size = self.forcalc_se.shape[0]
        self.table_se.setColumnCount(se_size)
        self.table_se.setRowCount(se_size)
        self.table_se.verticalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
        self.table_se.horizontalHeader().setSectionResizeMode(qw.QHeaderView.Stretch)
        self.se_table_font_size = int(self.table_se.columnWidth(0) / 5)
        for col_index in range(se_size):
            for row_index in range(se_size):
                if (self.se_origin == (-1, -1) and col_index == int((se_size) / 2) and row_index == int((se_size) / 2))\
                        or (col_index == self.se_origin[0] and row_index == self.se_origin[1]):
                    is_origin = True
                else:
                    is_origin = False
                value = self.forcalc_se[col_index][row_index]
                current_table_item = self._get_se_table_item(value, is_origin)
                self.table_se.setItem(col_index, row_index, current_table_item)

    def _update_se(self):
        # update se origin
        if self.se_origin != Config.DEFAULT_SE_ORIGIN:
            offset = int((np.maximum(self.morph_oper_se_width, self.morph_oper_se_height) - self.forcalc_se.shape[0]) / 2)
            self.se_origin = (self.se_origin[0] + offset, self.se_origin[1] + offset)
        # update se
        if self.se_type < 3:
            self.forcalc_se = MorphOperAlgo.mine_getStructureElement(self.se_type, (self.morph_oper_se_width, self.morph_oper_se_height))
            self.forcalc_se = MorphOperAlgo.CheckSE(self.forcalc_se)
            self.table_se_click_mode = 'OFF'
            self.table_se.setEnabled(False)
        else:
            self.table_se_click_mode = 'USER_DEFINED_SE'
            # self.se_origin = Config.DEFAULT_SE_ORIGIN
            self.forcalc_se = np.ones((self.morph_oper_se_height, self.morph_oper_se_width))
            self.forcalc_se = MorphOperAlgo.CheckSE(self.forcalc_se)
            self.table_se.setEnabled(True)
            # self.forcalc_se = self.forcalc_se

    def _update_morph_funs_image(self):
        if self.morph_funs_flag == 0:
            self.morph_funs_image = MorphFunsAlgo.DistanceTrans(self.morph_funs_source_image, self.distance_trans_mode)
        elif self.morph_funs_flag == 1:
            self.morph_funs_image, self.morph_funs_SiF = MorphFunsAlgo.Skeleton(self.morph_funs_source_image,
                                                                                is_show_animation=self.morph_funs_is_show_animation)
        elif self.morph_funs_flag == 2:
            self.morph_funs_image = MorphFunsAlgo.SkeletonReconstrctution(self.morph_funs_SiF,
                                                                          self.morph_funs_source_image.shape)
                                                                          # is_show_animation=self.morph_funs_is_show_animation)
        elif self.morph_funs_flag == 3:
            self.morph_funs_image = MorphFunsAlgo.EdgeDetection(self.morph_funs_source_image,
                                                                mode = self.morph_funs_edge_detection_mode)
        elif self.morph_funs_flag == 4:
            if self.image_type == 'BW':
                self.morph_funs_image = MorphFunsAlgo.ConditionalDilation(self.morph_funs_source_image,
                                                                          self.graphics_view_marker.morph_funs_marker)
                                                                          # is_show_animation=self.morph_funs_is_show_animation)
            elif self.image_type == 'GRAY':
                self.morph_funs_image = MorphFunsAlgo.OCBR(self.morph_funs_source_image,
                                                           mode = self.morph_funs_ocbr_mode)
                                                           # is_show_animation=self.morph_funs_is_show_animation)
        elif self.morph_funs_flag == 5:
            self.morph_funs_image = MorphFunsAlgo.Gradient(self.morph_funs_source_image, mode = self.morph_funs_gradient_mode)
        self.qitem_morph_funs_image, qscene_morph_funs_image = Utils.show_on_graphview(self.morph_funs_image)
        self.graphics_view_morph_funs_image.setScene(qscene_morph_funs_image)
        self.graphics_view_morph_funs_image.fitInView(self.qitem_morph_funs_image, qc.Qt.KeepAspectRatio)

    def _update_morph_funs_widget_enabled(self):
        if self.image_type == 'GRAY':
            if self.morph_funs_flag not in self.morph_funs_gray_flags:
                self.morph_funs_flag = 4
                self.radiobutton_morph_reconstruction.setChecked(True)
            self.radiobutton_distance_transfrom.setEnabled(False)
            self.radiobutton_skeleton.setEnabled(False)
            self.radiobutton_skeleton_reconstruction.setEnabled(False)
            self.radiobutton_edge_detection.setEnabled(False)
            self.radiobutton_morph_reconstruction.setEnabled(True)
            self.radiobutton_gradient.setEnabled(True)
            self.combobox_marker_shape.setEnabled(False)
            self.pushbutton_set_marker.setEnabled(False)
        elif self.image_type == 'BW':
            if self.morph_funs_flag not in self.morph_funs_bw_flags:
                self.morph_funs_flag = 0
                self.radiobutton_distance_transfrom.setChecked(True)
            self.radiobutton_distance_transfrom.setEnabled(True)
            self.radiobutton_skeleton.setEnabled(True)
            self.radiobutton_skeleton_reconstruction.setEnabled(True)
            self.radiobutton_edge_detection.setEnabled(True)
            self.radiobutton_morph_reconstruction.setEnabled(True)
            self.radiobutton_gradient.setEnabled(False)
            if self.morph_funs_flag == 4:
                self.combobox_marker_shape.setEnabled(True)
                self.pushbutton_set_marker.setEnabled(True)
                self.graphics_view_marker.setEnabled(True)
            else:
                self.combobox_marker_shape.setEnabled(False)
                self.pushbutton_set_marker.setEnabled(False)
                self.graphics_view_marker.setEnabled(False)

        self.combobox_morph_reconstrction.clear()
        self.combobox_morph_reconstrction.addItems(Config.COMBOBOX_MORPH_RECONSTRUCTUTION_ITEMS[self.image_type])

        if self.morph_funs_flag < 3:
            self.combobox_edge_detection.setEnabled(False)
            self.combobox_morph_reconstrction.setEnabled(False)
            self.combobox_gradient.setEnabled(False)
        else:
            self.combobox_distance_trans_mode.setEnabled(False)
            self.checkbox_animation.setEnabled(False)

        if self.morph_funs_flag == 0:
            self.combobox_distance_trans_mode.setEnabled(True)
            self.checkbox_animation.setEnabled(False)
        elif self.morph_funs_flag == 1:
            self.combobox_distance_trans_mode.setEnabled(False)
            self.checkbox_animation.setEnabled(True)
        elif self.morph_funs_flag == 2:
            self.combobox_distance_trans_mode.setEnabled(False)
            self.checkbox_animation.setEnabled(False)
        elif self.morph_funs_flag == 3:
            self.combobox_edge_detection.setEnabled(True)
            self.combobox_morph_reconstrction.setEnabled(False)
            self.combobox_gradient.setEnabled(False)
        elif self.morph_funs_flag == 4:
            self.combobox_edge_detection.setEnabled(False)
            self.combobox_morph_reconstrction.setEnabled(True)
            self.combobox_gradient.setEnabled(False)
        elif self.morph_funs_flag == 5:
            self.combobox_edge_detection.setEnabled(False)
            self.combobox_morph_reconstrction.setEnabled(False)
            self.combobox_gradient.setEnabled(True)


    def _init_threshold_ui(self):
        self.histgram_list, self.prob_list = ThresAlgo.Histgram(self.threshold_source_image)
        self.binary_image = ThresAlgo.Threshold(self.threshold_source_image, self.threshold)

        # set enable
        self.slider_threshold.setEnabled(True)
        self.line_edit_threshold.setEnabled(True)
        self.pushbutton_otsu.setEnabled(True)
        self.pushbutton_entropy.setEnabled(True)
        self.pushbutton_export.setEnabled(True)
        self.pushbutton_export_path_browser.setEnabled(True)

        # show images
        self.qitem_threshold_source_image, qscene_threshold_source_image = Utils.show_on_graphview(self.threshold_source_image)
        self.qitem_binary_image, qscene_binary_image = Utils.show_on_graphview(self.binary_image)

        self.graphics_view_source_image.setScene(qscene_threshold_source_image)
        self.graphics_view_binary_image.setScene(qscene_binary_image)

        self.graphics_view_source_image.fitInView(self.qitem_threshold_source_image, qc.Qt.KeepAspectRatio)
        self.graphics_view_binary_image.fitInView(self.qitem_binary_image, qc.Qt.KeepAspectRatio)

        # show histgram
        self._update_chart_histgram()

    def _init_filter_ui(self):
        # calculating
        self.forcalc_filter = FilterAlgo.CheckFilter(self.forshow_filter)
        self.filtered_image = FilterAlgo.Convolution(self.filter_source_image, self.forcalc_filter)
        self.filtered_image = FilterAlgo.CheckImage(self.filtered_image)

        # set enable
        self.frame_filters.setEnabled(True)

        # show images
        self.qitem_filter_source_image, qscene_filters_source_image = Utils.show_on_graphview(self.filter_source_image)
        self.qitem_filtered_image, qscene_filtered_image = Utils.show_on_graphview(self.filtered_image)

        self.graphics_view_source_image2.setScene(qscene_filters_source_image)
        self.graphics_view_filters_image.setScene(qscene_filtered_image)

        self.graphics_view_source_image2.fitInView(self.qitem_filter_source_image, qc.Qt.KeepAspectRatio)
        self.graphics_view_filters_image.fitInView(self.qitem_filtered_image, qc.Qt.KeepAspectRatio)

        # show kernal
        self._update_table_filter()

    def _init_morph_oper_ui(self):
        # set enable
        self.frame_morph_oper.setEnabled(True)
        self.frame_se_height.setEnabled(True)
        self.frame_se_width.setEnabled(True)
        self.pushbutton_set_origin.setEnabled(True)

        # show source image
        self.qitem_morph_oper_source_image, qscene_morph_oper_source_image = Utils.show_on_graphview(self.morph_oper_source_image)
        self.graphics_view_source_image3.setScene(qscene_morph_oper_source_image)
        self.graphics_view_source_image3.fitInView(self.qitem_morph_oper_source_image, qc.Qt.KeepAspectRatio)

        # show kernal
        self._update_table_se()
        self._update_morph_oper_image()

    def _init_morph_funs_ui(self):
        # assignment
        self.graphics_view_marker.image_width = self.morph_funs_source_image.shape[1]
        self.graphics_view_marker.image_height = self.morph_funs_source_image.shape[0]
        self.graphics_view_marker.mask = self.morph_funs_source_image
        self.graphics_view_marker.morph_funs_marker = np.zeros(self.morph_funs_source_image.shape)

        # set enable
        self.combobox_distance_trans_mode.setEnabled(True)
        self.groupbox_morph_funs_processing.setEnabled(True)

        # show source image
        self.qitem_morph_funs_source_image, qscene_morph_funs_source_image = Utils.show_on_graphview(self.morph_funs_source_image)
        self.graphics_view_source_image4.setScene(qscene_morph_funs_source_image)
        self.graphics_view_source_image4.fitInView(self.qitem_morph_funs_source_image, qc.Qt.KeepAspectRatio)

        # # show empty marker
        self._set_morph_funs_default_marker()

        # show
        self._update_morph_funs_widget_enabled()
        self._update_morph_funs_image()

    def _get_filter_table_item(self, value):
        qitem = qw.QTableWidgetItem()
        qitem.setText(str(value))
        qitem.setTextAlignment(qc.Qt.AlignCenter)
        qitem.setFont(qg.QFont('SimSun', self.filter_table_font_size))
        if value > 0:
            qitem.setBackground(qg.QBrush(qg.QColor(255, 255 - int(abs(value) / np.max(np.abs(self.forshow_filter[:])) * 255), 0, 128)))
        elif value < 0:
            qitem.setBackground(qg.QBrush(qg.QColor(255 -int(abs(value) / np.max(np.abs(self.forshow_filter[:])) * 255) , 255 -int(abs(value) / np.max(np.abs(self.forshow_filter[:])) * 255), 255, 64)))
        else:
            qitem.setBackground(qg.QBrush(qg.QColor(255, 255, 0, 64)))
        return qitem

    def _get_se_table_item(self, value, is_origin = False):
        qitem = qw.QTableWidgetItem()
        if value >= 0 and is_origin == False and self.forcalc_se.shape != (1, 1):
            qitem.setText(str(value))
            qitem.setTextAlignment(qc.Qt.AlignCenter)
            qitem.setFont(qg.QFont('SimSun', self.se_table_font_size))
            if value > 0:
                qitem.setBackground(qg.QBrush(qg.QColor(60, 60, 60)))
            elif value < 0:
                qitem.setBackground(qg.QBrush(qg.QColor(255, 255, 255)))
            else:
                qitem.setBackground(qg.QBrush(qg.QColor(230, 230, 230)))
        elif value == 1 and is_origin == True:
            qitem.setText('Ori')
            qitem.setTextAlignment(qc.Qt.AlignCenter)
            qitem.setFont(qg.QFont('SimSun', self.se_table_font_size))
            qitem.setBackground(qg.QBrush(qg.QColor(20, 20, 20)))
            qitem.setForeground(qg.QBrush(qg.QColor(230, 230, 230)))
        elif value == 0 and is_origin == True:
            qitem.setText('Ori')
            qitem.setTextAlignment(qc.Qt.AlignCenter)
            qitem.setFont(qg.QFont('SimSun', self.se_table_font_size))
            qitem.setBackground(qg.QBrush(qg.QColor(230, 230, 230)))
            qitem.setForeground(qg.QBrush(qg.QColor(60, 60, 60)))
        elif (value < 0 and is_origin == True) or self.forcalc_se.shape == (1, 1):
            self.se_origin = Config.DEFAULT_SE_ORIGIN
            self._update_table_se()
            self._update_morph_oper_image()
        return qitem

    def _mean_filter(self):
        self.filter_size = int(self.line_edit_filter_size.text())
        self.forshow_filter = FilterAlgo.CalcMeanFilter(self.filter_size)

    def _median_filter(self):
        self.filter_size = int(self.line_edit_filter_size.text())
        self.forshow_filter = np.zeros((self.filter_size, self.filter_size))

    def _gaussian_filter(self):
        self.filter_size = int(self.line_edit_filter_size.text())
        self.gaussian_sigma = float(self.line_edit_gaussian_sigma.text())
        self.forshow_filter = FilterAlgo.CalcGaussianFilter(self.filter_size, self.gaussian_sigma)

    def _user_definded_filter(self):
        self.filter_size = int(self.line_edit_filter_size.text())
        self.forshow_filter = np.ones((self.filter_size, self.filter_size))

    def _set_morph_funs_default_marker(self):
        self.graphics_view_marker.morph_funs_marker = Config.DEFAULT_IMAGE
        self.graphics_view_marker.qitem_morph_funs_marker, qscene_morph_funs_marker = Utils.show_on_graphview(self.graphics_view_marker.morph_funs_marker)
        self.graphics_view_marker.setScene(qscene_morph_funs_marker)
        self.graphics_view_marker.fitInView(self.graphics_view_marker.qitem_morph_funs_marker, qc.Qt.IgnoreAspectRatio)

    def _fit_view(self):
        if self.qitem_threshold_source_image is not None:
            self.graphics_view_source_image.fitInView(self.qitem_threshold_source_image, qc.Qt.KeepAspectRatio)
            self.graphics_view_binary_image.fitInView(self.qitem_binary_image, qc.Qt.KeepAspectRatio)
        if self.qitem_filter_source_image is not None:
            self.graphics_view_source_image2.fitInView(self.qitem_filter_source_image, qc.Qt.KeepAspectRatio)
            self.graphics_view_filters_image.fitInView(self.qitem_filtered_image, qc.Qt.KeepAspectRatio)
        if self.qitem_morph_oper_source_image is not None:
            self.graphics_view_source_image3.fitInView(self.qitem_morph_oper_source_image, qc.Qt.KeepAspectRatio)
            self.graphics_view_morph_oper_image.fitInView(self.qitem_morph_oper_image, qc.Qt.KeepAspectRatio)
        if self.qitem_morph_funs_source_image is not None:
            self.graphics_view_source_image4.fitInView(self.qitem_morph_funs_source_image, qc.Qt.KeepAspectRatio)
            self.graphics_view_morph_funs_image.fitInView(self.qitem_morph_funs_image, qc.Qt.KeepAspectRatio)
        if self.graphics_view_marker.qitem_morph_funs_marker is not None:
            self.graphics_view_marker.fitInView(self.graphics_view_marker.qitem_morph_funs_marker, qc.Qt.IgnoreAspectRatio)

class SendToWindow(qw.QDialog, Ui_Dialog):
    def __init__(self):
        super(SendToWindow, self).__init__()
        self.setupUi(self)

        self.selected_tab = 0
        self.radiobutton_threshold.released.connect(self.slot_radiobutton_threshold)
        self.radiobutton_filters.released.connect(self.slot_radiobutton_filters)
        self.radiobutton_morph_operation.released.connect(self.slot_radiobutton_morph_operation)
        self.radiobutton_morph_function.released.connect(self.slot_radiobutton_morph_function)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def slot_radiobutton_threshold(self):
        self.selected_tab = 0

    def slot_radiobutton_filters(self):
        self.selected_tab = 1

    def slot_radiobutton_morph_operation(self):
        self.selected_tab = 2

    def slot_radiobutton_morph_function(self):
        self.selected_tab = 3


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())