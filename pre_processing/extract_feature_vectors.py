import os
import sys
import pandas as pd
import javalang as jl

from utils.misc import add_delimiter
from utils.pre_processing_utils import get_tree, get_num_of_public_methods, get_num_of_called_methods


def extract_feature_vectors(root):

	df = pd.DataFrame(
		columns=['class', 'MTH', 'FLD', 'RFC', 'INT', 'SZ', 'CPX', 'EX', 'RET', 'BCM', 'NML', 'WRD', 'DCM'])

	for top_class in get_top_classes(root):

		mth, fld, rfc, ints = get_class_metrics(top_class)
		

# returns all classes that have the same name as the container java file
def get_top_classes(root):
	top_classes = []
	for (path, dirs, files )in os.walk(root):
		for file in files:
			if file.endswith(".java"):
				file_path = add_delimiter(path) + file
				file_name = file.replace('.java', '')

				top_class = get_top_class(file_path, file_name)

				if top_class is not None:
					top_classes.append(top_class)

	return top_classes


# returns the class having the same name as the container java file
def get_top_class(file_path, file_name):
	for path, node in get_tree(file_path).filter(jl.tree.ClassDeclaration):
		if node.name == file_name:
			return node

	return None


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
