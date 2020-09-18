# unlink or move files using data from CSV file

import pandas as pd
import os, pdb
import send2trash

new_folder = os.path.join(os.getcwd(),'analysis_folder')
raw_data = pd.read_csv('large_file_list.csv')

print('running...')
for idx, row in raw_data.iterrows():
    old_folder = row['Folder']
    file_name = row['Filename']
    old_path = os.path.join(old_folder, file_name)
    if os.path.isfile(old_path):

		# delete file directly
		#os.unlink(file_path)
        #send2trash.send2trash(file_path)
		
		# move to analysis folder
		# https://stackoverflow.com/questions/8858008/how-to-move-a-file
        new_path = os.path.join(new_folder, file_name)
        os.rename(old_path, new_path)
		
    else:
	    print('error.', old_path)
		
print('done.')