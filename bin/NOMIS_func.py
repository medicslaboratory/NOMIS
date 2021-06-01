#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:05:27 2019

@author: olivierp
"""
import pandas as pd
import numpy as np
import pickle
import warnings as wn
import nibabel as nib
import numpy.ma as ma
pd.options.display.precision = 10

def regionf(data, value):
    string = ""
    andstring = " & "
    for i in range(len(value)):
        val = value[i]
        if i != np.max(range(len(value))):
            out = "(np.logical_or(data < " + str(val) + ", data >" + str(val) + "))" + str(andstring)
        else:
            out = "(np.logical_or(data < " + str(val) + ", data >" + str(val) + "))"
        string += out 
    return eval(string)

def FS6_CNR_peratlas(pt, atlas, path_FS, regions_numbers="default", image='brain', bigregions=True, regions_names="default", FS=6):
    data = []
    i = pt 
    #print('CNR', i)
    cerebralwhitemattervol = ("cerebralwhitemattervol", [2,41])
    try:
        if atlas == 'aseg':
            parcfile = "aparc.DKTatlas+aseg.mgz"
            regions_numbers = [2, 4,	5,	7,	8,	10,	11,	12,	13,	14,	15,	16,	17,	18,	24,	26,	28,	41,	43,	44,	46,	47,	49,	50,	51,	52,	53,	54,	58,	60]
            regions_names = [x.lower() for x in ["Left-Cerebral-White-Matter",	"Left-Lateral-Ventricle",	"Left-Inf-Lat-Vent",	"Left-Cerebellum-White-Matter",	"Left-Cerebellum-Cortex",	"Left-Thalamus-Proper",	"Left-Caudate",	"Left-Putamen",	"Left-Pallidum",	"3rd-Ventricle",	"4th-Ventricle",	"Brain-Stem",	"Left-Hippocampus",	"Left-Amygdala",	"CSF",	"Left-Accumbens-area",	"Left-VentralDC",	"Right-Cerebral-White-Matter",	"Right-Lateral-Ventricle",	"Right-Inf-Lat-Vent",	"Right-Cerebellum-White-Matter",	"Right-Cerebellum-Cortex",	"Right-Thalamus-Proper",	"Right-Caudate",	"Right-Putamen",	"Right-Pallidum",	"Right-Hippocampus",	"Right-Amygdala",	"Right-Accumbens-area",	"Right-VentralDC",	"CC_Posterior",	"CC_Mid_Posterior",	"CC_Central",	"CC_Mid_Anterior",	"CC_Anterior"]]
            totalgrayvol = ("totalgrayvol", [8,10,11,12,13,17,18,26,	28,	47,	49,	50,	51,	52,	53,	54,	58,	60, 1000,1002,	1003,	1005,	1006,	1007,	1008,	1009,	1010,	1011,	1012,	1013,	1014,	1015,	1016,	1017,	1018,	1019,	1020,	1021,	1022,	1023,	1024,	1025,	1026,	1027,	1028,	1029,	1030,	1031,	1034,	1035,	2000,	2002,	2003,	2005,	2006,	2007,	2008,	2009,	2010,	2011,	2012,	2013,	2014,	2015,	2016,	2017,	2018,	2019,	2020,	2021,	2022,	2023,	2024,	2025,	2026,	2027,	2028,	2029,	2030,	2031,	2034,	2035])
            cortexvol = ("cortexvol", [1000,	1002,	1003,	1005,	1006,	1007,	1008,	1009,	1010,	1011,	1012,	1013,	1014,	1015,	1016,	1017,	1018,	1019,	1020,	1021,	1022,	1023,	1024,	1025,	1026,	1027,	1028,	1029,	1030,	1031,	1034,	1035,	2000,	2002,	2003,	2005,	2006,	2007,	2008,	2009,	2010,	2011,	2012,	2013,	2014,	2015,	2016,	2017,	2018,	2019,	2020,	2021,	2022,	2023,	2024,	2025,	2026,	2027,	2028,	2029,	2030,	2031,	2034,	2035])
            lhcortexvol = ("lhcortexvol", [1000,	1002,	1003,	1005,	1006,	1007,	1008,	1009,	1010,	1011,	1012,	1013,	1014,	1015,	1016,	1017,	1018,	1019,	1020,	1021,	1022,	1023,	1024,	1025,	1026,	1027,	1028,	1029,	1030,	1031,	1034,	1035])
            rhcortexvol = ("rhcortexvol", [2000,	2002,	2003,	2005,	2006,	2007,	2008,	2009,	2010,	2011,	2012,	2013,	2014,	2015,	2016,	2017,	2018,	2019,	2020,	2021,	2022,	2023,	2024,	2025,	2026,	2027,	2028,	2029,	2030,	2031,	2034,	2035])
            subcortgrayvol = ('subcortgrayvol', [10,11,12,13,17,18,26,28,49,	50,	51,	52,	53,	54,	58,	60])
            ventricles = ("ventricles",[4,5,14,15,24,43,44])
            bigcnr = [totalgrayvol, cortexvol, lhcortexvol, rhcortexvol, subcortgrayvol, cerebralwhitemattervol, ventricles]
            bigcnrnames = ['totalgrayvol', 'cortexvol', 'lhcortexvol', 'rhcortexvol', 'subcortgrayvol', 'cerebralwhitemattervol', 'ventricles']
            cnr_regions_names = [x.lower() for x in ["Left-Cerebellum-Cortex",	"Left-Thalamus-Proper",	"Left-Caudate",	"Left-Putamen",	"Left-Pallidum", "Brain-Stem",	"Left-Hippocampus",	"Left-Amygdala",	 "Left-Accumbens-area",	"Left-VentralDC", "Right-Cerebellum-Cortex",	"Right-Thalamus-Proper",	"Right-Caudate",	"Right-Putamen",	"Right-Pallidum", "Right-Hippocampus",	"Right-Amygdala",	"Right-Accumbens-area",	"Right-VentralDC"]]
            cnr_regions_names = bigcnrnames + cnr_regions_names
        if atlas != 'aseg': bigcnr=[cerebralwhitemattervol]
        if atlas == 'DKT':
            parcfile = "aparc.DKTatlas+aseg.mgz"
            regions_numbers = [1000,	1002,	1003,	1005,	1006,	1007,	1008,	1009,	1010,	1011,	1012,	1013,	1014,	1015,	1016,	1017,	1018,	1019,	1020,	1021,	1022,	1023,	1024,	1025,	1026,	1027,	1028,	1029,	1030,	1031,	1034,	1035,	2000,	2002,	2003,	2005,	2006,	2007,	2008,	2009,	2010,	2011,	2012,	2013,	2014,	2015,	2016,	2017,	2018,	2019,	2020,	2021,	2022,	2023,	2024,	2025,	2026,	2027,	2028,	2029,	2030,	2031,	2034,	2035]
            regions_names = [x.lower() for x in ["ctx-unknown_L",	"ctx-caudalanteriorcingulate_L",	"ctx-caudalmiddlefrontal_L",	"ctx-cuneus_L",	"ctx-entorhinal_L",	"ctx-fusiform_L",	"ctx-inferiorparietal_L",	"ctx-inferiortemporal_L",	"ctx-isthmuscingulate_L",	"ctx-lateraloccipital_L",	"ctx-lateralorbitofrontal_L",	"ctx-lingual_L",	"ctx-medialorbitofrontal_L",	"ctx-middletemporal_L",	"ctx-parahippocampal_L",	"ctx-paracentral_L",	"ctx-parsopercularis_L",	"ctx-parsorbitalis_L",	"ctx-parstriangularis_L",	"ctx-pericalcarine_L",	"ctx-postcentral_L",	"ctx-posteriorcingulate_L",	"ctx-precentral_L",	"ctx-precuneus_L",	"ctx-rostralanteriorcingulate_L",	"ctx-rostralmiddlefrontal_L",	"ctx-superiorfrontal_L",	"ctx-superiorparietal_L",	"ctx-superiortemporal_L",	"ctx-supramarginal_L",	"ctx-transversetemporal_L",	"ctx-insula_L",	"ctx-unknown_R",	"ctx-caudalanteriorcingulate_R",	"ctx-caudalmiddlefrontal_R",	"ctx-cuneus_R",	"ctx-entorhinal_R",	"ctx-fusiform_R",	"ctx-inferiorparietal_R",	"ctx-inferiortemporal_R",	"ctx-isthmuscingulate_R",	"ctx-lateraloccipital_R",	"ctx-lateralorbitofrontal_R",	"ctx-lingual_R",	"ctx-medialorbitofrontal_R",	"ctx-middletemporal_R",	"ctx-parahippocampal_R",	"ctx-paracentral_R",	"ctx-parsopercularis_R",	"ctx-parsorbitalis_R",	"ctx-parstriangularis_R",	"ctx-pericalcarine_R",	"ctx-postcentral_R",	"ctx-posteriorcingulate_R",	"ctx-precentral_R",	"ctx-precuneus_R",	"ctx-rostralanteriorcingulate_R",	"ctx-rostralmiddlefrontal_R",	"ctx-superiorfrontal_R",	"ctx-superiorparietal_R",	"ctx-superiortemporal_R",	"ctx-supramarginal_R",	"ctx-transversetemporal_R",	"ctx-insula_R"]]
            cnr_regions_names = regions_names
        if atlas == 'DK':
            parcfile = "aparc+aseg.mgz"
            regions_numbers = [1000,	1001,	1002,	1003,	1005,	1006,	1007,	1008,	1009,	1010,	1011,	1012,	1013,	1014,	1015,	1016,	1017,	1018,	1019,	1020,	1021,	1022,	1023,	1024,	1025,	1026,	1027,	1028,	1029,	1030,	1031,	1032,	1033,	1034,	1035,	2000,	2001,	2002,	2003,	2005,	2006,	2007,	2008,	2009,	2010,	2011,	2012,	2013,	2014,	2015,	2016,	2017,	2018,	2019,	2020,	2021,	2022,	2023,	2024,	2025,	2026,	2027,	2028,	2029,	2030,	2031,	2032,	2033,	2034,	2035]
            regions_names = [x.lower() for x in ["ctx-unknown_L",	"ctx-bankssts_L",	"ctx-caudalanteriorcingulate_L",	"ctx-caudalmiddlefrontal_L",	"ctx-cuneus_L",	"ctx-entorhinal_L",	"ctx-fusiform_L",	"ctx-inferiorparietal_L",	"ctx-inferiortemporal_L",	"ctx-isthmuscingulate_L",	"ctx-lateraloccipital_L",	"ctx-lateralorbitofrontal_L",	"ctx-lingual_L",	"ctx-medialorbitofrontal_L",	"ctx-middletemporal_L",	"ctx-parahippocampal_L",	"ctx-paracentral_L",	"ctx-parsopercularis_L",	"ctx-parsorbitalis_L",	"ctx-parstriangularis_L",	"ctx-pericalcarine_L",	"ctx-postcentral_L",	"ctx-posteriorcingulate_L",	"ctx-precentral_L",	"ctx-precuneus_L",	"ctx-rostralanteriorcingulate_L",	"ctx-rostralmiddlefrontal_L",	"ctx-superiorfrontal_L",	"ctx-superiorparietal_L",	"ctx-superiortemporal_L",	"ctx-supramarginal_L",	"ctx-frontalpole_L",	"ctx-temporalpole_L",	"ctx-transversetemporal_L",	"ctx-insula_L",	"ctx-unknown_R",	"ctx-bankssts_R",	"ctx-caudalanteriorcingulate_R",	"ctx-caudalmiddlefrontal_R",	"ctx-cuneus_R",	"ctx-entorhinal_R",	"ctx-fusiform_R",	"ctx-inferiorparietal_R",	"ctx-inferiortemporal_R",	"ctx-isthmuscingulate_R",	"ctx-lateraloccipital_R",	"ctx-lateralorbitofrontal_R",	"ctx-lingual_R",	"ctx-medialorbitofrontal_R",	"ctx-middletemporal_R",	"ctx-parahippocampal_R",	"ctx-paracentral_R",	"ctx-parsopercularis_R",	"ctx-parsorbitalis_R",	"ctx-parstriangularis_R",	"ctx-pericalcarine_R",	"ctx-postcentral_R",	"ctx-posteriorcingulate_R",	"ctx-precentral_R",	"ctx-precuneus_R",	"ctx-rostralanteriorcingulate_R",	"ctx-rostralmiddlefrontal_R",	"ctx-superiorfrontal_R",	"ctx-superiorparietal_R",	"ctx-superiortemporal_R",	"ctx-supramarginal_R",	"ctx-frontalpole_R",	"ctx-temporalpole_R",	"ctx-transversetemporal_R",	"ctx-insula_R"]]
            cnr_regions_names = regions_names
        if atlas == 'Destrieux':
            parcfile = "aparc.a2009s+aseg.mgz"
            regions_numbers = list(map(int, '11101	11102	11103	11104	11105	11106	11107	11108	11109	11110	11111	11112	11113	11114	11115	11116	11117	11118	11119	11120	11121	11122	11123	11124	11125	11126	11127	11128	11129	11130	11131	11132	11133	11134	11135	11136	11137	11138	11139	11140	11141	11143	11144	11145	11146	11147	11148	11149	11150	11151	11152	11153	11154	11155	11156	11157	11158	11159	11160	11161	11162	11163	11164	11165	11166	11167	11168	11169	11170	11171	11172	11173	11174	11175	12101	12102	12103	12104	12105	12106	12107	12108	12109	12110	12111	12112	12113	12114	12115	12116	12117	12118	12119	12120	12121	12122	12123	12124	12125	12126	12127	12128	12129	12130	12131	12132	12133	12134	12135	12136	12137	12138	12139	12140	12141	12143	12144	12145	12146	12147	12148	12149	12150	12151	12152	12153	12154	12155	12156	12157	12158	12159	12160	12161	12162	12163	12164	12165	12166	12167	12168	12169	12170	12171	12172	12173	12174	12175'.split()))
            regions_names = [x.lower() for x in 'ctx_lh_G&S_frontomargin	ctx_lh_G&S_occipital_inf	ctx_lh_G&S_paracentral	ctx_lh_G&S_subcentral	ctx_lh_G&S_transv_frontopol	ctx_lh_G&S_cingul-Ant	ctx_lh_G&S_cingul-Mid-Ant	ctx_lh_G&S_cingul-Mid-Post	ctx_lh_G_cingul-Post-dorsal	ctx_lh_G_cingul-Post-ventral	ctx_lh_G_cuneus	ctx_lh_G_front_inf-Opercular	ctx_lh_G_front_inf-Orbital	ctx_lh_G_front_inf-Triangul	ctx_lh_G_front_middle	ctx_lh_G_front_sup	ctx_lh_G_Ins_lg&S_cent_ins	ctx_lh_G_insular_short	ctx_lh_G_occipital_middle	ctx_lh_G_occipital_sup	ctx_lh_G_oc-temp_lat-fusifor	ctx_lh_G_oc-temp_med-Lingual	ctx_lh_G_oc-temp_med-Parahip	ctx_lh_G_orbital	ctx_lh_G_pariet_inf-Angular	ctx_lh_G_pariet_inf-Supramar	ctx_lh_G_parietal_sup	ctx_lh_G_postcentral	ctx_lh_G_precentral	ctx_lh_G_precuneus	ctx_lh_G_rectus	ctx_lh_G_subcallosal	ctx_lh_G_temp_sup-G_T_transv	ctx_lh_G_temp_sup-Lateral	ctx_lh_G_temp_sup-Plan_polar	ctx_lh_G_temp_sup-Plan_tempo	ctx_lh_G_temporal_inf	ctx_lh_G_temporal_middle	ctx_lh_Lat_Fis-ant-Horizont	ctx_lh_Lat_Fis-ant-Vertical	ctx_lh_Lat_Fis-post	ctx_lh_Pole_occipital	ctx_lh_Pole_temporal	ctx_lh_S_calcarine	ctx_lh_S_central	ctx_lh_S_cingul-Marginalis	ctx_lh_S_circular_insula_ant	ctx_lh_S_circular_insula_inf	ctx_lh_S_circular_insula_sup	ctx_lh_S_collat_transv_ant	ctx_lh_S_collat_transv_post	ctx_lh_S_front_inf	ctx_lh_S_front_middle	ctx_lh_S_front_sup	ctx_lh_S_interm_prim-Jensen	ctx_lh_S_intrapariet&P_trans	ctx_lh_S_oc_middle&Lunatus	ctx_lh_S_oc_sup&transversal	ctx_lh_S_occipital_ant	ctx_lh_S_oc-temp_lat	ctx_lh_S_oc-temp_med&Lingual	ctx_lh_S_orbital_lateral	ctx_lh_S_orbital_med-olfact	ctx_lh_S_orbital-H_Shaped	ctx_lh_S_parieto_occipital	ctx_lh_S_pericallosal	ctx_lh_S_postcentral	ctx_lh_S_precentral-inf-part	ctx_lh_S_precentral-sup-part	ctx_lh_S_suborbital	ctx_lh_S_subparietal	ctx_lh_S_temporal_inf	ctx_lh_S_temporal_sup	ctx_lh_S_temporal_transverse	ctx_rh_G&S_frontomargin	ctx_rh_G&S_occipital_inf	ctx_rh_G&S_paracentral	ctx_rh_G&S_subcentral	ctx_rh_G&S_transv_frontopol	ctx_rh_G&S_cingul-Ant	ctx_rh_G&S_cingul-Mid-Ant	ctx_rh_G&S_cingul-Mid-Post	ctx_rh_G_cingul-Post-dorsal	ctx_rh_G_cingul-Post-ventral	ctx_rh_G_cuneus	ctx_rh_G_front_inf-Opercular	ctx_rh_G_front_inf-Orbital	ctx_rh_G_front_inf-Triangul	ctx_rh_G_front_middle	ctx_rh_G_front_sup	ctx_rh_G_Ins_lg&S_cent_ins	ctx_rh_G_insular_short	ctx_rh_G_occipital_middle	ctx_rh_G_occipital_sup	ctx_rh_G_oc-temp_lat-fusifor	ctx_rh_G_oc-temp_med-Lingual	ctx_rh_G_oc-temp_med-Parahip	ctx_rh_G_orbital	ctx_rh_G_pariet_inf-Angular	ctx_rh_G_pariet_inf-Supramar	ctx_rh_G_parietal_sup	ctx_rh_G_postcentral	ctx_rh_G_precentral	ctx_rh_G_precuneus	ctx_rh_G_rectus	ctx_rh_G_subcallosal	ctx_rh_G_temp_sup-G_T_transv	ctx_rh_G_temp_sup-Lateral	ctx_rh_G_temp_sup-Plan_polar	ctx_rh_G_temp_sup-Plan_tempo	ctx_rh_G_temporal_inf	ctx_rh_G_temporal_middle	ctx_rh_Lat_Fis-ant-Horizont	ctx_rh_Lat_Fis-ant-Vertical	ctx_rh_Lat_Fis-post	ctx_rh_Pole_occipital	ctx_rh_Pole_temporal	ctx_rh_S_calcarine	ctx_rh_S_central	ctx_rh_S_cingul-Marginalis	ctx_rh_S_circular_insula_ant	ctx_rh_S_circular_insula_inf	ctx_rh_S_circular_insula_sup	ctx_rh_S_collat_transv_ant	ctx_rh_S_collat_transv_post	ctx_rh_S_front_inf	ctx_rh_S_front_middle	ctx_rh_S_front_sup	ctx_rh_S_interm_prim-Jensen	ctx_rh_S_intrapariet&P_trans	ctx_rh_S_oc_middle&Lunatus	ctx_rh_S_oc_sup&transversal	ctx_rh_S_occipital_ant	ctx_rh_S_oc-temp_lat	ctx_rh_S_oc-temp_med&Lingual	ctx_rh_S_orbital_lateral	ctx_rh_S_orbital_med-olfact	ctx_rh_S_orbital-H_Shaped	ctx_rh_S_parieto_occipital	ctx_rh_S_pericallosal	ctx_rh_S_postcentral	ctx_rh_S_precentral-inf-part	ctx_rh_S_precentral-sup-part	ctx_rh_S_suborbital	ctx_rh_S_subparietal	ctx_rh_S_temporal_inf	ctx_rh_S_temporal_sup	ctx_rh_S_temporal_transverse'.lower().split()]
            cnr_regions_names = regions_names

        print(i, 'Extracting CNR', atlas, 'with', parcfile)
        labels = nib.load(path_FS + i + "/mri/" + parcfile)
        labels_data = labels.get_data()
        t1 = nib.load(path_FS + i + "/mri/" + image + ".mgz")
        t1_data = t1.get_data()
        columnsnames = ['id']
        data2 = []
        data2.extend([i])
        for name, num in bigcnr:
            try:
                r = regionf(labels_data, num)
                t1_data_masked = ma.array(t1_data, mask=r)
                data2.extend([np.mean(t1_data_masked), np.std(t1_data_masked, ddof=1)])    
                columnsnames.extend([name, name + "_sd"])
            except: pass
        for j in range(len(regions_numbers)):
            try:
                #print(regions_names[j])
                r = labels_data != regions_numbers[j]
                t1_data_masked = ma.array(t1_data, mask=r)
                data2.extend([np.mean(t1_data_masked), np.std(t1_data_masked, ddof=1)])    
                columnsnames.extend([regions_names[j], regions_names[j]+ "_sd"])
            except: pass
        data.append(data2)
        bigoutput = pd.DataFrame(data)
        bigoutput.columns = columnsnames
        bigoutput.set_index('id', inplace=True)
        bigoutput2 = CNR(bigoutput, region=cnr_regions_names, mean='', sd='_sd')
        #print(1,bigoutput2)
        bigoutput2 = bigoutput2[bigoutput2.applymap(isnumber)]
        #print(2,bigoutput2)
        return bigoutput2        

    except: 
        print(i, ' did not work')
        pass
        

def isnumber(x):
    try:
        float(x)
        return True
    except:
        return False

    
def CNR(data, region=["cortex", "subcortical"], mean='', sd='_sd'):
    data.columns = data.columns.str.lower()
    for gm in region:
        data[gm + '_cnr'] = np.square(data[gm + mean] - data['cerebralwhitemattervol']) / (np.square(data[gm + sd]) + np.square(data['cerebralwhitemattervol_sd']))
    return data


def get_FS_stats(csv, path_FS, outputpath, current_path, version, atlaslist, fsfilelist, verbose='on', warn='off', names=['StructName', 'NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv', 'GausCurv', 'FoldInd', 'CurvInd'], colnames=(['NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv', 'GausCurv', 'FoldInd', 'CurvInd'], ['NumVert', 'SurfArea', 'GrayVol', 'ThickAvg', 'ThickStd', 'MeanCurv', 'GausCurv', 'FoldInd', 'CurvInd'])):
    if warn == 'off': wn.filterwarnings("ignore")
    if verbose == 'on': print('Collecting FreeSurfer 6 stats')
    for atlas in atlaslist:
        lbigoutput = pd.DataFrame()
        rbigoutput = pd.DataFrame()
        for subject in csv['id']:
            #if verbose == 'on': print(atlas, subject)
            try:
                left = pd.read_csv(path_FS + subject + "/stats/lh." + atlas + ".stats", comment='#', delim_whitespace=True, header=None, index_col=0, names=names)
                loutput = pd.Series()
                for n in range(len(colnames[0])):
                    m = left[colnames[0][n]]
                    m.index = [str(x) + '_' + colnames[1][n] for x in m.index]
                    m.name = subject
                    loutput = pd.Series(loutput.append(m), name=subject)
                loutput = pd.DataFrame(loutput).T
                lbigoutput = lbigoutput.append(loutput)
            except:
                if verbose == 'on': print('The file ' +  path_FS + subject + "/stats/lh." + atlas + ".stats" + ' does not exist')
                pass
            
            try:
                right = pd.read_csv(path_FS + subject + "/stats/rh." + atlas + ".stats", comment='#', delim_whitespace=True, header=None, index_col=0, names=names)
                routput = pd.Series()
                for n in range(len(colnames[0])):
                    m = right[colnames[0][n]]
                    m.index = [str(x) + '_' + colnames[1][n] for x in m.index]
                    m.name = subject
                    routput = pd.Series(routput.append(m), name=subject)
                routput = pd.DataFrame(routput).T
                rbigoutput = rbigoutput.append(routput)
            except:
                if verbose == 'on': print('The file ' +  path_FS + subject + "/stats/rh." + atlas + ".stats" + ' does not exist')
                pass

        if not lbigoutput.empty:
            lbigoutput.columns = lbigoutput.columns.str.lower()
            if 'pial' in atlas: lbigoutput = lbigoutput.filter(regex='surfarea')
            lbigoutput.to_csv(outputpath + "raw_scores/" + 'lh.' + atlas + '.csv', index_label='id')
        if not rbigoutput.empty:
            rbigoutput.columns = rbigoutput.columns.str.lower()
            if 'pial' in atlas: rbigoutput = rbigoutput.filter(regex='surfarea')
            rbigoutput.to_csv(outputpath + "raw_scores/" + 'rh.' + atlas + '.csv', index_label='id')

    # aseg and wmparc
    voxelsize = pd.DataFrame()
    bigaseg = pd.DataFrame()
    bigaseg2 = pd.DataFrame()
    bigwmparc = pd.DataFrame()
    bigwmparc = pd.DataFrame()
    bigbrainstem = pd.DataFrame()
    bigrhpcsub = pd.DataFrame()
    biglhpcsub = pd.DataFrame()
    nameaseg = ['Index', 'SegId', 'NVoxels', 'Volume_mm3', 'StructName', 'normMean', 'normStdDev', 'normMin', 'normMax', 'normRange']
    for subject in csv['id']:
        try:
            # get voxel size 
            if '.long.' in subject: 
                print('Longitudinal pipeline detected. Looking for original image in', subject.split('.long.')[0])
                t1o = nib.load(path_FS + subject.split('.long.')[0]  + '/mri/orig/001.mgz')
            else: t1o = nib.load(path_FS + subject + '/mri/orig/001.mgz')
            voxel = [t1o.header.get_zooms()[0]*t1o.header.get_zooms()[1]*t1o.header.get_zooms()[2]]
            voxelsize = voxelsize.append(pd.Series(voxel, name=subject, index=['voxel']))
        except: pass
        # aseg file
        asegoutput = pd.Series()
        try:
            aseg = pd.read_csv(path_FS + subject + "/stats/aseg.stats", comment='#', delim_whitespace=True, header=None, index_col=0, names=nameaseg)
            aseg.index = aseg['StructName']
            aseg = aseg[['Volume_mm3']]
            aseg = pd.Series(aseg['Volume_mm3'])
            aseg = pd.Series(asegoutput.append(aseg), name=subject)
            aseg = pd.DataFrame(aseg).T
            bigaseg = bigaseg.append(aseg)
        except: pass
        # big regions top of test aseg file
        asegoutput2 = pd.Series()
        try:
            aseg2 = pd.read_csv(path_FS + subject + "/stats/aseg.stats", delimiter=',', header=None, names=names)
            aseg2 = aseg2.loc[aseg2['NumVert'].notnull()]
            aseg2 = aseg2.loc[aseg2['StructName'].str.contains('Measure')]
            aseg2['NumVert'] = aseg2['NumVert'].str.replace(' ', '')
            aseg2 = aseg2[['NumVert','GrayVol']]
            aseg2.columns = ['region','measure']
            aseg2.set_index(['region'], inplace=True)
            aseg2 = pd.Series(aseg2['measure'])
            aseg2 = pd.Series(asegoutput2.append(aseg2), name=subject)
            aseg2 = pd.DataFrame(aseg2).T
            if 'SurfaceHoles' not in aseg2.columns and '.long.' in subject: 
                print('Longitudinal pipeline detected. Looking for surface holes in', subject.split('.long.')[0])
                aseg22 = pd.read_csv(path_FS + subject.split('.long.')[0] + "/stats/aseg.stats", delimiter=',', header=None, names=names)
                aseg22 = aseg22.loc[aseg22['NumVert'].notnull()]
                aseg22 = aseg22.loc[aseg22['StructName'].str.contains('Measure')]
                aseg22['NumVert'] = aseg22['NumVert'].str.replace(' ', '')
                aseg22 = aseg22[['NumVert','GrayVol']]
                aseg22.columns = ['region','measure']
                aseg22.set_index(['region'], inplace=True)
                aseg22 = pd.Series(aseg22['measure'])
                aseg22 = pd.Series(asegoutput2.append(aseg22), name=subject)
                aseg22 = pd.DataFrame(aseg22).T
                aseg22 = aseg22[['SurfaceHoles']]
                aseg2 = pd.concat([aseg2, aseg22], axis=1)
        except: pass
        
        #left
        side='left_'
        asegoutput3 = pd.Series()
        try:
            aseg3 = pd.read_csv(path_FS + subject + "/stats/lh.aparc.DKTatlas.stats", delimiter=',', header=None, names=names)
            aseg3['NumVert'] = aseg3['NumVert'].str.replace(' ', '')
            aseg3 = aseg3.loc[aseg3['NumVert'].isin(['WhiteSurfArea', 'MeanThickness'])]
            aseg3 = aseg3[['NumVert','GrayVol']]
            aseg3.columns = ['region', 'measure']
            aseg3.set_index(['region'], inplace=True)
            aseg3 = pd.Series(aseg3['measure'])
            aseg3 = pd.Series(asegoutput3.append(aseg3), name=subject)
            aseg3 = pd.DataFrame(aseg3).T
            aseg3.columns = [side + 'WhiteSurfArea', side + 'MeanThickness']
        except: pass
        asegoutput5 = pd.Series()
        try:
            aseg5 = pd.read_csv(path_FS + subject + "/stats/lh.aparc.pial.stats", delimiter=',', header=None, names=names)
            aseg5['NumVert'] = aseg5['NumVert'].str.replace(' ', '')
            aseg5 = aseg5.loc[aseg5['NumVert'].isin(['PialSurfArea'])]
            aseg5 = aseg5[['NumVert','GrayVol']]
            aseg5.columns = ['region', 'measure']
            aseg5.set_index(['region'], inplace=True)
            aseg5 = pd.Series(aseg5['measure'])
            aseg5 = pd.Series(asegoutput5.append(aseg5), name=subject)
            aseg5 = pd.DataFrame(aseg5).T
            aseg5.columns = [side + 'PialSurfArea']
        except: pass
        #right
        side='right_'
        asegoutput4 = pd.Series()
        try:
            aseg4 = pd.read_csv(path_FS + subject + "/stats/rh.aparc.DKTatlas.stats", delimiter=',', header=None, names=names)
            aseg4['NumVert'] = aseg4['NumVert'].str.replace(' ', '')
            aseg4 = aseg4.loc[aseg4['NumVert'].isin(['WhiteSurfArea', 'MeanThickness'])]
            aseg4 = aseg4[['NumVert','GrayVol']]
            aseg4.columns = ['region', 'measure']
            aseg4.set_index(['region'], inplace=True)
            aseg4 = pd.Series(aseg4['measure'])
            aseg4 = pd.Series(asegoutput4.append(aseg4), name=subject)
            aseg4 = pd.DataFrame(aseg4).T
            aseg4.columns = [side + 'WhiteSurfArea', side + 'MeanThickness']
        except: pass    
        asegoutput6 = pd.Series()
        try:
            aseg6 = pd.read_csv(path_FS + subject + "/stats/rh.aparc.pial.stats", delimiter=',', header=None, names=names)
            aseg6['NumVert'] = aseg6['NumVert'].str.replace(' ', '')
            aseg6 = aseg6.loc[aseg6['NumVert'].isin(['PialSurfArea'])]
            aseg6 = aseg6[['NumVert','GrayVol']]
            aseg6.columns = ['region', 'measure']
            aseg6.set_index(['region'], inplace=True)
            aseg6 = pd.Series(aseg6['measure'])
            aseg6 = pd.Series(asegoutput6.append(aseg6), name=subject)
            aseg6 = pd.DataFrame(aseg6).T
            aseg6.columns = [side + 'PialSurfArea']
            big26 = pd.concat([aseg2, aseg3, aseg4, aseg5, aseg6], axis=1)
            bigaseg2 = bigaseg2.append(big26)
        except: pass
        wmparcoutput = pd.Series()
        try:
            wmparc = pd.read_csv(path_FS + subject + "/stats/wmparc.stats", comment='#', delim_whitespace=True, header=None, index_col=0, names=nameaseg)
            wmparc = wmparc.loc[wmparc['StructName'].str.contains('wm')]
            wmparc.index = wmparc['StructName']
            wmparc = wmparc[['Volume_mm3']]
            wmparc = pd.Series(wmparc['Volume_mm3'])
            wmparc = pd.Series(wmparcoutput.append(wmparc), name=subject)
            wmparc = pd.DataFrame(wmparc).T
            bigwmparc = bigwmparc.append(wmparc)
        except: pass    
        # HPC subfields and brainstem
        try:
            rhpcsub = pd.read_csv(path_FS + subject + "/mri/rh.hippoSfVolumes-T1.v10.txt", delimiter=' ', header=None, index_col=0, names=['regions', subject])
            rhpcsub = rhpcsub.T
            bigrhpcsub = bigrhpcsub.append(rhpcsub)
        except: pass    
        try:
            lhpcsub = pd.read_csv(path_FS + subject + "/mri/lh.hippoSfVolumes-T1.v10.txt", delimiter=' ', header=None, index_col=0, names=['regions', subject])
            lhpcsub = lhpcsub.T
            biglhpcsub = biglhpcsub.append(lhpcsub)
        except: pass    
        try:
            brainstem = pd.read_csv(path_FS + subject + "/mri/brainstemSsVolumes.v10.txt", delimiter=' ', header=None, index_col=0, names=['regions', subject])
            brainstem = brainstem.T
            bigbrainstem = bigbrainstem.append(brainstem)
        except: pass
               
    if not bigrhpcsub.empty:
        bigrhpcsub.columns = bigrhpcsub.columns.str.lower()
        bigrhpcsub.to_csv(outputpath + 'raw_scores/rhpcsub.csv', index_label='id')
    
    if not biglhpcsub.empty:
        biglhpcsub.columns = biglhpcsub.columns.str.lower()
        biglhpcsub.to_csv(outputpath + 'raw_scores/lhpcsub.csv', index_label='id')
        
    if not bigbrainstem.empty:
        bigbrainstem.columns = bigbrainstem.columns.str.lower()
        bigbrainstem.to_csv(outputpath + 'raw_scores/brainstem.csv', index_label='id')
        
    if not bigaseg.empty:
        bigaseg.columns = bigaseg.columns.str.lower()
        # compute sum of corpus callosum and log10 for ventricles
        bigaseg['cc'] = bigaseg['cc_posterior'] + bigaseg['cc_mid_posterior'] + bigaseg['cc_central'] + bigaseg['cc_mid_anterior'] + bigaseg['cc_anterior'] 
        bigaseg['ventricles'] = bigaseg['3rd-ventricle'] + bigaseg['4th-ventricle'] + bigaseg['left-inf-lat-vent'] + bigaseg['left-lateral-ventricle'] + bigaseg['right-inf-lat-vent'] + bigaseg['right-lateral-ventricle'] 
        bigaseg.to_csv(outputpath + 'raw_scores/aseg.csv', index_label='id')
    
    if not bigaseg2.empty:
        bigaseg2.columns = bigaseg2.columns.str.lower()
        # add etiv, surfaceholes and voxel size to csv 
        etiv = bigaseg2[['etiv', 'surfaceholes']]
        # log surface holes
        etiv['surfaceholes'] = np.log(etiv['surfaceholes'])
        csv = pd.merge(etiv, csv, how='right', left_index=True, right_on=['id'])
        csv = pd.merge(voxelsize, csv, how='right', left_index=True, right_on=['id'])
        csv.set_index(['id'], inplace=True)
        csv.to_csv(outputpath + 'raw_scores/csv.csv')
        bigaseg2.to_csv(outputpath + 'raw_scores/aseg_bigregions.csv', index_label='id')
        
    if not bigwmparc.empty:
        bigwmparc.columns = bigwmparc.columns.str.lower()
        bigwmparc.to_csv(outputpath + 'raw_scores/wmparc.csv', index_label='id')  
    
    #if verbose == 'on': print('FreeSurfer 6 data collected')
    if verbose == 'on': print('Coding variables')

    # center age and etiv and select Z score version
    meanage = pd.read_csv(current_path + '/bin/meanage.csv', index_col=None, header=None)
    meanetiv = pd.read_csv(current_path + '/bin/meanetiv.csv', index_col=None, header=None)
    meansurfaceholes = pd.read_csv(current_path + '/bin/meansurfaceholes.csv', index_col=None, header=None)

    adjlist = 'intra-cranial volume, scanner characteristics and image quality'
    if 'sex' in csv.columns: adjlist = 'sex, ' + adjlist
    if 'age' in csv.columns: adjlist = 'age, ' + adjlist

    if 'sex' not in csv.columns: csv['sex'] = 'F'
    if 'age' not in csv.columns: csv['age'] = meanage.loc[0,0]


    print('Normative Z scores are adjusted for ' + adjlist)

    # calculate power IVs
    listenumvar = [('age', meanage), ('etiv', meanetiv), ('surfaceholes', meansurfaceholes)]
    for c, m in listenumvar:
        try:
            csv[c] = csv[c] - m.loc[0,0]
            c3 = c + "3"
            c2 = c + "2"
            #print(c, c2, c3)
            csv[c3] = csv[c] * csv[c] * csv[c]
            csv[c2] = csv[c] * csv[c]
        except: pass
        
    # categorical variables
    try:
        csv.loc[(csv['sex'].str.lower() == 'f'), 'sex_m'] = 0    
        csv.loc[(csv['sex'].str.lower() == 'm'), 'sex_m'] = 1    
        csv = csv.drop(['sex'], axis=1)
    except: pass
    csv.loc[(csv['mfs'] == 1.5), 'mfs_15'] = 1    
    csv.loc[(csv['mfs'] == 3), 'mfs_15'] = 0    
    csv.loc[(csv['manufacturer'].str.lower() != 'philips'), 'manufacturer_philips'] = 0    
    csv.loc[(csv['manufacturer'].str.lower() == 'philips'), 'manufacturer_philips'] = 1    
    csv.loc[(csv['manufacturer'].str.lower() != 'ge'), 'manufacturer_ge'] = 0    
    csv.loc[(csv['manufacturer'].str.lower() == 'ge'), 'manufacturer_ge'] = 1    
    csv = csv.drop(['manufacturer', 'mfs'], axis=1)
        
    # interactions
    try: csv['age_x_etiv'] = csv['age'] * csv['etiv']
    except: pass
    try: csv['age_x_sex_m'] = csv['age'] * csv['sex_m']
    except: pass
    try: csv['etiv_x_sex_m'] = csv['sex_m'] * csv['etiv']
    except: pass
    csv['etiv_x_mfs_15'] = csv['mfs_15'] * csv['etiv']
    csv['mfs_15_x_manufacturer_philips'] = csv['manufacturer_philips'] * csv['mfs_15']
    csv['mfs_15_x_manufacturer_ge'] = csv['manufacturer_ge'] * csv['mfs_15']
    
    #if verbose == 'on': print('Variables coding done')
    csv.to_csv(outputpath + 'raw_scores/csv_in.csv')
    ### Calculate Z scores
    data = csv  
    try: data = data.set_index('id')
    except: pass
    fslist = pd.read_csv(current_path + '/bin/fsvarlist.csv')
    
    for f in fsfilelist:
        #print(f)
        try:
            FSdata = pd.read_csv(outputpath + '/raw_scores/' + f, index_col=0)
            FSdata.columns = FSdata.columns.str.lower()
            # remove rows with non-numeric values
            FSdata.replace('--', np.nan, inplace=True)
            try: 
                for x in ['3rd-ventricle', 'left-inf-lat-vent', 'left-lateral-ventricle', 'right-inf-lat-vent', 'right-lateral-ventricle', 'ventricles']:
                    FSdata[x] = np.log10(FSdata[x])
            except: pass
            region_list = fslist[f].dropna()
            # remove non pertinent variables
            suffix_drop = ['curvind', 'foldind', 'gauscurv', 'numvert', 'meancurv', 'thickstd']
            drop_list = [x for x in region_list.tolist() if x.endswith(tuple(suffix_drop))]
            region_list = [x for x in region_list.tolist() if x not in drop_list]
        
            # match sociodemo with FS outpout file
            data2 = pd.merge(data, FSdata, how='inner', left_index=True, right_index=True, suffixes=('', '_y'))
            data2.drop(data2.filter(regex='_y$').columns.tolist(),axis=1, inplace=True)
            # add CNR regions
            if any(x in f for x in ['aseg', 'exvivo', 'wm', 'brainstem', 'hpcsub']) == False:
                if 'pialDKT' in f : ff = f.replace('pialDKT', 'DKTatlas')
                else: ff = f.replace('.pial', '')
                CNRdata = pd.read_csv(outputpath + 'CNR/' + ff, index_col=0, na_values=['--'])
                
                data2 = pd.merge(data2, CNRdata, how='inner', left_index=True, right_index=True, suffixes=('', '_y'))
                data2.drop(data2.filter(regex='_y$').columns.tolist(),axis=1, inplace=True)
            # add totalgray CNR
            CNRdata2 = pd.read_csv(outputpath + 'CNR/aseg.csv', index_col=0)
            column_list = [x for x in CNRdata2.columns if x.endswith('_cnr')]
            CNRdata2 = CNRdata2[column_list]
            data2 = pd.merge(data2, CNRdata2, how='inner', left_index=True, right_index=True)
            pred_data = data2[region_list]
            z_data = data2[region_list]
            #region_ageall = pd.DataFrame()
            model_path = current_path + '/bin/models/' 
            # add region volume to each model
            for var in region_list:
                data3 = data2[data2[var].notna()]
                cnr = '_'.join(var.split('_')[:-1]) + '_cnr'
                if cnr not in data3.columns: cnr = 'totalgrayvol_cnr'
                if var in ['left_whitesurfarea','left_meanthickness', 'left_pialsurfarea']: cnr = 'lhcortexvol_cnr'
                if var in ['right_whitesurfarea','right_meanthickness', 'right_pialsurfarea']: cnr = 'rhcortexvol_cnr'
                #if f == 'brainstem.csv': cnr = 'brain-stem_cnr'
                if f == 'lhpcsub.csv': cnr = 'left-hippocampus_cnr'
                if f == 'rhpcsub.csv': cnr = 'right-hippocampus_cnr'
                
                # center age and etiv
                meanCNR = pd.read_csv(model_path + f + '/CNR_regions/' + var + '.csv')
                data3['cnr'] = data3[cnr] - meanCNR.iloc[0,0]
                # center volume and compute squared/cubed and/or interactions with CNR region
                data3['cnr2'] = data3['cnr']*data3['cnr'] 
                data3['cnr3'] = data3['cnr']*data3['cnr']*data3['cnr']
                #print(var)
                mse = pd.read_csv(model_path + f + '/Models/' + var + '_mse.csv', index_col=None, header=None)
                mse = mse.loc[0,0]
                loaded_model = pickle.load(open(model_path + f + '/Models/' + var + '.sav', 'rb'))
                pred_list = pd.Series(pd.read_csv(model_path + f + '/Models/' + var + '.csv').columns)
                x_select = data3.copy()
                x_select = x_select.loc[:,pred_list]    
                pred = loaded_model.predict(x_select)
                pred = pd.DataFrame(pred, columns=[str(var) + '_pred']).set_index(x_select.index)
                # add to dataset 
                pred_data = pd.merge(pred_data, pred, how='outer', left_index=True, right_index=True)
                # compute z scores
                z_data[str(var) + '_z'] = (pred_data[var] - pred_data[str(var) + '_pred']) / np.sqrt(mse)
            
               
            z_data = z_data.drop(labels=region_list, axis=1)
            z_data.columns = z_data.columns.str.replace(r'_z$', '', regex=True)
            z_data.to_csv(outputpath + 'normative_z_scores/' + f)
            if verbose == 'on': print(f + ' normative Z scores were saved in ', outputpath + 'normative_z_scores/')
            
        except: 
            print('There was problem. Normative data for ' + f + ' were not saved')
            pass

