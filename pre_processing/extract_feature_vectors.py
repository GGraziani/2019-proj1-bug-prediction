import os
import sys
import pandas as pd

from utils.pre_processing_utils import get_num_of_public_methods, get_num_of_called_methods, get_top_classes


def extract_feature_vectors(root):

	df = pd.DataFrame(
		columns=['class', 'MTH', 'FLD', 'RFC', 'INT', 'SZ', 'CPX', 'EX', 'RET', 'BCM', 'NML', 'WRD', 'DCM'])

	for top_class in get_top_classes(root):

		mth, fld, rfc, ints = get_class_metrics(top_class)
		

def get_class_metrics(p_class):
	
	mth = len(p_class.methods)

	fld = len(p_class.fields)

	rfc = get_num_of_public_methods(p_class) + get_num_of_called_methods(p_class)

	interfaces = p_class.implements
	ints = 0 if interfaces is None else len(interfaces)

	return mth, fld, rfc, ints


def extract_feature_vectors_argparse(args):
	if args.source is None or not os.path.exists(args.source):
		print("Enter a valid path to a source code...")
		sys.exit(0)

	extract_feature_vectors(args.source)
