#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
from pathlib import Path
import glob
import numpy as np
import matplotlib.pyplot as plt
import os

def parseCSV2pandas(csv_file,n_rows2skip=138):
    #n_rows2skip = 138
    #pd_frame = pd.read_csv(csv_file,error_bad_lines=False,skiprows=n_rows2skip)
    pd_frame = pd.read_csv(csv_file,skiprows=n_rows2skip)
    n_columns = len(list(pd_frame.columns.values))
    if n_columns < 7:
        #print(csv_file)
        #pd_frame = pd.read_csv(csv_file,error_bad_lines=False,skiprows=n_rows2skip+1)
        pd_frame = pd.read_csv(csv_file,skiprows=n_rows2skip+1)
    return pd_frame

def convert_goes_to_pandas(csv_file_name):
    n_rows2skip = 1
    try:
        with open(csv_file_name,'r') as file:
            for line in file:
                if 'data:' in line: break
                n_rows2skip += 1
        #print(n_rows2skip)
        pd_frame = pd.read_csv(csv_file_name,skiprows=n_rows2skip)
        return pd_frame
    except Exception as e: print(e,csv_file_name)


def listOfFiles(root_dir='data_goes',file_regx='*.csv'):
    regex = root_dir+'/**/'+file_regx
    files_list = glob.glob(regex,recursive = True)
    return files_list

def listOfFolders(folder='goes*'):
    folders_path = os.path.join('..', 'data', 'data_goes','201[123456789]','*',folder)
    #ls = glob.glob('data_goes/201[123456789]/*/'+folder,recursive = True)
    ls = glob.glob(folders_path,recursive = True)
    ls.sort()
    return ls

def fillMissedData(files=[],flux_type = 'A_FLUX'):
    ARR_SIZE = 42188
    data_matrix = []
    for file in files:

        data_frame = parseCSV2pandas(file)
        time_str = [s.split()[1] for s in data_frame[['time_tag']].values.squeeze() if len(s.split()) > 1]
        time_millis = list(map(lambda x: float(x.split(':')[0])*60*60+float(x.split(':')[1])*60+float(x.split(':')[2]),time_str))
        time_series_data = data_frame[[flux_type]].values
        
        time_series_data = time_series_data.squeeze().tolist()
        
        
        data_array = []
        for ind,(i,j,data) in enumerate(zip(time_millis[:-1],time_millis[1:],time_series_data[:-1])):
            data_array.append(data)
            if j-i > 2.051:
                #print(ind,j-i,str_second_time[ind],str_second_time[ind+1])
                deltaT = j-i-2
                expand = [0] * int(deltaT/2.0479691697114157)
                data_array.extend(expand)
        data_array.append(time_series_data[-1])
        delta_series = 42188 - len(data_array)
        if delta_series > 0:
            data_array.extend([0]*delta_series)
        elif delta_series < 0:
            data_array = data_array[:delta_series]
        #if np.std(data_array) > 0:
        data_matrix.append(data_array)
        
    final_data = np.array(data_matrix)
    final_data[np.where(np.isnan(final_data) == True)] = 0
    final_data[np.where(final_data <= 0)] = np.min(final_data[np.where(final_data > 0)])
    return final_data

def averageByTime(data_matrix,avg_time_s = 2):
    assert avg_time_s % 2 == 0
    avg_time_s = 1 if avg_time_s < 2 else avg_time_s/2
    avg_time_s = int(avg_time_s)
    
    #print(avg_time_s)
    
    data_entries,data_lenght = data_matrix.shape
    mod = data_lenght % avg_time_s
    new_length = int(data_lenght/avg_time_s)
    
    #print(data_entries,data_lenght,mod,new_length)
    
    data = data_matrix[:,:data_lenght-mod]
    data = data.reshape(-1,avg_time_s)
    #print(data)
    return np.mean(data,axis=1).reshape(data_entries,-1)


# In[2]:


def hhmmss2seconds(time_format):
    spt = time_format.split(':')
    ans = 0.0
    print(spt)
    for i,s in enumerate(spt):
        ans += 60**(len(spt)-i-1) * float(s)
    return ans


if __name__ == '__main__':
    
    files = listOfFiles(root_dir='*/201[4]',file_regx='g15_xrs*')
    #print(len(files))
    #f = 'data_goes\\2018\\03\\goes15\\csv\\g15_xrs_2s_20180311_20180311.csv'
#     f.replace('\\','/')
    #print(f)
    fillMissedData(files)
    #f = files[0]
    
    #files = ['data_goes/2011/02/goes15/csv/g15_xrs_2s_20110223_20110223.csv']
#     for f in files[200:400]:
#         pd1 = parseCSV2pandas(f)
#         str_second_time = [s.split()[1] for s in pd1[['time_tag']].values.squeeze()]
#         seconds_time = list(map(lambda x: float(x.split(':')[0])*60*60+float(x.split(':')[1])*60+float(x.split(':')[2]),str_second_time))

#         sum =0 
#         tms2 = []

#         for ind,(i,j) in enumerate(zip(seconds_time[:-1],seconds_time[1:])):
#             tms2.append(i)
#             if j-i > 2.051:
#                 #print(ind,j-i,str_second_time[ind],str_second_time[ind+1])
#                 deltaT = j-i-2
#                 expand = [0] * int(deltaT/2.0479691697114157)
#                 tms2.extend(expand)
#         tms2.append(seconds_time[-1])
#         delta_series = 42188 - len(tms2)
#         if delta_series > 0:
#             tms2.extend([0]*delta_series)
#         elif delta_series < 0:
#             tms2 = tms2[:delta_series]
    #tms2 = fillMissedData(files)
    #print(tms2,tms2.shape)
    #print(len(tms2),42188-len(tms2))
        #plt.plot(seconds_time)
        #plt.plot(tms2)
        #plt.show()
    
#listOfFiles('data_geos','geos','xrs*.csv')    


# ValueError: zero-size array to reduction operation minimum which has no identity

# In[ ]:




