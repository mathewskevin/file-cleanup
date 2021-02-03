import os
import pandas as pd

root_dir = r'/home/kevin/My_Stuff/My_Storage'

# function to read folders in directory
def read_directory(cur_dir):
	mid_list = os.listdir(cur_dir)
	directories = [name for name in mid_list if os.path.isdir(os.path.join(cur_dir, name))]
	files = [i for i in mid_list if i not in directories]
	return directories, files

# function to walk directory tree & populate database with filenames
def directory_tree(mid_dir, full_dict = {}):
	mid_directories, mid_files = read_directory(mid_dir)
	mid_df = pd.DataFrame(mid_files, columns={'Files'})
	mid_df['Directory'] = mid_dir
	
	full_dict[mid_dir] = mid_df
	if len(mid_directories) != 0: # keep searching deeper 
		for mid_folder in mid_directories:
			new_dir = os.path.join(mid_dir, mid_folder)
			directory_tree(new_dir, full_dict)
	else: # add deepest folder to list
		print(mid_dir)
	return full_dict
	
print('starting...')
	
# read data
out_dict = directory_tree(root_dir)

# create output dataframe
keys = [i for i in out_dict.keys()]
out_df = pd.DataFrame()
for key in keys:
    out_df = pd.concat([out_df,out_dict.get(key)])

# save data
out_df.to_csv('output.csv',index=None)

print('done.')