import os
import sys

from utils.misc import csv_read_drop_index


def train_classifiers(fv, fv_path):
	print('\n> Training the classifiers for feature vector "%s"' % fv_path)
	pass


def train_classifiers_argparse(args):
	if args.fv is None or not os.path.exists(args.fv):
		print("Enter a valid path to a feature vector...")
		sys.exit(0)
	
	df = csv_read_drop_index(args.fv)
	
	train_classifiers(df, args.fv)
