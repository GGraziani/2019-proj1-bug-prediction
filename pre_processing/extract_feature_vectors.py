import re
import sys
import pandas as pd

from utils.misc import write_df_to_csv, gen_name, df_sort_cols
from utils.pre_processing_utils import *


def extract_feature_vectors(root):
	print('\n> Starting feature vector extraction for project "%s"' % root)
	df = pd.DataFrame(columns=FV_COLS)

	for t_class in get_top_classes(root):

		mth, fld, rfc, ints = get_class_metrics(t_class)
		sz, cpx, ex, ret = get_methods_metrics(t_class)
		bcm, nml, wrd, dcm = get_npl_metrics(t_class)
		
		df = df.append({
			'class': t_class.name,                             # class name
			'MTH': mth, 'FLD': fld, 'RFC': rfc, 'INT': ints,   # CLASS METRICS
			'SZ': sz, 'CPX': cpx, 'EX': ex, 'RET': ret,        # METHOD METRICS
			'BCM': bcm, 'NML': nml, 'WRD': wrd, 'DCM': dcm     # NPL METRICS
		}, ignore_index=True, sort=-1)
	
	df = df_sort_cols(df, FV_COLS)
	path = write_df_to_csv(DEF_FV_DIR, df, gen_name('feature_vector'))
	print('> Feature vector/s has/ve been written to file "%s"' % os.path.abspath(path))
	
	return df, path
		
		
# return the maximum CLASS METRICS over all methods
def get_class_metrics(t_class):
	
	mth = len(t_class.methods)
	fld = len(t_class.fields)
	rfc = get_num_of_public_methods(t_class) + get_num_of_called_methods(t_class)
	ints = 0 if t_class.implements is None else len(t_class.implements)

	return mth, fld, rfc, ints


# return the maximum METHODS METRICS over all methods
def get_methods_metrics(t_class):
	sz, cpx, ex, ret = 0, 0, 0, 0
	
	for method in t_class.methods:
		t_sz, t_cpx, t_ex, t_ret = get_method_metrics(method)
		
		sz = max(sz, t_sz)
		cpx = max(cpx, t_cpx)
		ex = max(ex, t_ex)
		ret = max(ret, t_ret)
		
	return sz, cpx, ex, ret


# return the NPL METRICS over all methods
def get_npl_metrics(t_class):
	bcm, nml, wrd, dcm = 0, 0, 0, 0
	
	for path, node in t_class:
		if hasattr(node, 'documentation') and node.documentation is not None:
			bcm += 1
			
			doc_words = len(re.findall(r'\w+', node.documentation))
			wrd += doc_words
	
	statements = get_num_of_statements(t_class.methods)
	dcm = wrd/statements if statements != 0 else 0
	
	nml = get_avg_method_name_len(t_class.methods)

	return bcm, nml, wrd, dcm


def extract_feature_vectors_argparse(args):
	if args.source is None or not os.path.exists(args.source):
		print("Enter a valid path to a source code...")
		sys.exit(0)

	extract_feature_vectors(args.source)
