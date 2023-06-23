# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:26:41 2022

@author: giuse
"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import numpy as np
import os
import func
import pandas as pd

class Explore(QWidget):
    def __init__(self, ms2, eic, eim, df, store_folder):
        self.ms2 = ms2
        self.ms2_new = ms2
        self.kill_index = []
        self.store_folder = store_folder
        self.eic = eic
        self.eim = eim
        self.df = df
        super().__init__()
        self.setWindowTitle("Annotated compounds")
        self.setWindowIcon(QIcon('msipixel_icon_exe.ico'))
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        self.layout.addWidget(self.label)
        self.add_mdi_table()
        self.add_mdi_picture()
        
        self.setLayout(self.layout)
        self.b2 = QPushButton("Overwrite annotation list")
        self.layout.addWidget(self.b2)
        self.b2.clicked.connect(self.overwrite_annotation_list)
        self.b1 = QPushButton("Export results")
        self.layout.addWidget(self.b1)
        self.b1.clicked.connect(self.export_results)
    
    def export_results(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")[0]
        col_names = ["id", "Name", "HMDB", "mf", "InchKey", "mw", "mz", "adduct", "charge", "polarity", "Cosine similarity"]
        table_columns_index = [0, 8, 9, 10, 11, 1, 2, 3, 4, 5, 7]
        file_to_save = [self.ms2_new[:,i] for i in table_columns_index]
        file_to_save = np.array(file_to_save).transpose()
        df = pd.DataFrame(file_to_save, columns=col_names)
        df.to_excel(filename, index=False)
        
    
    def add_mdi_table(self):
        table_columns_index = [0, 8, 9, 10, 11, 1, 2, 3, 4, 5, 7]
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.ms2.shape[0]) 
        self.tableWidget.setColumnCount(len(table_columns_index)+1)
        self.tableWidget.setSortingEnabled(True)
        for i in range(self.ms2.shape[0]):
            for k in range(len(table_columns_index)):
                self.tableWidget.setItem(i, k, QTableWidgetItem(str(self.ms2[i,table_columns_index[k]])))
            self.tableWidget.setItem(i, 11, QTableWidgetItem(str(i)))
        self.tableWidget.setHorizontalHeaderLabels(["id", "Name", "HMDB", "mf", "InchKey", "mw", "mz", "adduct", "charge", "polarity", "Cosine similarity", "or_index"])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.hideColumn(11)
        self.tableWidget.viewport().installEventFilter(self)
        self.tableWidget.resizeColumnsToContents()
        self.layout.addWidget(self.tableWidget)
    
    def add_mdi_picture(self):
        
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                index = self.tableWidget.indexAt(event.pos())
                if index.data():
                    self.build_MSMS_plot(index.row())
            elif event.button() == Qt.RightButton:
                index = self.tableWidget.indexAt(event.pos())
                if index.isValid():
                    self.index_to_be_delete = index.row()
                    self.setContextMenuPolicy(Qt.CustomContextMenu)
                    self.customContextMenuRequested.connect(self.right_menu)
        return super().eventFilter(source, event)
    
    def build_MSMS_plot(self, row_index):
        row_index = int(self.tableWidget.item(row_index,11).text())
        index_ms = self.ms2[row_index]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title(f"Precursor {np.round(index_ms[2], 5)}: Best library score {np.round(index_ms[7]*100, 2)}%")
        ax.stem(index_ms[16], index_ms[17]/max(index_ms[17]), 'b', markerfmt="", label="empiric")
        ax.stem(index_ms[12], -index_ms[13]/max(index_ms[13]), 'r', markerfmt="", label="library")
        ax.legend()
        self.canvas.draw()
    
    def right_menu(self, pos):
        menu = QMenu()
        # Add menu options
        delete = menu.addAction(f'Delete row')

        # Menu option events
        delete.triggered.connect(self.delete_menu)

        # Position
        menu.exec_(self.mapToGlobal(pos))
    
    def delete_menu(self):
        self.tableWidget.hideRow(self.index_to_be_delete)
        self.kill_index.append(int(self.tableWidget.item(self.index_to_be_delete,11).text()))
    
    def overwrite_annotation_list(self):
        self.ms2_new, self.eic, self.eim, self.df = func.ms2_manual_filtering(self.ms2, self.eic, self.eim, self.df, self.kill_index)
        np.save(os.path.join(self.store_folder, "ms2.npy"), self.ms2_new)
        np.save(os.path.join(self.store_folder, "all_eic.npy"), self.eic)
        np.save(os.path.join(self.store_folder, "all_eim.npy"), self.eim)
        self.df.to_pickle(os.path.join(self.store_folder, "df.pkl"))
        '''
        self.new_ms2 = []
        for i in range(len(self.ms2)):
            if i not in self.kill_index:
                self.new_ms2.append(self.ms2[i])
        self.new_ms2 = np.array(self.new_ms2, dtype=object)
        np.save(os.path.join(self.store_folder, "ms2.npy"), self.new_ms2)
        '''
    
    
        
        