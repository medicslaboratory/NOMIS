#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 08:55:36 2020

@author: olivierp
"""
import sys
import argparse
parser=argparse.ArgumentParser()
#required
parser.add_argument("-csv", dest='csv', help='csv file containing subjects id (as in FreeSurfer’s subject directory), sex (categorized as M/F), age, manufacturer (categorized as GE/Philips/Siemens), magnetic field strength (1.5/3), and voxel acquisition size in mm3 (e.g. 1). For an example, see /Calculator/csv_example.csv', required=True)
parser.add_argument("-s", dest='subject_dir', help='The path to the directory containing all the FreeSurfer subjects folders.', required=True)
#optional
parser.add_argument("-o", dest='out', help='Folder where the normative z scores csv files will be saved. Default is /Calculator/out', required=False)
parser.add_argument("-a", dest='atlas', help='Atlas name. Choices are DK, DKT, Destrieux, Default is DK. By default, norms for other atlases (aseg, ex vivo, brainstem subfields, hippocampal subfields) are computed if they are in the FreeSurfer stats folder.', required=False)
parser.add_argument("-v", dest='verbose', help='on/off, Print executed steps. Default is on', required=False)
parser.add_argument("-w", dest='warnings', help='on/off, Print warnings. Default is off', required=False)
args=parser.parse_args()

if args.atlas is None: atlas='DK'
else: atlas=args.atlas
if str(args.verbose) == 'off': verbose='off'
if args.verbose is None or str(args.verbose) == 'on': verbose='on'
import warnings as wn
if args.warnings is None or str(args.warnings) == 'off': warnings='off'
if args.warnings is not None and str(args.warnings) == 'on': warnings='on'
if warnings == 'off': wn.filterwarnings("ignore")

import pandas as pd
import os
from bin import NOMIS_func
if verbose == 'on': 
    import platform
    print('python version ', platform.python_version())
    if int(platform.python_version()[0]) == 2: 
        print('python 3 is required')
        print('quit')
        quit()
    print('argparse version ', argparse.__version__)
    import numpy as np
    print('numpy version ', np.__version__)
    import pickle
    print('pickle version ', pickle.format_version)
    import nibabel as nib
    print('nibabel version ', nib.__version__)
    print('pandas version ', pd.__version__)
    import sklearn
    print('sklearn version ', sklearn.__version__)

current_path = os.path.dirname(os.path.realpath(__file__))
path_csv = args.csv
csv1 = pd.read_csv(path_csv)
csv = csv1.dropna()
missing = [x for x in csv1['id'].tolist() if x not in csv['id'].tolist()]
print(len(missing), 'participants had missing values in the csv file:', missing)

# variables list
version = 'hi' 
if 'sex' in csv.columns: version = 's' + version
if 'age' in csv.columns: version = 'a' + version

path_FS = args.subject_dir
path_FS = path_FS + '/'

if args.out is not None: 
    outputpath = args.out
    outputpath = outputpath + '/'
    
if args.out is None: outputpath = current_path + '/Example/out/'     

if not os.path.exists(outputpath + "CNR/"): os.makedirs(outputpath + "CNR/")
if not os.path.exists(outputpath + "raw_scores/"): os.makedirs(outputpath + "raw_scores/")
if not os.path.exists(outputpath + "normative_z_scores/"): os.makedirs(outputpath + "normative_z_scores/")

# the cortical atlaslist is for bilateral atlases and list and names for pial can be modified here as required
mainatlas = atlas
if mainatlas == 'DK': 
    mainname = 'aparc'
    mainpial = 'aparc.pial'
if mainatlas == 'DKT': 
    mainname = 'aparc.DKTatlas'
    mainpial = 'aparc.pialDKT'
if mainatlas == 'Destrieux': 
    mainname = 'aparc.a2009s'
    mainpial = 'aparc.pial.a2009s'
    
for atlas, name in [('aseg', 'aseg'), (mainatlas, mainname)]:
    CNRdata = pd.DataFrame()
    for i in csv['id']:
        CNRdata1 = NOMIS_func.FS6_CNR_peratlas(i, atlas=atlas, path_FS=path_FS)
        CNRdata = pd.concat([CNRdata, CNRdata1], axis=0)
    
    if atlas !='aseg':
        if atlas == 'Destrieux':
            CNRdata.columns = [x.replace('ctx_', '') for x in CNRdata.columns]
            left = [x for x in CNRdata.columns if x.startswith('lh_')]
            left = [x for x in left if x.endswith('_cnr')]
            right = [x for x in CNRdata.columns if x.startswith('rh_')]
            right = [x for x in right if x.endswith('_cnr')]
            CNRdataL = CNRdata[left]        
            CNRdataL.columns = [x.replace('lh_', '') for x in CNRdataL.columns]
            CNRdataR = CNRdata[right]
            CNRdataR.columns = [x.replace('rh_', '') for x in CNRdataR.columns]

        else:
            CNRdata.columns = [x.replace('ctx-', '') for x in CNRdata.columns]
            left = [x for x in CNRdata.columns if x.endswith('_l_cnr')]
            right = [x for x in CNRdata.columns if x.endswith('_r_cnr')]
            CNRdataL = CNRdata[left]        
            CNRdataL.columns = [x.replace('_l', '') for x in CNRdataL.columns]
            CNRdataR = CNRdata[right]
            CNRdataR.columns = [x.replace('_r', '') for x in CNRdataR.columns]
        CNRdataL.to_csv(outputpath + 'CNR/lh.' + name + '.csv', index=True)
        CNRdataR.to_csv(outputpath + 'CNR/rh.' + name + '.csv', index=True)
    else: 
        CNRdata.to_csv(outputpath + "CNR/" + name + '.csv')

if verbose == 'on': print('Contrast-to-noise ratio computed')

atlaslist=[mainname, mainpial, 'BA_exvivo',]
fsfilelist=['aseg_bigregions.csv', 'aseg.csv', 'brainstem.csv', 'lhpcsub.csv', 'rhpcsub.csv', 'lh.' + mainname + '.csv', 'rh.' + mainname + '.csv', 'lh.BA_exvivo.csv', 'rh.BA_exvivo.csv', 'wmparc.csv', 'lh.' + mainpial + '.csv', 'rh.' + mainpial + '.csv',]
NOMIS_func.get_FS_stats(csv, path_FS, outputpath, current_path, version, atlaslist, fsfilelist, verbose=verbose, warn=warnings)





























