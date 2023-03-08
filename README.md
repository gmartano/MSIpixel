# MSIpixel

# Installation
MSIpixel is provided as windows exe format. Download the MSIpixel_win.zip file, unzip and run locally on your machine by dobble cliccking on MSIpixel.exe. (Optional) You can download a test_file.zip file for testing MSIpixel funcionalities.

![image](https://user-images.githubusercontent.com/91892227/223106091-f837b511-7d86-42a4-9846-7c92b3f8983b.png)

# Building library
The library can be created by adding MS/MS spectra into a single folder. MS/MS spectra can be exported from raw data with manual inspection (see below) or an initial spectral library can be generated by clicking on HMDB easy parser button. This button will ask for All Metabolites XML file that can be found at https://hmdb.ca/downloads and an XML file with MS/MS spectra e.g. "MS-MS Spectra Files (XML) - Predicted".

# Process data
There are two initial option for data processing: manual inspection and process.
  - Manual inspection
  
    Input: mzML file
    It will open a new screen. By adding m/z value or type a chemical formula, the software will search and display the TIC and the MS/MS list available for the given       value. MS/MS can be exported by clicking on the "Create library file"
    ![image](https://user-images.githubusercontent.com/91892227/223106951-a10fd652-8011-4e7e-9a9e-31f1cef6fb03.png)

  - Progress
  
    Input: mzML file, xml file, library Folder
    This process perform automated identification and quantitaion of the data. Users can define the ppm range for compound identification and isolation, and (optional)       to correct the intensity against the TIC by clicking of the checkbox.
    Note: The quantity and quality of matched compounds depend on the presence of their MS/MS     spectra in the library folder.
 
# Filter results
 
 Apply the filters on the datset.
 
# Explore results
 
 Return a list of annotate componds with the given MS/MS score aganst the library. Note: deleting a compound in this part, it will delete in the entire analysis.
 
# Spatial correlation
 
 Return a spatial correlation of each annotated compoung within the image of interest
 ![image](https://user-images.githubusercontent.com/91892227/223116192-4fae41b7-7977-439c-a39f-4f758a91c38a.png)

 
# RGB Plot
 
 It gives the possibility to plot 3 different compounds and generate a merge figure
 ![image](https://user-images.githubusercontent.com/91892227/223116432-5b5d9a18-ac8b-4fa6-882f-1e1c1caca620.png)

 
# Pixel analysis
 
 It gives the possibility to select ROIs and export the data of the given ROIs.
 ![image](https://user-images.githubusercontent.com/91892227/223116680-7236fe23-115f-4af1-bf57-80539a232572.png)
