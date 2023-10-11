# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:51:21 2022

@author: Giuseppe Martano
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import func
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import matplotlib.path as mpltPath
import numpy as np
import pandas as pd


class Ui_Form(object):
    def setupUi(self, Form, all_eim):
        Form.setObjectName("Form")
        Form.resize(715, 748)
        #Form.setStyleSheet("background-color: rgb(160, 160, 160);")
        Form.setWindowFlags(Form.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
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
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMaximumSize(QtCore.QSize(360, 16777215))
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(self.widget_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget, 0, 0, 1, 1)
        
        self.widget_4 = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        
        self.widget = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(360, 160))
        self.widget.setMaximumSize(QtCore.QSize(360, 160))
        self.widget.setObjectName("widget")
        
        self.widget_3 = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 3, 1)
        self.gridLayout_2.addWidget(self.widget_3, 0, 1, 3, 1)
        self.gridLayout_2.addWidget(self.widget_4, 3, 1, 1, 1)
        
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(5, 40, 90, 31))
        #self.pushButton.setStyleSheet("border-radius : 10;\n" "background-color: rgb(255, 212, 37);")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(140, 0, 91, 41))
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(100, 40, 151, 31))
        #self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setGeometry(QtCore.QRect(260, 40, 50, 31))
        #self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setGeometry(QtCore.QRect(310, 40, 40, 31))
        #self.spinBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.spinBox.setValue(5)
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName("comboBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(5, 80, 90, 31))
        #self.pushButton_2.setStyleSheet("border-radius : 10;\n" "background-color: rgb(255, 212, 37);")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.widget)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 80, 151, 31))
        #self.comboBox_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 80, 90, 31))
        #self.pushButton_3.setStyleSheet("border-radius : 10;\n" "background-color: rgb(255, 212, 37);")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(5, 120, 345, 31))
        #self.pushButton_4.setStyleSheet("border-radius : 10;\n" "background-color: rgb(255, 212, 37);")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.color = ('black','red', 'green', 'blue')
        self.comboBox.addItems(self.color)
        self.line_color = self.comboBox.currentText()
        self.comboBox.currentTextChanged.connect(self.update_line_color)
        self.pushButton_2.setEnabled(False)
        
        self.all_eim = all_eim
        self.row = 0
        self.ran_int = 0
        self.r_arr = func.plot_data(self.all_eim[0,2])
        self.active = [None, None, None, None]
        self.populate_table()
        self.create_boxplot()
        self.create_mdi()
        self.pushButton.clicked.connect(self.add_roi_to_list)
        self.pushButton_2.clicked.connect(self.line_drawer)
        self.ROI_list = []
        self.selected_ROIs = []
        self.selected_boxplot = []
        self.retranslateUi(Form)
        self.linewidth = self.spinBox.value()
        self.spinBox.valueChanged.connect(self.update_linewidth)
        self.comboBox_2.currentTextChanged.connect(self.check_pushbutton_2_is_enable)
        self.pushButton_3.clicked.connect(self.delete_ROI_with_push)
        self.pushButton_4.clicked.connect(self.export_pixels)
        
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    def export_pixels(self):
        if len(self.selected_boxplot) > 0:
            col_names = np.array(['Pixel', 'MS2', 'Label', 'Score'])
            col_names = col_names.reshape(2,2)
            compound_array = np.array([[i[2:-2],k] for i,k in self.all_eim[:,3:]])
            pixel_names = []
            pixels_arr = []
            for k in self.selected_boxplot:
                group = k[0]
                pixels = [f"Pixel({i};{g})" for i,g in k[2]]
                for i in pixels:
                    pixel_names.append([i, group])
                pixels_arr += [[j,g] for j,g in k[2]]
            pixel_names = np.array(pixel_names).transpose()
            col_names = np.c_[col_names, pixel_names]
            row_values = np.zeros((0,len(pixels_arr)))
            for i in range (len(self.all_eim)):
                imz = self.all_eim[i, 2]
                array = func.plot_data(imz)
                single_row = np.array([array[g,k] for k,g in pixels_arr])
                single_row = single_row.reshape(1,len(single_row))
                row_values = np.concatenate((row_values, single_row))
            compound_array = np.c_[compound_array, row_values]
            col_names = np.concatenate((col_names, compound_array))
            col_names = pd.DataFrame(col_names)
            save_path = QtWidgets.QFileDialog.getSaveFileName(None, "Save TXT file as", "", ".xlsx(*.xlsx)")[0]
            col_names.to_excel(save_path, header=False, index=False)
    
    def decorate_mdi(self):
        imz = self.all_eim[self.row,2]
        self.r_arr = func.plot_data(imz)
        if len(self.selected_boxplot) > 0:
            for k in range(len(self.selected_boxplot)):
                pixels = []
                for i in self.selected_boxplot[k][2]:
                    if self.r_arr[i[1], i[0]] > 0:
                        pixels.append(self.r_arr[i[1], i[0]])
                self.selected_boxplot[k][1] = pixels
            self.decorate_boxplot()
        self.r.clear()
        self.r.imshow(self.r_arr, cmap='Greys_r', aspect='equal', label="Red")
        for i in self.selected_ROIs:
            x = [int(p[0]) for p in i[3]]
            y = [int(p[1]) for p in i[3]]
            self.r.plot(x, y, color=i[1], linewidth=i[2])
            self.canvas.draw()
        self.canvas.draw()
    
    def extract_pixels(self, lines):
        path = mpltPath.Path(lines)
        xy = []
        for x in range(self.r_arr.shape[1]):
            for y in range(self.r_arr.shape[0]):
                xy.append([x,y])
        x = path.contains_points(xy)
        xy = np.array(xy)
        empty_pixels = xy[x]
        pixels = []
        for i in empty_pixels:
            if self.r_arr[i[1], i[0]] > 0:
                pixels.append(self.r_arr[i[1], i[0]])
        self.selected_boxplot.append([self.comboBox_2.currentText(), pixels, empty_pixels])
        self.decorate_boxplot()
        self.selected_ROIs = [i for i in self.selected_ROIs]
        self.decorate_mdi()
        for i in self.selected_ROIs:
            x = [int(p[0]) for p in i[3]]
            y = [int(p[1]) for p in i[3]]
            self.r.plot(x, y, color=i[1], linewidth=i[2])
            self.canvas.draw()
    
    def decorate_boxplot(self):
        self.box.clear()
        if len(self.selected_boxplot) > 0:
            y = []
            x = []
            for i in self.selected_boxplot:
                y.append(i[1])
                x.append(i[0])
            self.box.boxplot(y, notch=True, sym="o", labels=x)
        self.box_canvas.draw()
    
    def delete_ROI_with_push(self):
        name_to_delete = self.comboBox_2.currentText()
        self.delete_ROI(name_to_delete)
    
    def delete_ROI(self, name_to_delete):
        self.selected_boxplot = [i for i in self.selected_boxplot if name_to_delete not in i]
        self.decorate_boxplot()
        if len(self.ROI_list) > 1:
            self.ROI_list = self.ROI_list[self.ROI_list != name_to_delete]
            if type(self.ROI_list) == str:
                self.ROI_list = [self.ROI_list]
            
            self.comboBox_2.clear()
            self.comboBox_2.addItems(self.ROI_list)
        else:
            self.ROI_list = []
            self.comboBox_2.clear()
        self.pushButton_2.setEnabled(False)
        self.selected_ROIs = [i for i in self.selected_ROIs if name_to_delete not in i]
        self.decorate_mdi()
        for i in self.selected_ROIs:
            x = [int(p[0]) for p in i[3]]
            y = [int(p[1]) for p in i[3]]
            self.r.plot(x, y, color=i[1], linewidth=i[2])
            self.canvas.draw()
        
    
    def check_pushbutton_2_is_enable(self):
        self.pushButton_2.setEnabled(True)
        for i in self.selected_ROIs:
            if self.comboBox_2.currentText() == i[0]:
                self.pushButton_2.setEnabled(False)
        
    def update_line_color(self):
        self.line_color = self.comboBox.currentText()
        
    def create_boxplot(self):
        self.box_figure = plt.figure()
        self.box = self.box_figure.add_subplot(1,1,1, label="Gray")
        self.box.boxplot([])
        sub = QtWidgets.QVBoxLayout(self.widget_4)
        self.box_canvas = FigureCanvasQTAgg(self.box_figure)
        sub.addWidget(self.box_canvas)
    
    def update_linewidth(self):
        self.linewidth = self.spinBox.value()
    
    def add_roi_to_list(self):
        self.group_name = self.textEdit.toPlainText()
        if self.group_name == "":
            self.ran_int += 1
            self.group_name = f"Group_{self.ran_int}"
        elif self.group_name in self.ROI_list:
            self.ran_int += 1
            self.group_name = f"{self.group_name}_{self.ran_int}"
        self.ROI_list.append(str(self.group_name))
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.ROI_list)
        self.comboBox_2.setCurrentText(self.ROI_list[-1])
        self.pushButton_2.setEnabled(True)
        
    def populate_table(self):
        self.tableWidget.setRowCount(self.all_eim.shape[0]) 
        self.tableWidget.setColumnCount(2)
        for i in range(self.all_eim.shape[0]):
            for k in range(2):
                if k == 0:
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                  QtCore.Qt.ItemIsEnabled)
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    string = str(self.all_eim[i,3])
                    for q in ["[", "]", "'"]:
                        string = str.replace(string, q, "")
                    item = QtWidgets.QTableWidgetItem(string)
                self.tableWidget.setItem(i, k, item)
        self.tableWidget.setHorizontalHeaderLabels(["", "Name"])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.itemClicked.connect(self.handleItemClicked)
    
    def handleItemClicked(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.row, self.column = item.row(), item.column()
            self.decorate_mdi()
            if self.active[item.column()] == None:
                self.active[item.column()] = item.row()
            else:
                self.tableWidget.item(self.active[item.column()], item.column()).setCheckState(QtCore.Qt.Unchecked)
                self.active[item.column()] = item.row()
        else:
            if self.active[item.column()] != None:
                self.tableWidget.item(self.active[item.column()], item.column()).setCheckState(QtCore.Qt.Unchecked)
                self.active[item.column()] = None
        if item.checkState() == QtCore.Qt.Unchecked:
            self.active[item.column()] = None
        else:
            pass
    
        
    def line_drawer(self):
        self.pushButton_2.setEnabled(False)
        col = self.line_color
        linwidth = self.linewidth
        plt.gca()
        xy = [(-1,-1)]
        start = plt.ginput(1)
        stop = []
        for i in range(int(start[0][0])-1, int(start[0][0])+2):
            for k in range(int(start[0][1])-1, int(start[0][1])+2):
                stop.append([i,k])
        lines = [[int(i) for i in start[0]]]
        while [int(i) for i in xy[0]] not in stop:
            xy = plt.ginput(1)
            if len(lines) > 2:
                if [int(i) for i in xy[0]] in stop:
                    xy = start
            lines.append([int(i) for i in xy[0]])
            x = [int(p[0]) for p in lines[-2:]]
            y = [int(p[1]) for p in lines[-2:]]
            plt.plot(x,y, color=col, linewidth=linwidth)
            self.canvas.draw()
        self.selected_ROIs.append([self.comboBox_2.currentText(), self.line_color, self.linewidth, lines])
        self.extract_pixels(lines)
        
        
    def create_mdi(self):
        self.figure = plt.figure()
        self.r = self.figure.add_subplot(1,1,1, label="Gray")
        self.r.imshow(self.r_arr, cmap='Greys_r', aspect='equal')
        sub = QtWidgets.QVBoxLayout(self.widget_3)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        sub.addWidget(self.toolbar)
        sub.addWidget(self.canvas)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Pixel analysis"))
        Form.setWindowIcon(QtGui.QIcon('msipixel_icon_exe.ico'))
        self.pushButton.setText(_translate("Form", "Add Group"))
        self.label.setText(_translate("Form", "Group name"))
        self.pushButton_2.setText(_translate("Form", "Draw"))
        self.pushButton_3.setText(_translate("Form", "Delete"))
        self.pushButton_4.setText(_translate("Form", "Export Pixel Groups"))
