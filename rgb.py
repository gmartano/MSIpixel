# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:51:21 2022

@author: Giuseppe Martano
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import func
import numpy as np
import matplotlib


class Ui_rgb_plot(QWidget):
    def setupUi(self, rgb_plot, all_eim):
        self.all_eim = all_eim
        self.r_arr = func.plot_data(self.all_eim[0,2])
        self.g_arr = func.plot_data(self.all_eim[0,2])
        self.b_arr = func.plot_data(self.all_eim[0,2])
        self.active = [None, None, None, None]
        
        rgb_plot.setObjectName("rgb_plot")
        rgb_plot.resize(893, 679)
        #rgb_plot.setStyleSheet("background-color: rgb(160, 160, 160);")
        rgb_plot.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        rgb_plot.setWindowFlags(rgb_plot.windowFlags() | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)
        self.gridLayout_2 = QtWidgets.QGridLayout(rgb_plot)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(rgb_plot)
        self.widget.setObjectName("widget")
        self.gridLayout_2.addWidget(self.widget, 0, 1, 1, 1)
        self.frame = QtWidgets.QFrame(rgb_plot)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(350, 0))
        self.frame.setMaximumSize(QtCore.QSize(350, 16777215))
        self.frame.setObjectName("frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)

        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(102)
        self.gridLayout_5.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.populate_table()
        self.row, self.column = 0, 0
        
        self.cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',['none','red'],256)
        self.cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',['none','green'],256)
        self.cmap3 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',['none','blue'],256)
        self.create_mdi()
        for i in range(3):
            self.decorate_mdi()
            self.column +=1
        self.retranslateUi(rgb_plot)
        QtCore.QMetaObject.connectSlotsByName(rgb_plot)
        
    
    def populate_table(self):
        self.tableWidget.setRowCount(self.all_eim.shape[0]) 
        self.tableWidget.setColumnCount(4)
        for i in range(self.all_eim.shape[0]):
            for k in range(4):
                if k < 3:
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsUserCheckable |
                                  Qt.ItemIsEnabled)
                    item.setCheckState(Qt.Unchecked)
                else:
                    string = str(self.all_eim[i,3])
                    for q in ["[", "]", "'"]:
                        string = str.replace(string, q, "")
                    item = QTableWidgetItem(string)
                self.tableWidget.setItem(i, k, item)
        self.tableWidget.setHorizontalHeaderLabels(["R", "G", "B", "Name"])
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
    
    def decorate_mdi(self):
        imz = self.all_eim[self.row,2]
        if self.column == 0:
            self.r_arr = func.plot_data(imz)
            self.r.clear()
            self.r.imshow(self.r_arr, cmap='Reds_r', aspect='equal', label="Red")
        elif self.column == 1:
            self.g_arr = func.plot_data(imz)
            self.g.clear()
            self.g.imshow(self.g_arr, cmap='Greens_r', aspect='equal', label="Green")
        elif self.column == 2:
            self.b_arr = func.plot_data(imz)
            self.b.clear()
            self.b.imshow(self.b_arr, cmap='Blues_r', aspect='equal', label="Blue")
        self.decorate_rgb()
        self.canvas.draw()
    
    def decorate_rgb(self):
        
        self.rgb.clear()
        self.rgb.imshow(self.r_arr, cmap=self.cmap1, alpha=0.8, interpolation='none', aspect='equal', label="Red")
        self.rgb.imshow(self.g_arr, cmap=self.cmap2 , alpha=0.8, interpolation='none', aspect='equal', label="Green")
        self.rgb.imshow(self.b_arr, cmap=self.cmap3 , alpha=0.8, interpolation='none', aspect='equal', label="Blue")
        
        
            
    def create_mdi(self):
        self.figure = plt.figure()
        self.r = self.figure.add_subplot(2,2,1, label="Red")
        self.g = self.figure.add_subplot(2,2,2, label="Green")
        self.b = self.figure.add_subplot(2,2,3, label="Blue")
        self.rgb = self.figure.add_subplot(2,2,4, label="RGB")
        self.r.imshow(self.r_arr, cmap='Reds_r', aspect='equal')
        self.g.imshow(self.g_arr, cmap='Greens_r', aspect='equal')
        self.b.imshow(self.b_arr, cmap='Blues_r', aspect='equal')
        self.rgb.imshow(self.r_arr, cmap='Reds_r', aspect='equal')
        sub = QtWidgets.QVBoxLayout(self.widget)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        sub.addWidget(self.toolbar)
        sub.addWidget(self.canvas)


    def retranslateUi(self, rgb_plot):
        _translate = QtCore.QCoreApplication.translate
        rgb_plot.setWindowTitle(_translate("rgb_plot", "RGB Plotter"))
        rgb_plot.setWindowIcon(QtGui.QIcon('msipixel_icon_exe.ico'))

