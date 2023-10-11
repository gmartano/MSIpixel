# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:51:21 2022

@author: Giuseppe Martano
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns


class Ui_Form(object):
    def setupUi(self, Form, df):
        self.df = df
        Form.setObjectName("Spatial correlation analysis")
        Form.resize(747, 624)

        Form.setWindowFlags(Form.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        x = sns.clustermap(self.df, metric="correlation", square=True, yticklabels=True, xticklabels=True)
        canvas = FigureCanvas(x.figure)
        self.toolbar = NavigationToolbar(canvas)
        self.gridLayout.addWidget(self.toolbar)
        canvas.draw()
        self.gridLayout.addWidget(canvas)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Correlation map"))
        Form.setWindowIcon(QtGui.QIcon('msipixel_icon_exe.ico'))