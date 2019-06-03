import datetime
import os


def add_delimiter(path):
	if not path.endswith('/'):
		return path+'/'
	return path


def gen_name(name):
	return name + '-' + str(int(datetime.datetime.now().timestamp()*1000))


def indent(text, spaces=4):
	spaces = ' ' * spaces
	return '\n'.join(spaces + line if line.strip() != '' else line for line in text.split('\n'))


def list_get(li, index, fallback=None):
	try:
		return li[index]
	except IndexError:
		return fallback
	

def df_sort_cols(df, sorted):
	return df.reindex(sorted, axis=1)


def write_df_to_csv(folder, df, name):
	if not os.path.exists(folder):
		os.makedirs(folder)

	file_path = folder + '/' + name + ".csv"
	
	df.to_csv(file_path)
	
	return file_path
