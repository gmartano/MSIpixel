# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 14:59:39 2023

@author: Giuseppe Martano
"""

import pymzml
import numpy as np
import os
from scipy.signal import find_peaks_cwt
from molmass import Formula as mf
from scipy.spatial.distance import cosine
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import pandas as pd


def eic_all2(arguments):
    xml_path, ppm, ms1, ms2, progress, emit = arguments
    all_eic = []
    all_eim = []
    items = list(set(ms2[:,0]))
    p = 0
    for i in items:
        p +=1
        
        prog = 10 + (p/len(items))*80
        if emit == True:
            pass
            #progress.emit(int(prog))
        ms2_i = ms2[ms2[:,0] == i]
        axis_name = str(ms2_i[:,8])
        score = float(ms2_i[0,7])
        if len(ms2_i) > 1:
            ms2_i = ms2_i[0].reshape(1,18)
        args = (get_imz_parameter(xml_path))
        imz = generate_imz(xml_path, ppm, ms1, ms2_i, args)
        all_eic.append([i, imz[:,2], axis_name, score])
        all_eim.append([i, imz, axis_name, score])
    all_eic = np.c_[np.arange(len(all_eic), dtype=object), np.array(all_eic, dtype=object)]
    all_eim = np.c_[np.arange(len(all_eic), dtype=object), np.array(all_eim, dtype=object)]
    return all_eic, all_eim

def ms2_manual_filtering(ms2, eic, eim, df, kill_index):
    df_list = np.array(df.index)
    matrix = np.array(df, dtype=float)
    name_to_kill = ms2[:,8][kill_index]
    ms2 = np.delete(ms2, kill_index, 0)
    x = []
    for i in range(len(eic)):
        for k in name_to_kill:
            if k in eic[i,3]:
                if len(str.split(eic[i,3], "' '")) > 1:
                    name_to_delete = f"'{k}'"
                    new_name = str.replace(eic[i,3], name_to_delete, "")
                    final_name = ""
                    for g in str.split(new_name, " "):
                        if len(g) > 0:
                            final_name = final_name + g + " "
                    if len(final_name) == 0:
                        x.append(i)
                    else:
                        eim[i,3] = final_name
                        df_list[i] = final_name[2:17]
                else:
                    x.append(i)
    eic = np.delete(eic, x, 0)
    eim = np.delete(eim, x, 0)
    matrix = np.delete(matrix, x, 0)
    matrix = np.delete(matrix, x, 1)
    df_list = np.delete(df_list, x, 0)
    df_list = df_list.reshape(len(df_list))
    df = pd.DataFrame(matrix, index= df_list, columns= df_list)
    return ms2, eic, eim, df

def imz_filters(eic, eim, df, thr, perc_pixel, minimum_score):
    df_list = np.array(df.index)
    matrix = np.array(df, dtype=float)
    pixel_len = len(eic[0,2])
    score_list = eic[:,4] >= minimum_score
    eic = eic[score_list]
    eim = eim[score_list]
    df_list = df_list[score_list]
    matrix = matrix[score_list]
    matrix = matrix[:, score_list]
    x = []
    for i in range(len(eic)):
        active_pixels = len(eic[i,2][eic[i,2] > thr])
        if active_pixels == 0:
            x.append(i)
        elif active_pixels*100.0/pixel_len < perc_pixel:
            x.append(i)
    eic = np.delete(eic, x, 0)
    eim = np.delete(eim, x, 0)
    matrix = np.delete(matrix, x, 0)
    matrix = np.delete(matrix, x, 1)
    df_list = np.delete(df_list, x, 0)
    df_list = df_list.reshape(len(df_list))
    df = pd.DataFrame(matrix, index= df_list, columns= df_list)
    return eic, eim, df
    

def get_imz_parameter(xml_path):
    root = ET.parse(xml_path).getroot()
    for elem in root:
        if elem.tag.split('}')[1] == 'rasterConfig':
            for subelem in elem:
                if subelem.tag.split('}')[1] == 'spacing':
                    spacing = float(subelem.text)
                elif subelem.tag.split('}')[1] == "velocity":
                    velocity = float(subelem.text)
                elif subelem.tag.split('}')[1] == "transitionTime":
                    transitionTime = float(subelem.text)      
        else:
            width = int(elem.attrib.get('width'))
            height = int(elem.attrib.get('height'))

    pixel_time = spacing/velocity
    return pixel_time, transitionTime, width, height


def imz_matrix(width, height, pixel_time, transitionTime):
    xyt = []
    t = 0
    for i in range(height):
        for k in range(width):
            t += pixel_time
            xyt.append([k,i,t])
        t += transitionTime
    return xyt

def ms1_into_matrix(ms1, xyt, pixel_time):
    imz = []
    for i in range(len(xyt)):
        time = xyt[i][2]
        start_time = time - pixel_time
        pixel = ms1[(ms1[:,3] > start_time)&(ms1[:,3] < time)]
        if len(pixel) == 0:
            value_i = 0
        elif len(pixel) == 1:
            value_i = sum(pixel[0,5])
        elif len(pixel) > 1 and len(pixel[:,5]) > 0:
            temp = []
            for k in range(len(pixel[:,5])):
                temp.append(sum(pixel[k,5]))
            value_i = np.mean(temp)
        else:
            value_i = 0
        imz.append([xyt[i][0], xyt[i][1], value_i])
    imz = np.array(imz, dtype=object)
    return imz
def plot_data(imz):
    matrix = np.zeros((max(imz[:,1])+1, max(imz[:,0])+1))
    for i in range (len(imz)):
        matrix[imz[i,1], imz[i,0]] = imz[i,2]
    matrix = np.nan_to_num(matrix, nan=0.0)
    return matrix
    plt.imshow(matrix)
    
def generate_imz(xml_path, ppm, ms1, ms2, args):
    if args == None:
        pixel_time, transitionTime, width, height = get_imz_parameter(xml_path)
    else:
        pixel_time, transitionTime, width, height = args
    xyt = imz_matrix(width, height, pixel_time, transitionTime)
    eic = extract_compounds(ms1, ms2[0], ppm)
    imz = ms1_into_matrix(eic, xyt, pixel_time)
    return imz

def generate_imz_from_precursor(xml_path, ppm, ms1, ms2):
    pixel_time, transitionTime, width, height = get_imz_parameter(xml_path)
    xyt = imz_matrix(width, height, pixel_time, transitionTime)
    prec = ms2
    delta = prec*ppm/1000000
    eic = mzrange(ms1, prec-delta, prec+delta)
    imz = ms1_into_matrix(eic, xyt, pixel_time)
    return imz
    
def extract_compounds(ms1, compound, ppm):
    prec = compound[2]
    delta = prec*ppm/1000000
    eic = mzrange(ms1, prec-delta, prec+delta)
    return eic

def check_goodness(imz, threshold, perc_pixel):
    array = np.nan_to_num(list(imz[:,2]), nan=0.0)
    n_pixel = len(array)
    array_thr = len(array[array > 0])
    if array_thr > 0:
        if array_thr*100.0/n_pixel >= perc_pixel:
            return True
        else:
            return False
    else:
        return False


def num_to_name(all_eic):
    x = list(all_eic[:,3])
    for i in range (len(x)):
        text = x[i]
        text = str.replace(text, "[", "")
        text = str.replace(text, "]", "")
        text = str.replace(text, "'", "")
        text = str.replace(text, "\n", ",")
        x[i] = text[:15]
    return x


adducts = np.array([["H", 0, 0, 0, "+"], ["Na", 22.989769282, 0, 0, "+"],
                    ["H", 0, 0, 0, "-"],["Cl", 34.968852682, 0, 0, "-"]], dtype=object)
charge_tab = np.array([[0, 0, 0, 0], [3, 0.3344516116900002, 0, 0], [2, 0.5016774175350003, 0, 0],
                       [1, 1.0033548350700006, 0, 0], [4, 0, 0, 0]], dtype=object)


def update_mf(i, mf, spectra, p, emp_mz, emp_int):
    x = np.zeros((1,18), dtype=object)
    x[0,7] = p
    x[0,16] = emp_mz
    x[0,17] = emp_int
    for k in range(7):
        x[0,k] = mf[i,k]
    for k in range(len(spectra)):
        x[0,k+8] = spectra[k]
    return x

def cluster_mz_values(all_mz):
    start = 1
    stop = 0
    while start != stop:
        start = len(all_mz)
        for i in range(1, len(all_mz)):
            if (all_mz[i,0]-all_mz[i-1,0]) < 0.2:
                all_mz[i,0] = 0
                all_mz[i-1,1] = all_mz[i-1,1] + all_mz[i,1]
                all_mz[i-1,2] = all_mz[i-1,2] + all_mz[i,2]
        all_mz = all_mz[all_mz[:,0] > 0]
        stop = len(all_mz)
    return all_mz

def perform_annotation(args):
    mf, ext2, lib = args
    mf = np.c_[mf, np.zeros((len(mf),11))]
    final = np.zeros((0,18), dtype=object)
    emp_mz = ext2[0,4]
    emp_int = ext2[0,5]/max(ext2[0,5])
    metabolite = np.stack([ext2[0,4], ext2[0,5]/max(ext2[0,5])])
    for i in range(len(mf)):
        sub_lib = lib[lib[:,2] == mf[i,6]]
        for spectra in sub_lib:
            library = np.stack([spectra[4], spectra[5]/max(spectra[5])])
            all_mz = np.concatenate((metabolite[0,:], library[0,:]))
            all_mz = np.array(list(set(all_mz)), dtype=float)
            all_mz.sort()
            all_mz = np.stack([all_mz, np.zeros(len(all_mz)), np.zeros(len(all_mz))])
            all_mz = all_mz.transpose()
            for j in range(len(all_mz)):
                for k in range(len(metabolite[0,:])):
                    if all_mz[j,0] == metabolite[0,k]:
                        all_mz[j,1] = metabolite[1,k]
                for k in range(len(library[0,:])):
                    if all_mz[j,0] == library[0,k]:
                        all_mz[j,2] = library[1,k]                 
            all_mz = cluster_mz_values(all_mz)
            p = 1 - cosine(all_mz[:,1], all_mz[:,2])
            found = update_mf(i, mf, spectra, p, emp_mz, emp_int)
            final = np.concatenate((final, found))
    return final


def best_score(ms2):
    clean = np.zeros((0,18))
    index = list(set(ms2[:,0]))
    for i in index:
        one_id = ms2[ms2[:,0] == i]
        if len(one_id) > 0:
            one_id = one_id[one_id[:,7] == max(one_id[:,7])]
        clean = np.concatenate((clean, one_id))
    return clean


def reassign_ms2(one_name, ms2, esclusion):
    new_list = np.zeros((0,18))
    for i in esclusion:
        esc_ms2 = ms2[ms2[:,8] != i]
    for index in one_name[:,0]:
        one_id = esc_ms2[esc_ms2[:,0] == index]
        if len(one_id) > 0:
            one_id = one_id[one_id[:,7] == max(one_id[:,7])]
            new_list = np.concatenate((new_list, one_id))
    return new_list


def resolving_duplicates(one_name, ms2):
    final = np.zeros((0,18), dtype=object)
    while len(one_name) > 0:
        best = one_name[one_name[:,7] == max(one_name[:,7])]
        one_name = one_name[one_name[:,7] != max(one_name[:,7])]
        final = np.concatenate((final, best))
        one_name = reassign_ms2(one_name, ms2, final[:,8])
    return final


def dynamic_resolver(ms2, ppm):
    index = list(set(ms2[:,0]))
    index.sort()
    clean = np.zeros((0,18), dtype=object)
    skip = []
    for i in index:
        if i in skip:
            pass
        else:
            start = ms2[ms2[:,0] == i]
            precursor = start[0,2]
            replicates = ms2[(ms2[:,2] > (precursor - precursor*ppm/1000000))&(ms2[:,2] < (precursor + precursor*ppm/1000000))]
            for k in list(set(replicates[:,0])):
                if k in skip:
                    replicates = replicates[replicates[:,0] != k]
                else:
                    skip.append(k)
            replicates[:,0] = min(replicates[:,0])
            clean = np.concatenate((clean, replicates))
    return clean

def findPeaks(spectra):
    spec = []
    for i in range(len(spectra)):
        if len(spectra[i][5]) > 0:
            peaks = find_peaks_cwt(spectra[i][5], widths=1.5, min_snr=1.5)
            if len(peaks) > 0:
                spec.append([spectra[i][0], spectra[i][1], spectra[i][2], spectra[i][3], spectra[i][4][peaks], spectra[i][5][peaks], spectra[i][6]])
            else:
                spec.append([spectra[i][0], spectra[i][1], spectra[i][2], spectra[i][3], np.array([0.0]), np.array([0.0]), spectra[i][6]])
        else:
            spec.append([spectra[i][0], spectra[i][1], spectra[i][2], spectra[i][3], np.array([0.0]), np.array([0.0]), spectra[i][6]])
    return np.array(spec, dtype=object)

def mzrange(spectra, minmz, maxmz):
    spec = []
    for i in range(len(spectra)):
        intensities = spectra[i,5][(spectra[i,4]> minmz)&(spectra[i,4]<maxmz)]
        masslist = spectra[i,4][(spectra[i,4]> minmz)&(spectra[i,4]<maxmz)]
        spec.append([spectra[i,0], spectra[i,1], spectra[i,2], spectra[i,3], masslist, intensities, spectra[i,6]])
    return np.array(spec, dtype=object)


def ms2eic(spec2, eic, massrange):
    minmz, maxmz = spec2[2] - massrange, spec2[2] + massrange
    eic = mzrange(eic, minmz, maxmz)
    return eic

def adduct_table(ms2, ppm):
    if ms2[6] == "+":
        polarity = adducts[adducts[:,4] == "+"]
    else:
        polarity = adducts[adducts[:,4] == "-"]
    polarity[:,1] = ms2[2] - polarity[:,1]
    polarity[:,2] = polarity[:,1] - ppm*polarity[:,1]/1000000
    polarity[:,3] = polarity[:,1] + ppm*polarity[:,1]/1000000
    return polarity

def consistency(adduct_item, eic, parallel):
    cons = mzrange(eic, adduct_item[2], adduct_item[3])
    n = 0
    for i in range(len(cons)):
        if len(cons[i][4]) > 0:
            n +=1
    if parallel == True:
        equal_to = 3
    else:
        equal_to = 2
    if n == equal_to:
        return True
    else:
        return False

def check_existence(addlist, spec, parallel):
    for i in range(1, len(addlist)):
        if consistency(addlist[i], spec, parallel) == True:
            return addlist[i][0]
    else:
        return addlist[0][0]

def assign_adduct(ms2, ms1, ppm, parallel):
    eic = ms2eic(ms2, ms1, 2)
    spec = findPeaks(eic)
    addlist = adduct_table(ms2, ppm)
    if consistency(addlist[0], spec, parallel) == True:
        final_adduct = check_existence(addlist, spec)
        return final_adduct
    else:
        return False


def charge_table(ms2, ppm):
    charge = charge_tab[charge_tab[:,0] < 4]
    charge[:,1] = ms2[2] + charge[:,1]
    charge[:,2] = charge[:,1] - ppm*charge[:,1]/1000000
    charge[:,3] = charge[:,1] + ppm*charge[:,1]/1000000
    return charge

def assign_charge(ms2, ms1, ppm, parallel):
    eic = ms2eic(ms2, ms1, 6)
    spec = findPeaks(eic)
    addlist = charge_table(ms2, ppm)
    if consistency(addlist[0], spec, parallel) == True:
        final_adduct = check_existence(addlist, spec, parallel)
        return final_adduct
    else:
        return False


def assign_mw(precursor, adduct, charge, polarity):
    if polarity == "+" and charge < 2:
        mw = precursor - mf(adduct).monoisotopic_mass + 0.0005485799090649834
    else:
        if adduct == "H":
            mw = precursor + mf(adduct).monoisotopic_mass - 0.0005485799090649834
        else:
            mw = precursor - mf(adduct).monoisotopic_mass - 0.0005485799090649834
    return mw

def match_formula(mw, ppm, db):
    minmz, maxmz = mw - ppm*mw/1000000, mw + ppm*mw/1000000
    match = db[(db[:,1] > minmz)&(db[:,1] < maxmz)]
    return match

def precursor_to_mf(ms2, ms1, ppm, db, parallel):
    compound_list = []
    final_charge = assign_charge(ms2, ms1, ppm, parallel)
    if ms2[6] == "+":
        polarity = adducts[adducts[:,4] == "+"]
    else:
        polarity = adducts[adducts[:,4] == "-"]
    if final_charge != False:
        for i in polarity[:,0]:
            mw = assign_mw(ms2[2], i, final_charge, ms2[6])
            match = match_formula(mw, ppm, db)
            if len(match) > 0:
                for k in range (len(match)):
                    compound_list.append([ms2[7], mw, ms2[2], i, final_charge, ms2[6], match[k,0]])
    return compound_list

def splitter(args):
    ms2, ms1, ppm, db, parallel = args
    compounds = []
    for i in range(len(ms2)):
        ms2_i = ms2[i] ### QUI SI PIANTA
        comp_per_id = precursor_to_mf(ms2_i, ms1, ppm, db, parallel)
        if len(comp_per_id) > 0:
            for q in range(len(comp_per_id)):
                compounds.append(comp_per_id[q])
    return compounds

def db_from_lib(lib):
    db = np.zeros((0,2))
    y = list(set(lib[:,2]))
    for i in y:
        try:
            new = np.array([i, float(mf(i).monoisotopic_mass)]).reshape(1,2)
            db = np.concatenate((db, new))
        except:
            pass
    db = np.array(db, dtype=object)
    for i in range(len(db[:,1])):
        db[i,1] = float(db[i,1])
    return db
        
def transform_data(mzml_file, norm_tic):
    print("Extracting ms and ms2 values")
    run = pymzml.run.Reader(mzml_file)
    #msi datastructure = [index, mslevel, precursor, time, mz, intensities, polarity]
    index = 0
    ms = []
    for n, spec in enumerate(run):
        if spec["negative scan"] is not None:
            polarity = "-"
        elif spec["positive scan"] is not None:
            polarity = "+"
        if spec.ms_level == 1:
            if norm_tic == True:
                ms.append([index, spec.ms_level, None, spec.scan_time_in_minutes()*60, spec.mz, spec.i/spec.TIC, polarity])
            else:
                ms.append([index, spec.ms_level, None, spec.scan_time_in_minutes()*60, spec.mz, spec.i, polarity])
            index += 1
        elif spec.ms_level == 2:
            if len(spec.i) > 0:
                ms.append([index-1, spec.ms_level, spec.selected_precursors[0]['mz'], spec.scan_time_in_minutes(), spec.mz, spec.i, polarity])
    return np.array(ms, dtype=object)

def transform_data_manual(mzml_file):
    print("Extracting ms and ms2 values")
    run = pymzml.run.Reader(mzml_file)
    #msi datastructure = [index, mslevel, precursor, time, mz, intensities, polarity]
    index = 0
    ms = []
    for n, spec in enumerate(run):
        if spec["negative scan"] is not None:
            polarity = "-"
        elif spec["positive scan"] is not None:
            polarity = "+"
        if spec.ms_level == 1:
            ms.append([index, spec.ms_level, None, spec.scan_time_in_minutes()*60, spec.mz, spec.i, polarity])
            index += 1
        elif spec.ms_level == 2:
            if len(spec.i) > 0:
                ms.append([spec.index, spec.ms_level, spec.selected_precursors[0]['mz'], spec.scan_time_in_minutes(), spec.mz, spec.i, polarity])
    return np.array(ms, dtype=object)
    
def msn_split(ms):
    mslevel1 = ms[ms[:,1] == 1]
    mslevel2 = ms[ms[:,1] == 2]
    return mslevel1, mslevel2
    
    
def load_library_folder(lib_folder):
    print("Loading the MS/MS library")
    try:
        file_list = [s for s in os.listdir(lib_folder) if str.split(s, ".")[1] == "npy"]
    except:
        return []
    lib = np.zeros((0,8))
    for file in file_list:
        if str.split(file, ".")[-1] == "npy":
            lib_temp = np.load(os.path.join(lib_folder, file), allow_pickle=True)
            lib = np.concatenate((lib, lib_temp))
    return lib
    
def run_shared(mzml_path, norm_tic):
    ms2 = transform_data(mzml_path, norm_tic)
    ms1, ms2 = msn_split(ms2)
    return ms1, ms2