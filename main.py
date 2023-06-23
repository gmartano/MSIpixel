# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:51:21 2022

@author: giuse
"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import numpy as np
import psutil
import multiprocessing as mp
from scipy.stats import ks_2samp
import pandas as pd
import pyarrow
import fastparquet

from zipfile import ZipFile
import xml.etree.ElementTree as ET

import func
import mainWindow
import manual_inspection
import rgb
import infusion
import clustermap
import sys
import ROI

w_dir = os.path.dirname(__file__)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)

class Main(QMainWindow):
    progressChanged = pyqtSignal(int)
    progressChanged2 = pyqtSignal(bool)
    progressChanged3 = pyqtSignal(bool)
    progressChanged_2 = pyqtSignal(int)
    progressChanged_22 = pyqtSignal(bool)
    progressChanged_23 = pyqtSignal(bool)
    progressChanged_3 = pyqtSignal(int)
    progressChanged_32 = pyqtSignal(bool)
    progressChanged_33 = pyqtSignal(bool)
    buttonRename = pyqtSignal(str)
    activateProcess_inf = pyqtSignal(bool)
    activateExplore_inf = pyqtSignal(bool)
    progressChanged_spat = pyqtSignal(int)
    progressChange_vis = pyqtSignal(bool)
    progressChanged_check = pyqtSignal(bool)
    activateProcess_spat = pyqtSignal(bool)
    activateProcess_spat2 = pyqtSignal(bool)
    emit_warning = pyqtSignal(str)
    activateProcess_rgb = pyqtSignal(bool)
    progressChanged_hmdb = pyqtSignal(int)
    progressChanged_hmdb_vis = pyqtSignal(bool)
    progressChanged_hmdb1 = pyqtSignal(int)
    progressChanged_hmdb_vis1 = pyqtSignal(bool)
    progressChanged_hmdb_en = pyqtSignal(bool)
    activatePixel = pyqtSignal(bool)
    
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        
        QMainWindow.__init__(self)
        
        self.ui = mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MSIpixel")
        self.threadpool = QThreadPool()
        
        self.mzml = None
        self.xml = None
        self.library_folder = None
        self.ms2 = None
        self.thr = self.ui.spinBox_2_thr.value()
        self.ui.spinBox_2_thr.valueChanged.connect(self.threshold_update)
        self.perc_pixel = self.ui.spinBox_pixel.value()
        self.ui.spinBox_pixel.valueChanged.connect(self.perc_pixel_update)

        self.update_ms2 = False
        
        
        
        ### INITIAL APPARENCE
        self.initial_app()
        self.ui.spinBox_2_thr.setMaximum(10000000)
        ### END OF INITIAL APPARENCE
        
        ### CLICK AND GO BUTTONS
        self.ui.button_load_mzml.clicked.connect(self.open_mzml)
        self.ui.button_load_xml.clicked.connect(self.open_xml)
        self.ui.button_load_folder.clicked.connect(self.open_folder)
        ### END OF CLICK AND GO BUTTONS
        self.ui.ppm_spinBox.setValue(5)
        self.ppm = self.ui.ppm_spinBox.value()
        self.ui.ppm_spinBox.valueChanged.connect(self.ppm_update)
        
        self.ui.pushButton_inf_process.clicked.connect(self.click_process_infusion)
        self.ui.pushButton_inf_explore.clicked.connect(self.open_explore)
        self.ui.pushButton_spat_process_2.clicked.connect(self.run_spatial)
        self.ui.pushButton_spat_explore_2.clicked.connect(self.open_explore_spatial)
        self.ui.pushButton_rgb.clicked.connect(self.run_rgb)
        self.ui.pushButton_manual.clicked.connect(self.run_manual)
        self.ui.pushButton_hmdb.clicked.connect(self.hmdb_easy_parser)
        self.ui.pushButton_rgb_2.clicked.connect(self.run_pixels)
        self.minimum_score = float(self.ui.spinBox_pixel_2.value())/100.0
        self.ui.spinBox_pixel_2.valueChanged.connect(self.update_minimum_score)
        
        
        
        self.w = None
    
    def update_minimum_score(self):
        self.minimum_score = float(self.ui.spinBox_pixel_2.value())/100.0
    
    def hmdb_easy_parser(self):
        self.ui.checkBox_hmdb.setVisible(True)
        self.ui.checkBox_hmdb1.setVisible(True)
        self.ui.pushButton_hmdb.setEnabled(False)
        self.ui.progressBar_spat_2.setVisible(True)
        self.ui.progressBar_spat_2.setRange(0,100)
        self.ui.progressBar_spat_2.setValue(0)
        self.ui.progressBar_spat_3.setVisible(True)
        self.ui.progressBar_spat_3.setRange(0,100)
        self.ui.progressBar_spat_3.setValue(0)
        self.progressChanged_hmdb.connect(self.ui.progressBar_spat_2.setValue)
        self.progressChanged_hmdb_vis.connect(self.ui.progressBar_spat_2.setVisible)
        self.progressChanged_hmdb1.connect(self.ui.progressBar_spat_3.setValue)
        self.progressChanged_hmdb_vis1.connect(self.ui.progressBar_spat_3.setVisible)
        self.progressChanged_hmdb_en.connect(self.ui.pushButton_hmdb.setEnabled)
        self.db_path = QFileDialog.getOpenFileName(self, "Select All Metabolite zip file", "", ".zip(*.zip)")[0]
        self.msms_path = QFileDialog.getOpenFileName(self, "Select MS-MS Spectra Files (XML) zip file", "", ".zip(*.zip)")[0]
        worker = Worker(self.hmdb) # Any other args, kwargs are passed to the run function
        # Execute
        self.threadpool.start(worker)
        
    
    def hmdb(self):
        self.progressChanged_hmdb_en.emit(False)
        self.hmdb = self.extract_list()
        self.progressChanged_hmdb_vis.emit(False)
        final_lib = self.bind_msms()
        save_path = (str.split(self.msms_path, "/")[-1])
        save_path = str.split(save_path, ".")[0] + ".npy"
        save_path = os.path.join(self.library_folder, save_path)
        np.save(save_path, final_lib)
        self.progressChanged_hmdb_vis1.emit(False)
        self.hmdb = None
        self.progressChanged_hmdb_en.emit(True)
        
    
    def hmdb_parser(self, path):
        root = ET.parse(path).getroot()
        return root
        
        
    def extract_list(self):
        unzip = ZipFile(self.db_path)
        hmdb = []
        root =self.hmdb_parser(unzip.open(unzip.namelist()[0]))
        p = 0
        for elem in root:
            p +=1
            self.progressChanged_hmdb.emit(int(p*100/len(root)))
            if elem.tag.split('}')[1] == "metabolite":
                for subelem in elem:
                    if subelem.tag.split('}')[1] == "accession":
                        acc_number = str(subelem.text)
                    elif subelem.tag.split('}')[1] == "name":
                        name = str(subelem.text)
                    elif subelem.tag.split('}')[1] == "chemical_formula":
                        mf = str(subelem.text)
                    elif subelem.tag.split('}')[1] == "inchikey":
                        inchK = str(subelem.text)
                hmdb.append([name, acc_number, mf, inchK])
        return hmdb
    
    def xml_msms_parser(self, path):
        root = self.hmdb_parser(path)
        for elem in root:
            mz, intensities = [], []
            if elem.tag == "instrument-type":
                instrument = elem.text
            elif elem.tag == "collision-energy-voltage":
                eV = elem.text
            elif elem.tag == "ionization-mode":
                if elem.text is not None:
                    if elem.text.capitalize() == "Positive":
                        polarity = "+"
                    elif elem.text.capitalize() == "Negative":
                        polarity = "-"
                    elif elem.text.capitalize() == "N/a":
                        polarity = "+"
                    else:
                        print(elem.text.capitalize())
                else:
                    polarity = "+"
            elif elem.tag == "database-id":
                hmdbid = elem.text
            if elem.tag == "ms-ms-peaks":
                for subelem in elem:
                    for subsubelem in subelem:
                        if subsubelem.tag == "mass-charge":
                            mz.append(float(subsubelem.text))
                        elif subsubelem.tag == "intensity":
                            intensities.append(float(subsubelem.text))
        return hmdbid, polarity, eV, instrument, mz, intensities
            
        

    def bind_msms(self):
        self.hmdb = np.array(self.hmdb, dtype=object)
        self.ui.progressBar_spat_3.setRange(0,100)
        unzip = ZipFile(self.msms_path)
        ms_files = unzip.namelist()
        final_lib = []
        for i in range(len(ms_files)):
            self.progressChanged_hmdb1.emit(int(i*100/len(ms_files)))
            hmdbid, polarity, eV, instrument, mz, intensities = self.xml_msms_parser(unzip.open(ms_files[i]))
            temp_lib = self.hmdb[self.hmdb[:,1] == hmdbid]
            if len(temp_lib) == 1:
                if len(mz) > 0:
                    final_lib.append([temp_lib[0,0], temp_lib[0,1], temp_lib[0,2], temp_lib[0,3], np.array(mz, dtype=float), np.array(intensities, dtype=float), eV, polarity])
            else:
                pass
        return np.array(final_lib, dtype=object)

    def run_pixels(self):
        self.pixy = QDialog()
        self.pixy_ui = ROI.Ui_Form()
        self.pixy_ui.setupUi(self.pixy, self.all_eim)
        self.pixy.show()
        
    def run_manual(self):
        self.g = QDialog()
        self.g_ui = manual_inspection.Ui_Form()
        self.g_ui.setupUi(self.g, self.mzml)
        self.g.show()
        
    def run_rgb(self):
        self.r = QDialog()
        self.r_ui = rgb.Ui_rgb_plot()
        self.r_ui.setupUi(self.r, self.all_eim)
        self.r.show()
        
    def open_explore_spatial(self):
        #self.df = pd.read_pickle(os.path.join(self.store_folder, "df.pkl"))
        if len(self.df) > 2:
            self.w = QDialog()
            self.w_ui = clustermap.Ui_Form()
            self.w_ui.setupUi(self.w, self.df)
            self.w.show()
        else:
            self.warning_messagge("Not enough elements for clustering analysis")
    
    def open_explore(self):
        self.k = infusion.Explore(self.ms2, self.all_eic, self.all_eim, self.df, self.store_folder)
        self.k.show()
        self.k.b2.clicked.connect(self.update_ms2_state)
        self.k.destroyed.connect(self.close_infusion)
        ### get widget signal and update the ms2
    
    def close_infusion(self):
        if self.update_ms2 == True:
            self.ms2 = np.load(os.path.join(self.store_folder, "ms2.npy"), allow_pickle =True)
            self.all_eic = np.load(os.path.join(self.store_folder, "all_eic.npy"), allow_pickle =True)
            self.df = pd.read_pickle(os.path.join(self.store_folder, "df.pkl"))
            self.all_eim = np.load(os.path.join(self.store_folder, "all_eim.npy"), allow_pickle =True)
        else:
            self.update_ms2 = False
    
    def update_ms2_state(self):
        self.update_ms2 = True
    
    def open_mzml(self):
        self.mzml = QFileDialog.getOpenFileName(self, "Select mzML file", "", ".mzML(*.mzML)")[0]
        self.ui.textEdit_mzml.setText(str.split(self.mzml, "/")[-1])
        if os.path.exists(self.mzml):
            self.ui.pushButton_manual.setEnabled(True)
            folder = os.path.dirname(self.mzml)
            folder_file = str.split(os.path.basename(self.mzml), ".")[0]
            self.store_folder = os.path.join(folder, folder_file)
            try:
                self.ms2 = np.load(os.path.join(self.store_folder, "ms2.npy"), allow_pickle =True)
                self.all_eic = np.load(os.path.join(self.store_folder, "all_eic.npy"), allow_pickle =True)
                self.df = pd.read_pickle(os.path.join(self.store_folder, "df.pkl"))
                self.all_eim = np.load(os.path.join(self.store_folder, "all_eim.npy"), allow_pickle =True)
                self.ui.pushButton_inf_explore.setEnabled(True)
                self.ui.pushButton_spat_explore_2.setEnabled(True)
                self.ui.pushButton_rgb.setEnabled(True)
                self.ui.pushButton_spat_process_2.setEnabled(True)
                self.ui.pushButton_rgb_2.setEnabled(True)
            except:
                self.ui.pushButton_inf_explore.setEnabled(False)
                self.ui.pushButton_spat_explore_2.setEnabled(False)
                self.ui.pushButton_rgb.setEnabled(False)
                self.ui.pushButton_spat_process_2.setEnabled(False)
                self.ui.pushButton_rgb_2.setEnabled(False)
            if self.xml is not None:
                if self.library_folder is not None:
                    self.ui.pushButton_inf_process.setEnabled(True)
        else:
            self.mzml = None
            self.all_eic = None
            self.all_eim = None
            self.df = None
            self.ui.pushButton_inf_process.setEnabled(False)
            self.ui.pushButton_manual.setEnabled(False)
            self.ui.pushButton_inf_explore.setEnabled(False)
            self.ui.pushButton_spat_explore_2.setEnabled(False)
            self.ui.pushButton_rgb.setEnabled(False)
            self.ui.pushButton_spat_process_2.setEnabled(False)
    
    def open_xml(self):
        self.xml = QFileDialog.getOpenFileName(self, "Select XML file", "", ".xml(*.xml)")[0]
        self.ui.textEdit_xml.setText(str.split(self.xml, "/")[-1])
        if os.path.exists(self.xml):
            if self.mzml is not None:
                if self.library_folder is not None:
                    self.ui.pushButton_inf_process.setEnabled(True)
        else:
            self.xml = None
            self.ui.pushButton_inf_process.setEnabled(False)
        
    def open_folder(self):
        self.library_folder = QFileDialog.getExistingDirectory(self, "Select Library Folder", "")
        if os.path.exists(self.library_folder):
            self.ui.textEdit_folder.setText(self.library_folder)
            self.ui.pushButton_hmdb.setEnabled(True)
            if self.xml is not None:
                if self.mzml is not None:
                    self.ui.pushButton_inf_process.setEnabled(True)
        else:
            self.ui.pushButton_inf_process.setEnabled(False)
            self.ui.pushButton_hmdb.setEnabled(False)
    
    
    def ppm_update(self):
        self.ppm = int(self.ui.ppm_spinBox.value())
    
    def threshold_update(self):
        self.thr = int(self.ui.spinBox_2_thr.value())
    
    def perc_pixel_update(self):
        self.perc_pixel = int(self.ui.spinBox_pixel.value())
    
    def click_process_infusion(self):
        self.lib = func.load_library_folder(self.library_folder)
        if len(self.lib) == 0:
            self.warning_messagge("No MS/MS spectra files found in the folder!")
            return
        self.progressChanged.connect(self.ui.progressBar.setValue)
        self.progressChanged2.connect(self.ui.progressBar.setVisible)
        self.progressChanged3.connect(self.ui.checkBox_inf1.setChecked)
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setRange(0,100)
        self.ui.progressBar.setValue(0)
        self.progressChanged_2.connect(self.ui.progressBar_2.setValue)
        self.progressChanged_22.connect(self.ui.progressBar_2.setVisible)
        self.progressChanged_23.connect(self.ui.checkBox_inf2.setChecked)
        self.ui.progressBar_2.setVisible(True)
        self.ui.progressBar_2.setRange(0,100)
        self.ui.progressBar_2.setValue(0)
        self.progressChanged_3.connect(self.ui.progressBar_3.setValue)
        self.progressChanged_32.connect(self.ui.progressBar_3.setVisible)
        self.progressChanged_33.connect(self.ui.checkBox_inf3.setChecked)
        self.ui.progressBar_3.setVisible(True)
        self.ui.progressBar_3.setRange(0,100)
        self.ui.progressBar_3.setValue(0)
        self.buttonRename.connect(self.ui.pushButton_inf_process.setText)
        self.activateProcess_inf.connect(self.ui.pushButton_inf_process.setEnabled)
        self.activateExplore_inf.connect(self.ui.pushButton_inf_explore.setEnabled)
        self.activateProcess_rgb.connect(self.ui.pushButton_rgb.setEnabled)
        self.activateProcess_spat.connect(self.ui.pushButton_spat_explore_2.setEnabled)
        self.activateProcess_spat2.connect(self.ui.pushButton_spat_process_2.setEnabled)
        self.activatePixel.connect(self.ui.pushButton_rgb_2.setEnabled)
        self.parallel = self.ui.checkBox_parallel.checkState()
        self.ppm = self.ui.ppm_spinBox.value()
        # Pass the function to execute
        worker = Worker(self.run_infusion, self.mzml, self.ppm) # Any other args, kwargs are passed to the run function
        # Execute
        self.threadpool.start(worker)
        #self.ui.pushButton_rgb_2.setEnabled(True)
        
    def run_spatial(self):
        self.activateProcess_spat.emit(False)
        self.all_eic, self.all_eim, self.df = func.imz_filters(self.all_eic, self.all_eim, self.df, self.thr, self.perc_pixel, self.minimum_score)
        
    def spatial_distance_eval(self):
        matrix = np.zeros((len(self.all_eic), len(self.all_eic)))
        for i in range(len(self.all_eic)):
            for k in range(len(self.all_eic)):
                a, b = np.nan_to_num(list(self.all_eic[i,2]), nan=0.0), np.nan_to_num(list(self.all_eic[k,2]), nan=0.0)
                a = a/max(a)
                b = b/max(b)
                Y = ks_2samp(a,b)
                matrix[i,k] = 1-Y[0]
        return matrix    

    def indexrange(self, spec, id_spec):
        if self.parallel == True:
            spec = spec[(spec[:,0] >= (id_spec - 1))&(spec[:,0] <= (id_spec +1))]
        else:
            spec = spec[(spec[:,0] >= (id_spec - 1))&(spec[:,0] < (id_spec +1))]
        return spec


    def multiprocess_mf(self, db, ppm, ms1, ms2):
        ncpu = psutil.cpu_count(logical=False) - 1
        args = []
        i_range = list(set(ms2[:,0]))
        results = []
        p = 0
        pool = mp.Pool(ncpu)
        for i in i_range:
            ext2 = ms2[ms2[:,0] == i]
            ext1 = self.indexrange(ms1, i)
            args.append((ext2, ext1, ppm, db, self.parallel))
        for result in pool.imap_unordered(func.splitter, args):
            p += 1
            percentage = int(p*100/len(args))
            self.progressChanged.emit(percentage)
            if len(result) > 0:
                for elem in result:
                    results.append(elem)
        pool.close()
        pool.join()
        self.progressChanged2.emit(False)
        self.progressChanged3.emit(True)
        return np.array(results, dtype=object)


    def multiprocess_annotation(self, mfs, ms2, lib):
        ncpu = psutil.cpu_count(logical=False) - 1
        args = []
        i_range = list(set(mfs[:,0]))
        results = []
        for i in i_range:
            send_lib = np.zeros((0, 8), dtype=object)
            mf = mfs[mfs[:,0] == i]
            for row in mf:
                temp_lib = lib[lib[:,2] == row[6]]
                temp_lib = temp_lib[temp_lib[:,7] == row[5]]
                send_lib = np.concatenate((send_lib, temp_lib))
            if len(send_lib) > 0:
                ext2 = ms2[ms2[:,7] == i]
                args.append((mf, ext2, send_lib))
        pool = mp.Pool(ncpu)
        p = 0
        for result in pool.imap_unordered(func.perform_annotation, args):
            p +=1
            percentage = int(p*100/len(args))
            self.progressChanged_2.emit(percentage)
            if len(result) > 0:
                for elem in result:
                    results.append(elem)
        pool.close()
        pool.join()
        self.progressChanged_22.emit(False)
        self.progressChanged_23.emit(True)
        return np.array(results, dtype=object)
    
    def correct_duplicates(self, best_score, ms2):
        ### add multiprocessing
        index = list(set(best_score[:,8]))
        clean = np.zeros((0,18), dtype=object)
        p = 0
        for i in index:
            one_name = best_score[best_score[:,8] == i]
            if len(set(one_name[:,0])) > 1:
                one_name = func.resolving_duplicates(one_name, ms2)
            else:
                clean = np.concatenate((clean, one_name))
            p += 1
            self.progressChanged_3.emit(int(p/(10*len(index))))
        
        return clean
    
    def eic_all_mp(self, ms1):
        available_ram = psutil.virtual_memory()[1]
        size = sys.getsizeof(ms1) + sys.getsizeof(self.xml) + sys.getsizeof(self.ms2)
        cpu_size = int(available_ram/(size*2000))
        ncpu = psutil.cpu_count(logical=False) - 1
        ncpu = min(ncpu, cpu_size)
        #ncpu = 1
        args = []
        if ncpu < 2:
            args = (self.xml, self.ppm, ms1, self.ms2, self.progressChanged_3, True)
            return func.eic_all2(args)
        else:
            pace = np.arange(0, len(self.ms2), max(2, int(len(self.ms2)/ncpu)))
            pace[-1] = len(self.ms2)
            for i in range(1, len(pace)):
                partial_ms2 = self.ms2[pace[i-1]:pace[i]]
                minmz, maxmz = min(partial_ms2[:,2]) - 1 , max(partial_ms2[:,2]) + 1
                partial_ms1 = func.mzrange(ms1, minmz, maxmz)
                args.append((self.xml, self.ppm, partial_ms1, partial_ms2, None, False))
            results_eic, results_eim = np.zeros((0,5), dtype=object), np.zeros((0,5), dtype=object)
            #results_eic, results_eim = [], []
            p = 0
            pool = mp.Pool(ncpu)
            for result_eic, result_eim in pool.imap_unordered(func.eic_all2, args):
                p +=1
                progress = 10 + int(p*80/ncpu)
                self.progressChanged_3.emit(progress)
                results_eic = np.concatenate((results_eic, result_eic))
                results_eim = np.concatenate((results_eim, result_eim))
            pool.close()
            pool.join()
            all_eic = np.array(results_eic, dtype=object)
            all_eim = np.array(results_eim, dtype=object)
            for i in range(len(all_eic)):
                all_eic[i,0] = i
                all_eim[i,0] = i
            return all_eic, all_eim 

    def run_infusion(self, mzml_path, ppm):
        
        if not os.path.exists(self.store_folder):
            os.makedirs(self.store_folder)
        self.norm_tic = self.ui.checkBox_norm.checkState()
        if self.norm_tic == 0:
            self.norm_tic = False
        else:
            self.norm_tic = True
        self.activateProcess_inf.emit(False)
        self.activateExplore_inf.emit(False)
        
        
        db = func.db_from_lib(self.lib)
        
        ms1, ms2 = func.run_shared(mzml_path, self.norm_tic)
        index = [i for i,k in enumerate(ms2)]
        ms2 = np.c_[ms2, index]
        mfs = self.multiprocess_mf(db, ppm, ms1, ms2)
        ms2 = self.multiprocess_annotation(mfs, ms2, self.lib)
        
        clean = func.dynamic_resolver(ms2, ppm)
        best_s = func.best_score(clean)
        self.ms2 = self.correct_duplicates(best_s, ms2)
        self.ms2 = self.ms2[self.ms2[:,2].argsort()]
        np.save(os.path.join(self.store_folder, "ms2.npy"), self.ms2)
        self.all_eic, self.all_eim = self.eic_all_mp(ms1)
        np.save(os.path.join(self.store_folder, "all_eic.npy"), self.all_eic)
        self.progressChanged_3.emit(92)
        np.save(os.path.join(self.store_folder, "all_eim.npy"), self.all_eim)
        self.progressChanged_3.emit(93)
        self.axis_list = func.num_to_name(self.all_eic)
        self.progressChanged_3.emit(94)
        self.corr_matrix = self.spatial_distance_eval()
        self.progressChanged_3.emit(97)
        self.df = pd.DataFrame(self.corr_matrix, index=self.axis_list, columns=self.axis_list)
        self.progressChanged_3.emit(98)
        self.df.to_pickle(os.path.join(self.store_folder, "df.pkl"))
        self.progressChanged_3.emit(100)
        self.buttonRename.emit("Reprocess")
        self.progressChanged_32.emit(False)
        self.progressChanged_33.emit(True)
        self.activateProcess_inf.emit(True)
        self.activateExplore_inf.emit(True)
        self.activateProcess_rgb.emit(True)
        self.activateProcess_spat.emit(True)
        self.activateProcess_spat2.emit(True)
        self.activatePixel.emit(True)

    
    def warning_messagge(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("")
        msg.exec_()
    
    def initial_app(self):
        self.ui.progressBar.setVisible(False)
        self.ui.progressBar_2.setVisible(False)
        self.ui.progressBar_3.setVisible(False)
        self.ui.progressBar_spat.setVisible(False)
        self.ui.progressBar_spat_2.setVisible(False)
        self.ui.progressBar_spat_3.setVisible(False)
        self.ui.pushButton_inf_explore.setEnabled(False)
        self.ui.pushButton_inf_process.setEnabled(False)
        self.ui.pushButton_manual.setEnabled(False)
        self.ui.pushButton_spat_explore_2.setEnabled(False)
        self.ui.pushButton_rgb.setEnabled(False)
        self.ui.pushButton_spat_process_2.setEnabled(False)
        self.ui.pushButton_hmdb.setEnabled(False)
        self.ui.pushButton_rgb_2.setEnabled(False)
        

if __name__ == "__main__":
    import sys
    mp.freeze_support()
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())