import datetime
import os
import pandas as pd


def add_delimiter(path):
	if not path.endswith('/'):
		return path+'/'
	return path


def df_sort_cols(df, sorted):
	return df.reindex(sorted, axis=1)


def gen_name_with_time(name):
	return name + '-' + str(int(datetime.datetime.now().timestamp()*1000))


def gen_name_with_suffix(pref, suff):
	return pref + suff


def indent(text, spaces=4):
	spaces = ' ' * spaces
	return '\n'.join(spaces + line if line.strip() != '' else line for line in text.split('\n'))


def list_get(li, index, fallback=None):
	try:
		return li[index]
	except IndexError:
		return fallback


def csv_read_drop_index(file_path):
	df = pd.read_csv(file_path)
	df = df.drop(df.columns[0], axis=1)
	return df


def write_df_to_csv(folder, df, name):
	if not os.path.exists(folder):
		os.makedirs(folder)

	file_path = folder + '/' + name + ".csv"
	
	df.to_csv(file_path)
	
	return file_path
