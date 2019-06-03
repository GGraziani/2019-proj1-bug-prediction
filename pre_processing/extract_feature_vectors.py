import os
import sys
import pandas as pd

from utils.pre_processing_utils import get_num_of_public_methods, get_num_of_called_methods, get_top_classes, \
	get_method_metrics


def extract_feature_vectors(root):

	df = pd.DataFrame(
		columns=['class', 'MTH', 'FLD', 'RFC', 'INT', 'SZ', 'CPX', 'EX', 'RET', 'BCM', 'NML', 'WRD', 'DCM'])

	for t_class in get_top_classes(root):

		mth, fld, rfc, ints = get_class_metrics(t_class)
		sz, cpx, ex, ret = get_methods_metrics(t_class)


# return the maximum CLASS METRICS over all methods
def get_class_metrics(t_class):
	
	mth = len(t_class.methods)

	fld = len(t_class.fields)

	rfc = get_num_of_public_methods(t_class) + get_num_of_called_methods(t_class)

	interfaces = t_class.implements
	ints = 0 if interfaces is None else len(interfaces)

	return mth, fld, rfc, ints


# return the maximum METHODS METRICS over all methods
def get_methods_metrics(p_class):
	sz, cpx, ex, ret = 0, 0, 0, 0
	
	for method in p_class.methods:
		t_sz, t_cpx, t_ex, t_ret = get_method_metrics(method)
		
		sz = max(sz, t_sz)
		cpx = max(cpx, t_cpx)
		ex = max(ex, t_ex)
		ret = max(ret, t_ret)
		
	return sz, cpx, ex, ret


def extract_feature_vectors_argparse(args):
	if args.source is None or not os.path.exists(args.source):
		print("Enter a valid path to a source code...")
		sys.exit(0)

	extract_feature_vectors(args.source)
