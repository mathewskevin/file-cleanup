# This script creates a CSV file which lists all folders and files in a directory.
# 06/21/2021 - expanded to analyze multiple separate directories

import os, pdb
import pandas as pd
import time, datetime

# set output filename
output_csv_name = 'xcom.csv'

# set folders to search in
root_dir_1 = r'D:\Program Files (x86)\Steam\steamapps\common\XCOM 2'
root_dir_2 = r'D:\Program Files (x86)\Steam\steamapps\common\XCOM 2 SDK'
root_dir_3 = r'D:\Program Files (x86)\Steam\steamapps\common\XCOM 2 War of the Chosen SDK'

# put all folders into list to loop through
root_dir_list = [root_dir_1, root_dir_2, root_dir_3]

# funciton to convert python datetime to excel date
# https://stackoverflow.com/questions/9574793/how-to-convert-a-python-datetime-datetime-to-excel-serial-date-number
def excel_date(date1):
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

# function to get file extension from filename
def file_extension(filename):
	file_ext = os.path.splitext(filename)[~0]
	return file_ext

# function to read folders in directory
def read_directory(cur_dir):
	
	# reset data
	directories = []; files = []
	file_sizes = [0]; file_dates = [0]
	
	# option to skip directory based on string
	#if 'String' not in cur_dir and cur_dir != root_dir:
	#	files = ['Skipped']
	#	return directories, files, file_sizes, file_dates
	
	# try-except for handling permission denied to folder
	try:
		mid_list = os.listdir(cur_dir)
	except:
		files = ['Permission Denied']
		return directories, files, file_sizes, file_dates
	
	# loop through all items for directories
	directories = [name for name in mid_list if os.path.isdir(os.path.join(cur_dir, name))]
	
	# re-loop to find files
	files = [i for i in mid_list if i not in directories]
	
	# get file sizes and creation dates for each file
	file_sizes = []; file_dates = []
	for filename in files:
		size_bytes = os.path.getsize(os.path.join(cur_dir, filename))
		# https://www.geeksforgeeks.org/python-os-path-getmtime-method/
		mtime = os.path.getmtime(os.path.join(cur_dir, filename)) # modification time
		# https://stackoverflow.com/questions/10256093/how-to-convert-ctime-to-datetime-in-python
		local_time = datetime.datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")
		local_time = excel_date(local_time)
		
		file_sizes.append(size_bytes)
		file_dates.append(local_time)

	return directories, files, file_sizes, file_dates

# function to walk directory tree & populate database with filenames
def directory_tree(mid_dir, full_dict = {}):
	
	mid_directories, mid_files, mid_sizes, mid_dates = read_directory(mid_dir)
	
	# https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
	mid_df = pd.DataFrame(list(zip(mid_dates, mid_sizes, mid_files)), columns=['Date','Size','File Name'])
	mid_df['Directory'] = mid_dir
	
	full_dict[mid_dir] = mid_df

	if len(mid_directories) != 0: # keep searching deeper
		for mid_folder in mid_directories:
			new_dir = os.path.join(mid_dir, mid_folder)
			directory_tree(new_dir, full_dict)
	else: # add deepest folder to list
		print(mid_dir)
	return full_dict
		
if __name__ == "__main__":
	print('starting...')
	
	out_df = pd.DataFrame()
	
	# cycle through all desired search folders
	for root_dir in root_dir_list:
		
		out_dict = {} # reset output dictionary
		out_dict = directory_tree(root_dir, {}) # read data

		print('adding to output dataframe...')
		
		# convert dictionary to dataframe and add output dataframe
		keys = [i for i in out_dict.keys()]
		for key in keys:
			mid_df = out_dict.get(key)
			mid_df['Search Dir'] = root_dir
			out_df = pd.concat([out_df, mid_df])
		
	print('completed search, assembling csv file...')
	
	# reorganize for readability
	out_df = out_df[['Search Dir','Directory','Size','Date','File Name']]
	
	# file extensions
	out_df['Extension'] = out_df['File Name'].apply(file_extension)
	
	# remove duplicates
	out_df.drop_duplicates(inplace=True)
		
	# save data
	out_df.to_csv(output_csv_name, index=None)

	print('done.')
