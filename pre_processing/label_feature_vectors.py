import os
import pandas as pd
import sys

from utils.label_utils import get_dir_time_suffix, get_buggy_classes_in_file, DEF_LFV_DIR
from utils.misc import csv_read_drop_index, write_df_to_csv, gen_name_with_suffix


def label_feature_vectors(fv, fv_path, buggy_classes_dir):
	print('\n> Creating labels for feature vector "%s"' % fv_path)
	
	buggy_classes = get_buggy_classes(buggy_classes_dir)
	label_feature_vector = get_label_feature_vector(fv, buggy_classes)
	
	path = write_df_to_csv(
		DEF_LFV_DIR,
		label_feature_vector,
		gen_name_with_suffix('label_feature_vector', get_dir_time_suffix(fv_path, 'feature_vector')))
	
	print('> Labeled feature vector has been written to file "%s"' % os.path.abspath(path))
	
	return label_feature_vector, path


def get_buggy_classes(buggy_classes_dir):
	df = pd.DataFrame(columns=['class', 'buggy'])
	
	for (path, dirs, files) in os.walk(buggy_classes_dir):
		for file in files:
			for bc in get_buggy_classes_in_file(path, file):
				df = df.append({
					'class': bc, 'buggy': 1
				}, ignore_index=True, sort=-1)
	
	df.drop_duplicates(['class'], inplace=True)

	return df


def get_label_feature_vector(fv, buggy_classes):
	label_fv = pd.merge(fv, buggy_classes, how='left', left_on='class', right_on='class')
	label_fv = label_fv.fillna(0)
	
	label_fv.sort_values("class", inplace=True)
	label_fv.reset_index(drop=True, inplace=True)
	
	return label_fv
	
	
def label_feature_vectors_argparse(args):
	if args.fv is None or not os.path.exists(args.fv):
		print("Enter a valid path to a feature vector...")
		sys.exit(0)
		
	if args.buggy is None or not os.path.exists(args.buggy):
		print("Enter a valid path to a directory containing buggy classes...")
		sys.exit(0)
		
	df = csv_read_drop_index(args.fv)
	
	label_feature_vectors(df, args.fv, args.buggy)
