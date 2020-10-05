import re, os, pdb
import time, datetime
import pandas as pd

location = r'...'
search_string = r'...'

# https://stackoverflow.com/questions/9574793/how-to-convert-a-python-datetime-datetime-to-excel-serial-date-number
def excel_date(date1):
    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def search_folder(location, search_regex):
    for folder, subfolders, filenames in os.walk(location):
        for filename in filenames:
            try:
                search_result = search_regex.search(filename)
                # https://stackoverflow.com/questions/23086383/how-to-test-nonetype-in-python
                if search_result is not None:
                    size_bytes = os.path.getsize(os.path.join(folder, filename))
					# https://www.geeksforgeeks.org/python-os-path-getmtime-method/
                    mtime = os.path.getmtime(os.path.join(folder, filename)) # modification time
                    # https://stackoverflow.com/questions/10256093/how-to-convert-ctime-to-datetime-in-python
                    local_time = datetime.datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")
                    local_time = excel_date(local_time)
                    yield folder, filename, local_time, size_bytes
            except FileNotFoundError:
                pass
    			# maybe log error, maybe `pass`, maybe raise an exception
                # (halting further processing), maybe return an error object

if __name__ == '__main__':
    # check that file list is not open
    example_df = pd.DataFrame(['test'])
    example_df.to_csv('search_file_list.csv', index=None)
	
    search_regex = re.compile(search_string, re.I)	
    out_list = []
    print('Searching location: %s' % (location))
    for folder, filename, local_time, size in search_folder(location, search_regex):
        print(filename)
        out_list.append([folder, filename, local_time, size])
	
    df_out = pd.DataFrame(out_list)
    if df_out.shape == (0, 0):
        print('None found.')
    else:
	
        df_out.columns = ['Folder','Filename','Last Modified','File Size (Bytes)']
	
	    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.divide.html
	    # convert file size from bytes to MB
        divider = pd.Series([1e6]*df_out.shape[0])
        df_out['File Size (MB)'] = df_out['File Size (Bytes)'].divide(divider, fill_value=0).round(2)

        divider = pd.Series([1e9]*df_out.shape[0])
        df_out['File Size (GB)'] = df_out['File Size (Bytes)'].divide(divider, fill_value=0).round(2)	
	
        df_out.drop('File Size (Bytes)', axis=1, inplace=True)
	
	    # write to csv
        df_out.to_csv('search_file_list.csv', index=None)

print('done.')