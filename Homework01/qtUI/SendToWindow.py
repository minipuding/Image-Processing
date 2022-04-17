# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SendToWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(246, 217)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radiobutton_threshold = QtWidgets.QRadioButton(self.frame)
        self.radiobutton_threshold.setObjectName("radiobutton_threshold")
        self.verticalLayout.addWidget(self.radiobutton_threshold)
        self.radiobutton_filters = QtWidgets.QRadioButton(self.frame)
        self.radiobutton_filters.setObjectName("radiobutton_filters")
        self.verticalLayout.addWidget(self.radiobutton_filters)
        self.radiobutton_morph_operation = QtWidgets.QRadioButton(self.frame)
        self.radiobutton_morph_operation.setObjectName("radiobutton_morph_operation")
        self.verticalLayout.addWidget(self.radiobutton_morph_operation)
        self.radiobutton_morph_function = QtWidgets.QRadioButton(self.frame)
        self.radiobutton_morph_function.setObjectName("radiobutton_morph_function")
        self.verticalLayout.addWidget(self.radiobutton_morph_function)
        self.gridLayout.addWidget(self.frame, 1, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 5)
        self.gridLayout.setRowStretch(2, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Send current output image to \n"
"other page as input image."))
        self.radiobutton_threshold.setText(_translate("Dialog", "Threshold"))
        self.radiobutton_filters.setText(_translate("Dialog", "Filters"))
        self.radiobutton_morph_operation.setText(_translate("Dialog", "Morph Operation"))
        self.radiobutton_morph_function.setText(_translate("Dialog", "Morph Function"))

