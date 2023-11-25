# Cite as:
Morosi, et al., "MSIpixel: A Fully Automated Pipeline for Compound Annotation and Quantitation in Mass Spectrometry Imaging Experiments", Briefings in Bioinformatics, (2023)

DOI: https://doi.org/10.1093/bib/bbad463

# MSIpixel
To run MSIpixel, there are 2 options:
1)	On Windows machine, you can download the compile version of MSIpixel at https://github.com/gmartano/MSIpixel_utils/raw/main/MSIpixel_win.exe 
Unzip the folder and execute the MSIpixel.exe file.
2)	clone this repository or download all the .py files and place them in the same folder. Install python and dependencies as decribed below and then execute the main.py file. 
With both method, the following GUI should appear on your screen.

![mainGui](https://github.com/gmartano/MSIpixel/assets/91892227/82faa789-b530-4e7a-99a2-898c0f6743a5)

## Python version and Dependencies
MSIpixel was developed and tested with python 3.11.0. Library requirments: PyQt5, Numpy, psutil, scipy, pandas, seaborn, matplotlib, molmass,pymzml. To look at specific library versions, look at requirments.txt

## Test files
In order to test MSIpixel functionalities, we recommend you to download the test file (https://github.com/gmartano/MSIpixel_utils/raw/main/test_files.zip) and test_library (https://github.com/gmartano/MSIpixel_utils/raw/main/test_library.zip).
Unzip all the files and select the mzML, XML and the library folder to test the functionalities described below.

## Raw Data
MALDI acquisition should be set by using "Horizontal" and "Flyback" mode.

## Building library
The library can be created by adding MS/MS spectra into a single folder. MS/MS spectra can be exported from raw data with manual inspection(see below).
For export MS/MS spectra from raw files, load the mzML file that contain the spectra of interest on the main GUI.
Click on Manual Inspection, which is active only if an mzML file is selected.

## Manual inspection
A new screen it will appear. 

![f1](https://github.com/gmartano/MSIpixel/assets/91892227/c410c762-4c73-4231-9109-f69512a79e63)

It is possible to fill in the m/z values to search or insert a chemical formula. In the second case, the m/z value will be automatically calculated based on the give selected adduct. If MS/MS scan are present for the given m/z value within ppm tolerance, a list of clickable items will appear and can be visualized by selecting the values. To export the selected MS/MS, click on Create Library file. A popup will open and ask for Save.
Note 1: Depending on the size of the file, the new screen may appear after few seconds for small files (less than 1 gb) or several minutes for bigger files.
Note 2: Manual inspection do not reconstruct the spatial distribution and don’t need XML file.

## Process data
This process perform automated compound identification and quantification of the data, using custom libraries. Here the steps to follow:
1. Load mzML and xml files of the sample by clicking the relative buttons on top of main page of the app
2. Select the library folder. The app will load all the libraries stored in it and use them as reference to perform compounds identification
3. Choose the parameters in the Analysis block: ppm range for compound identification and isolation, and (optional) to correct the intensity against the TIC by clicking of the checkbox, and for parallel or sequential DDA acquisition method (based on the instrument and method configuration used).
4. Click Process button and wait for the analysis to end Once finished, a folder with results of the analysis is created in the same folder where the input mzML file is stored.
Note 1: Progress button will activate only if all the mzML, XML, and library folder are specified. 
Note 2: The analysis may required from few minutes to several hours to complete depending on the size and complexity of the acquired sample. Typical mzML file may spawn between few Gb to more than 100 Gb. We recommend to use a machine with at least the double size of RAM compared with the size of the files to analyse (e.g. for 30 Gb mzML use a system with 64 Gb RAM or more).

![f2](https://github.com/gmartano/MSIpixel/assets/91892227/27d749ee-03bd-46cc-b8b3-bbb59dceb798)

## Secondary analysis
Once the files are processed, several secondary analyses can be performed (Stats section).


## Load analyzed files
If you have already processed the data, you can load them just by loading the corresponding mzML file. The app will search for metafiles in a folder with the same name as mzML file and load the results.
Note: If you move that folder without moving the mzML file, the will not be able to load the results. 

## Explore results
Return a list of annotate compounds with the given MS/MS score against the library.
In this page, by right click, you can delete found annotation, but dataset will not change until Overwrite annotation list is clicked.
Annotation results can be exported by clicking on Export Results button.
Note: After Overwrite by deleting a compound here, it will remove it in the entire analysis.

![f3](https://github.com/gmartano/MSIpixel/assets/91892227/9a291052-1073-470f-a1ad-462e9f9f396a)

## Filter results
You can filter the identified features by applying:
Threshold: Define a minimum intensity to account for each signal.
Perc. of pixel: percentage of pixels with that feature
MS2 score (%): Filter out all the compound with MS2 score lower than the used define limit

## Spatial correlation
Return a spatial correlation plot of each annotated compound within the image of interest.

![f4](https://github.com/gmartano/MSIpixel/assets/91892227/605fe859-6460-4ef8-b43e-9df06530a7fd)

## RGB Plot
It gives the possibility to plot 3 different compounds and generate a merged figure.

![f5](https://github.com/gmartano/MSIpixel/assets/91892227/3f3097a7-c01b-4755-b640-573afe960c2f)

## Pixel analysis
It gives the possibility to draw different ROIs and export the data of them in Excel format (xlsx).
For drawing a ROI type the ROI name on the space next to Add Group button, select color and line thickness and then Click Add Group.
Click Draw for start drawing the ROI. The ROI will close by re-clicking on the first point of the ROI. For each ROI a boxplot relative to the selected compound will appear. Changing the compound will update the boxplot accordingly.

![f6](https://github.com/gmartano/MSIpixel/assets/91892227/6e4bf734-ca8b-4bfb-85db-2999a14c5c27)

## HMDB easy parser
Initial spectral library can be generated by clicking on HMDB easy parser button. This button will ask for All Metabolites XML file that can be found at https://hmdb.ca/downloads and an XML file with MS/MS spectra e.g. “MS-MS Spectra Files (XML) - Predicted”. The library is saved as npy file.
In order to activate this function, the Library Folder must have been selected. If not, create an empty folder and select it by clicking on Load Library Folder.

## Minimum and recommended system requirements
Minimum and recommended number of core = 4; > 16

Minimum and recommended RAM (GB) > 16; > 64
