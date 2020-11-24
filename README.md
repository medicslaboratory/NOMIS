# NOMIS
NOrmative Morphometry Image Statistics (NOMIS) for FreeSurfer 6.0
#################################### INSTRUCTIONS #####################################

@2020 MEDICS LABORATORY - CERVO BRAIN RESEARCH CENTER - UNIVERSITE LAVAL

MEDICS Normative morphometric data calculator for FreeSurfer 6.0 - Version 1.0

>>> Disclaimer
NOMIS.py is a free tool to compute normative morphometric values for FreeSurfer 6 developed by the MEDICS laboratory at the CERVO Brain Research Center / Universite Laval, Quebec, Canada. The normative values are computed and adjusted according to age, sex, estimated intracranial volume (eTIV), scanner manufacturer, scanner magnetic field strength, voxel size, surface holes and contrast-to-noise ratio.

 If you use the normative values, please cite and refer to the following publication:
 Potvin O., Dieumegarde L., and Duchesne S. (submitted). Quantifying morphometry deviation from the normality over the lifetime of the adult human brain.

 Please note that this calculator is NOT approved for any form of clinical use.
 These normative values are aimed to be applied on FreeSurfer 6.0 output already processed with fully-automated directive parameters: “recon-all -all” command without any manual or expert flag option (https://surfer.nmr.mgh.harvard.edu/fswiki/recon-all).
 All processed images should have finished without error and the user should verify the the segmentation quality.

 Normative values are Z scores with a mean of 0 and a standard deviation of 1.

 This tool was built on MacOS using Python 3.7.4 with the following modules: 
 argparse version 1.1
 nibabel version 2.5.1
 numpy version 1.17.2
 pandas version 0.25.1
 pickle version 4.0
 

 For questions, email the author at: olivier.potvin at cervo.ulaval.ca


>>> Script
 Extract the Calculator.zip file 
 Run the python script (NOMIS.py) from a terminal

 usage: python NOMIS.py [-h] -csv <csvpath> -s <subject_dir> [-o <outputpath>] [-a <atlas>] [-v <verbose>] [-w <warnings>]

 required arguments:
   -csv             csv file containing "id" as in FreeSurfer’s subject directory, "sex" categorized as M/F, "age", 
                    "manufacturer" categorized as GE/Philips/Siemens, "mfs" (magnetic field strength) categorized as 1.5/3, 
                    and "voxel" (voxel acquisition size in mm3, for example: 1)
                    For a csv file example, see "Calculator/Example/csv_example.csv"

   -s               The path to the directory containing the FreeSurfer subjects folders that you want to analyze.
   
 optional arguments:
   -h, --help       Show this help message
   -o               Output directory where the normative z scores will be saved. Default is Calculator/Example/out/
   -a               Atlas name. Choices are DK, DKT, Destrieux, Default is DK. By default, norms for other atlases (aseg, ex vivo, brainstem subfields, hippocampal subfields) are computed.
   -v {on/off}      Verbose. Default is on
   -w {on/off}      Print code warnings. Default is off
 
 
>>> Example
 A working example is supply with this tool and should produce normative data in the “./Calculator/Example/out” folder. In a Terminal window, change your working directory where the NOMIS.py tool is (the folder "Calculator/") and try:
 python NOMIS.py -csv Example/csv_example.csv -s Example/FreeSurfer_dir -a -DK


>>> Ouput
 Three folders are created. The "normative_z_scores" folder contains the nomative z scores files. The "raw_scores" folder contains the collected FreeSurfer 6 stats. The CNR folder contains the computed CNR values used to compute the norms. 

 File and region names are identical to those within the stats files, except:
 	cc = sum of the corpus callosum divisions: cc_posterior + cc_mid_posterior + cc_central + cc_mid_anterior + 'cc_anterior
 	ventricles = sum of all ventricles: 3rd-ventricle + 4th-ventricle + left-inf-lat-vent + left-lateral-ventricle' + right-inf-lat-vent + right-lateral-ventricle


>>> Other
 Although it is not required, if you want to compute pial surfaces stats for DKT and a2009s atlases, please see parcstats step in https://surfer.nmr.mgh.harvard.edu/fswiki/ReconAllTableStableV6.0. For the calculator we called them aparc.pial.DKT and aparc.pial.a2009s, but these names are arbitrary and can be changed easily within the NOMIS.py file (see atlaslist).


##########################################################################################
