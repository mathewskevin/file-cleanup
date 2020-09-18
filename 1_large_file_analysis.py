#! /usr/bin/env python3
# creates a CSV analysis of large system files given folder.

# https://codereview.stackexchange.com/questions/174754/finding-large-files
import os
import pandas as pd

def search_folder(location, min_filesize):
    for folder, subfolders, filenames in os.walk(location):
        for filename in filenames:
            try:
                size_bytes = os.path.getsize(os.path.join(folder, filename))
                if min_filesize * 1024 ** 2 <= size_bytes:
                    yield folder, filename, size_bytes
            except FileNotFoundError:
                pass
    			# maybe log error, maybe `pass`, maybe raise an exception
                # (halting further processing), maybe return an error object

if __name__ == '__main__':
    print('This program searches for ...')
    location = r'...'
    filesize = 100 # file size in MB
	
    out_list = []
    print('Files larger than %d MB in location: %s' % (filesize, location))
    for folder, filename, size in search_folder(location, filesize):
        print(filename, size)
        out_list.append([folder, filename, size])
	
    df_out = pd.DataFrame(out_list)
    df_out.columns = ['Folder','Filename','File Size (Bytes)']
	
	# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.divide.html
	# convert file size from bytes to MB
    divider = pd.Series([1e6]*df_out.shape[0])
    df_out['File Size (MB)'] = df_out['File Size (Bytes)'].divide(divider, fill_value=0).round(2)

    divider = pd.Series([1e9]*df_out.shape[0])
    df_out['File Size (GB)'] = df_out['File Size (Bytes)'].divide(divider, fill_value=0).round(2)	
	
    df_out.drop('File Size (Bytes)', axis=1, inplace=True)
	
	# write to csv
    df_out.to_csv('large_file_list.csv', index=None)

print('done.')