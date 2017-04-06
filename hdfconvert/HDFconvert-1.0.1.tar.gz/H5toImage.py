
# coding: utf-8

# In[1]:

import h5py
from PIL import Image
import os, sys

'''
Convert array in H5 to Image
'''

def h5toImage(load_path, save_path, file_name, target):
    '''
    load_path: directory path to load
    save_path: directory path to save
    file_name: all of name in loading directory
    target: target name in hdf file
    '''
    if load_path[-1] != '/':
        load_path = load_path + '/'
    if save_path[-1] != '/':
        save_path = save_path + '/'
    f = h5py.File(load_path + file_name, 'r') # Read font file
    all_data = f[target] # hdf has feature & unicode, need sub file name
    os.makedirs(save_path + file_name) # Make a directory to save images. If it exists, WindowsError
    for idx, cur_arr in enumerate(all_data): # array dim
        im = Image.fromarray(cur_arr)
        im.save(save_path + file_name + '/' + str(idx) + '.jpeg')
    return True

def makeDataset(load_path, save_path, target):
    file_list = os.listdir(load_path)
    for idx, cur_file in enumerate(file_list):
        cur_status = (float(idx) / len(file_list)) * 100
        cur_num = int(cur_status // 10)
        h5toImage(load_path, save_path, cur_file)
        sys.stdout.write(str('\r' +
                  '■'*cur_num + '□'*(10-cur_num) + 
                  ' {:03.2f}'.format(cur_status) + '% Current File: ' + cur_file)
                        )
    return True

def test():
    print("This library is H5toImage.")

if __name__ == "__main__":
    load_path, save_path, target = sys.argv[1], sys.argv[2], sys.argv[3]
    makeDataset(load_path, save_path, target)

