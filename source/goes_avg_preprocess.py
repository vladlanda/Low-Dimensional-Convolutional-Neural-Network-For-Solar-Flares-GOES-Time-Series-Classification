# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:38:11 2020

@author: uDuSa
"""
#%% Imports
import pandas as pd
import os
import glob
from matplotlib import pyplot as plt
import pickle

from tools import *

#%% Create year folders list
goes10_year_folders = [str(a) for a in range(1998,2006)]+['2008']
goes11_year_folders = ['2006','2007']

goes_dict = {'goes10':[str(a) for a in range(1998,2010)],
             'goes14':[str(2010)],
             'goes15':[str(a) for a in range(2011,2020)]}

print('goes_dict',goes_dict)
#%%
def concate_year_files(year_folder,goes_folder='goes15',xray_signature = 'g15_xrs_2s*.csv'):
    
    folders_path = os.path.join('..', 'data', 'data_goes','avg',year_folder,'*',goes_folder,'csv',xray_signature)
    ls = glob.glob(folders_path,recursive = True)
    ls.sort()
    
    data_matrix = []
    print('Loading : {}...'.format(year_folder),end='\r')
    for xray_file in ls:

        file_df = convert_goes_to_pandas(xray_file)
        # print(file_df[['B_FLUX']].isna().any() == False)
        
        # try:
        #     if file_df[['xl']].isna().values.any() : print(xray_file)
        #     i = (file_df['xl'] <= 1e-9)
        # except Exception as e:print(xray_file)
        
        data_matrix.append(file_df)

    print('Year {} loaded...'.format(year_folder))
    return data_matrix


goes_folder_arg = []
xray_signature_arg = []
year_folders = []

for lbl,data in goes_dict.items():
    goes_folder_arg += [lbl]*len(data)
    xray_signature_arg +=  ['g1*xrs_1m*.csv']*len(data)
    year_folders += data

print(goes_folder_arg)
print(xray_signature_arg)
print(year_folders)
#%%
all_years_data = list(map(concate_year_files,year_folders,goes_folder_arg,xray_signature_arg))
#%% create raw_years_data_dict
raw_years_data_dict = {}
for year_df_list,year_label in zip(all_years_data,year_folders):
    raw_years_data_dict[year_label] = pd.concat(year_df_list,ignore_index=True)
#%% Plot samples
raw_years_data_dict['1998']['xl'].plot()
plt.show()
raw_years_data_dict['2010']['B_AVG'].plot()
plt.show()
raw_years_data_dict['2014']['B_AVG'].plot()
plt.show()
raw_years_data_dict['2015']['B_AVG'].plot()
plt.show()

#%% Remove bad readings and save as numpy xl data ('time_tag','1.0-0.8nm')
def remove_anomaly_data(year_df):
    xray_1_08nm = 'xl' 
    MIN_VALUE = 1e-9
    
    try:
        year_df.rename(columns={"B_AVG": xray_1_08nm},inplace=True)
    except:pass
    
    # Remove bad reads
    indx = year_df[(year_df[xray_1_08nm] <= MIN_VALUE)].index
    year_df.drop(indx , inplace=True)
    
    # Interpolate bad reads
    # indx = (year_df[xray_1_08nm] <= MIN_VALUE)
    # year_df[indx] = None
    # year_df.interpolate(method='linear',inplace=True)
    
    return year_df
    

years_data_dict = {}
for year_label,year_df in raw_years_data_dict.items(): 
    
    year = remove_anomaly_data(year_df)
    years_data_dict[year_label] = year

    xl_avg_flux_file_path = os.path.join('..','data','data_goes','xray_avg_1m_numpy_data',year_label)

    np.save(xl_avg_flux_file_path,year[['time_tag','xl']].values)
    print((xl_avg_flux_file_path),' saved!...')

#%% Plot saved examples

plt.figure(figsize=(20,20))
plt.subplots_adjust(hspace=1)
for idx,year_label in enumerate(year_folders):
    xl_avg_flux_file_path = os.path.join('..','data','data_goes','xray_avg_1m_numpy_data',year_label+'.npy')
    array = np.load(xl_avg_flux_file_path,allow_pickle=True)
    
    plt.subplot(len(year_folders),1,idx+1)
    plt.title(year_label+' xray 1.0-0.8nm')
    plt.plot(array[:,1])
    
plt.show()





















