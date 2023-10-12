# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:51:21 2022

@author: Giuseppe Martano
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import func
from molmass import Formula as mf
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET


def getEV(mzml_path, index, root):
    
    for x in root:
        if x.tag.endswith("mzML"):
            for x in x:
                if x.tag.endswith("run"):
                    for x in x:
                        if x.tag.endswith("spectrumList"):
                            for x in x:
                                if x.attrib['index'] == str(index):
                                    for x in x:
                                        if x.tag.endswith("precursorList"):
                                            for x in x:
                                                for x in x:
                                                    if x.tag.endswith("activation"):
                                                        for x in x:
                                                            if x.attrib["name"] == "collision energy":
                                                                return x.attrib["value"]


def get_eix(ms1, compound, ppm):
    prec = compound
    delta = prec*ppm/1000000
    eic = func.mzrange(ms1, prec-delta, prec+delta)
    return eic

class Ui_Form(object):
    def setupUi(self, Form, mzml):
        self.mzml = mzml
        self.index_ms = None
        
        self.ms2 = func.transform_data_manual(self.mzml)
        self.ms1, self.ms2 = func.msn_split(self.ms2)
        self.root = ET.parse(self.mzml).getroot()
        
        Form.setObjectName("Manual Inspection")
        Form.resize(1020, 980)
        Form.setWindowFlags(Form.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        
        Form.setSizePolicy(sizePolicy)

        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget_2 = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)

        self.widget_2.setObjectName("widget_2")
        
        
        
        self.widget = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())        
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(1, 1))

        self.widget.setObjectName("widget")
        
        self.widget_3 = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QtCore.QSize(1, 1))

        self.widget_3.setObjectName("widget_3")
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 2)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_3, 1, 1, 1, 1)
        self.widget_4 = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QtCore.QSize(300, 105))
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 100))

        self.widget_4.setObjectName("widget_4")
        self.textEdit_3 = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit_3.setEnabled(False)
        self.textEdit_3.setGeometry(QtCore.QRect(0, 30, 80, 31))
        self.textEdit_3.setObjectName("textEdit_3")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 30, 135, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.textEdit_4 = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit_4.setEnabled(False)
        self.textEdit_4.setGeometry(QtCore.QRect(215, 30, 135, 31))
        self.textEdit_4.setObjectName("textEdit_4")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_3.setGeometry(QtCore.QRect(350, 30, 135, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.comboBox = QtWidgets.QComboBox(self.widget_4)
        self.comboBox.setGeometry(QtCore.QRect(485, 30, 80, 31))
        self.comboBox.setObjectName("comboBox")

        self.textEdit = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit.setEnabled(False)
        self.textEdit.setGeometry(QtCore.QRect(565, 30, 80, 31))
        self.textEdit.setObjectName("textEdit")

        self.lineEdit = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit.setGeometry(QtCore.QRect(645, 30, 80, 31))
        self.lineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEdit.setObjectName("lineEdit")

        self.textEdit_2 = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit_2.setEnabled(False)
        self.textEdit_2.setGeometry(QtCore.QRect(725, 30, 80, 31))
        self.textEdit_2.setObjectName("textEdit_2")


        self.spinBox = QtWidgets.QSpinBox(self.widget_4)
        self.spinBox.setGeometry(QtCore.QRect(805, 30, 80, 30))
        self.spinBox.setProperty("value", 5)
        self.spinBox.setObjectName("spinBox")
        
        self.pushButton = QtWidgets.QPushButton(self.widget_4)
        self.pushButton.setDefault(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setGeometry(QtCore.QRect(890, 30, 121, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)

        self.pushButton.setObjectName("pushButton")
        self.textEdit_5 = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit_5.setEnabled(False)
        self.textEdit_5.setGeometry(QtCore.QRect(0, 70, 80, 31))

        self.textEdit_5.setObjectName("textEdit_5")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_4.setGeometry(QtCore.QRect(80, 70, 135, 31))

        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_5.setGeometry(QtCore.QRect(300, 70, 300, 31))

        self.lineEdit_5.setObjectName("lineEdit_5")
        self.textEdit_6 = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit_6.setEnabled(False)
        self.textEdit_6.setGeometry(QtCore.QRect(220, 70, 80, 31))

        self.textEdit_6.setObjectName("textEdit_6")
        
        ### End GUI from QT Designer
        self.textEdit_3.setText("Name")
        self.textEdit_4.setText("Chemical formula")
        self.textEdit_2.setText("ppm")
        self.textEdit.setText(("m/z"))
        self.decorate_msms()
        self.tableWidget = QtWidgets.QTableWidget(self.widget_2)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 3)
        self.gridLayout_2.addWidget(self.widget_2, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_3, 2, 1, 1, 2)
        self.gridLayout_2.addWidget(self.widget_4, 3, 0, 1, 3)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        
        self.ppm = self.spinBox.value()

        self.precursor = 0
        self.spinBox.valueChanged.connect(self.update_ppm)
        self.populate_comboBox()
        self.adduct = self.comboBox.currentIndex()
        self.comboBox.currentTextChanged.connect(self.update_comboBox_index)
        self.lineEdit_3.returnPressed.connect(self.monoisotopic_mass)
        self.formula = self.lineEdit_3.text()
        self.lineEdit.editingFinished.connect(self.mass_to_picture)
        self.pushButton.setText("Export")
        self.pushButton.clicked.connect(self.export_msms)
        self.hmdb_id = None
        self.lineEdit_4.editingFinished.connect(self.new_hmdb_id)
        self.inchlkey = None
        self.lineEdit_5.editingFinished.connect(self.new_inchlkey)
        self.active_row = None
        self.tableWidget.itemClicked.connect(self.handleItemClicked)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    def new_hmdb_id(self):
        self.hmdb_id = self.lineEdit_4.text()
    
    def new_inchlkey(self):
        self.inchlkey = self.lineEdit_5.text()
        
    def export_msms(self):
        if self.index_ms != None:
            name = self.lineEdit_2.text()
            mf = self.lineEdit_3.text()
            mz = self.index_ms[4]
            intensities = self.index_ms[5]
            polarity = self.index_ms[6]
            lib = np.array([name, self.hmdb_id, mf, self.inchlkey, mz, intensities, self.eV, polarity], dtype=object).reshape(1,8)
            save_path = QtWidgets.QFileDialog.getSaveFileName(None, "Save library file as .npy", "", ".npy(*.npy)")[0]
            np.save(save_path, lib)
            self.index_ms = None
            
        
    def monoisotopic_mass(self):
        self.formula = self.lineEdit_3.text()
        try:
            self.mz = mf(self.formula).monoisotopic_mass + self.adducts[self.adduct,1]
            self.lineEdit.setText(str(np.round(self.mz, 5)))
            self.mass_to_picture()
        except:
            pass
    
    def mass_to_picture(self):
        self.precursor = float(self.lineEdit.text())
        ppm_mz = self.precursor*self.ppm/1000000
        self.msms = self.ms2[(self.ms2[:,2] > self.precursor - ppm_mz)&(self.ms2[:,2] < self.precursor + ppm_mz)]
        true_values = [len(i[5]) > 1 for i in self.msms]
        self.msms = self.msms[true_values]
        self.populate_table()
        self.active_row = None
        self.figure.clear()
        self.figure2.clear()
        ax = self.figure2.add_subplot(111)
        eix = get_eix(self.ms1, self.precursor, self.ppm)
        for i in range(len(eix)):
            eix[i,5] = sum(eix[i,5])
        ax.plot(eix[:,3]/60, eix[:,5])
        ax.set_title(f"Extracted ion chromatogram: {self.precursor}")
        self.canvas2.draw()
    
    def populate_table(self):
        self.tableWidget.clearContents()
        if len(self.msms) > 0:
            self.tableWidget.setRowCount(self.msms.shape[0]) 
            self.tableWidget.setColumnCount(2)
            for i in range(self.msms.shape[0]):
                for k in range(1,4):
                    if k == 1:
                        item = QTableWidgetItem()
                        item.setFlags(Qt.ItemIsUserCheckable |
                                      Qt.ItemIsEnabled)
                        item.setCheckState(Qt.Unchecked)
                    else:
                        item = QTableWidgetItem(str(self.msms[i,k])[:10])
                    self.tableWidget.setItem(i, k-1, item)
            self.tableWidget.setHorizontalHeaderLabels(["Select", "Precursor", "Time"])
            self.tableWidget.verticalHeader().setVisible(False)
            
    
    def handleItemClicked(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            if self.active_row == None:
                pass
            else:
                self.tableWidget.item(self.active_row, 0).setCheckState(QtCore.Qt.Unchecked)
            self.row = item.row()
            self.active_row = item.row()
            self.populate_msms_imd()
        else:
            try:
                self.tableWidget.item(self.active_row, 0).setCheckState(QtCore.Qt.Unchecked)
                self.active_row = None
            except:
                pass
    
    def decorate_msms(self):
        self.figure = plt.figure()
        sub = QtWidgets.QVBoxLayout(self.widget_3)
        self.canvas = FigureCanvasQTAgg(self.figure)
        sub.addWidget(self.canvas)
        
        ### figure MSI
        self.figure2 = plt.figure()
        sub = QtWidgets.QVBoxLayout(self.widget)
        self.canvas2 = FigureCanvasQTAgg(self.figure2)
        sub.addWidget(self.canvas2)
        
    def populate_msms_imd(self):
        self.index_ms = self.msms[self.row]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.eV = getEV(self.mzml, self.index_ms[0], self.root)
        ax.set_title(f"MS/MS acquired at {str(self.index_ms[3])[:5]}. Collision Energy {self.eV}")
        ax.stem(self.index_ms[4], self.index_ms[5], 'b', markerfmt="")
        
        self.canvas.draw()
        
    
    def update_ppm(self):
        self.ppm = self.spinBox.value()
        if self.precursor > 0:
            self.mass_to_picture()
    
    def update_comboBox_index(self):
        self.adduct = self.comboBox.currentIndex()
        if len(self.formula) > 0:
            self.monoisotopic_mass()
    
    def populate_comboBox(self):
        self.adducts = np.array([["H", 1.007276452320935, "+"], ["Na", 22.989220702090936, "+"],
                            ["-H", -1.007276452320935, "-"],["Cl", 34.96940126190906, "-"]], dtype=object)
        if self.ms1[0,6] == "+":
            self.adducts = self.adducts[self.adducts[:,2] == "+"]
        else:
            self.adducts = self.adducts[self.adducts[:,2] == "-"]
        for i in self.adducts[:,0]:
            self.comboBox.addItem(i)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Manual Inspection"))
        Form.setWindowIcon(QtGui.QIcon('msipixel_icon_exe.ico'))
        self.textEdit_3.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Name</span></p></body></html>"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">m/z</span></p></body></html>"))
        self.textEdit_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">ppm</span></p></body></html>"))
        self.textEdit_4.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Chemical Formula</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Create Library file"))
        self.textEdit_5.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">HMBD ID</span></p></body></html>"))
        self.textEdit_6.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">InChl Key</span></p></body></html>"))
