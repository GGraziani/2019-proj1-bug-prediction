import os
import sys
import pandas as pd
import scipy.stats

from utils.eval_utils import run_cross_validation, split_and_compute_stats, DEF_EVAL_DIR, make_boxplot_all
from utils.label_utils import get_dir_time_suffix
from utils.misc import csv_read_drop_index, write_df_to_csv, indent
from utils.training_utils import split_labeled_fv, CLASSIFIERS


def evaluate(fv, fv_path):
	print('\n> Evaluating the classifiers for feature vector "%s"' % fv_path)
	
	classes, data, labels = split_labeled_fv(fv)
	
	# Run 5-fold cross-validation
	metrics = run_cross_validation_all(data, labels)
	
	# add biased estimators
	metrics['precision']['b_estimator'], metrics['recall']['b_estimator'], metrics['fscore']['b_estimator'] = \
		gen_biased_estimators(data, labels)
	
	# Get evaluation directory
	eval_dir = DEF_EVAL_DIR + '/' + get_dir_time_suffix(fv_path, 'label_feature_vector-')
	
	# create one boxplot for each metric
	make_boxplot_all(metrics, eval_dir)

	# run wilcoxon test for each metric
	run_wilcoxon_test_all(metrics, eval_dir)

	
def run_cross_validation_all(data, labels):
	print(indent('\n- Running cross validation with 5-folds ...'))
	all_prec, all_recall, all_f1 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
	
	for label, clf in CLASSIFIERS.items():
		df = run_cross_validation(clf, data, labels)
		all_prec[label] = df['test_precision']
		all_recall[label] = df['test_recall']
		all_f1[label] = df['test_f1']

	return {
		'precision': all_prec,
		'recall': all_recall,
		'fscore': all_f1
	}


def gen_biased_estimators(data, labels):
	print(indent('\n- Generating biased estimators ...'))
	l_prec, l_recall, l_fscore = [], [], []

	for i in range(0, 100):
		prec, rec, f1, sup = split_and_compute_stats(data, labels)
		l_prec.append(prec)
		l_recall.append(rec)
		l_fscore.append(f1)

	return l_prec, l_recall, l_fscore


def run_wilcoxon_test_all(metrics, eval_dir):
	
	path = ''
	for key, val in metrics.items():
		path = run_wilcoxon_test(val, key, eval_dir)
	
	print(indent('\n- Wilcoxon tests results written to folder "%s"' % path))


def run_wilcoxon_test(df, name, folder):
	columns = df.columns.values
	t_df = pd.DataFrame(columns=columns, index=columns)
	
	for i in range(0, len(columns)-1):
		for j in range(i+1, len(columns)):

			stats, p_value = scipy.stats.mannwhitneyu(
				df[columns[i]].values,
				df[columns[j]].values,
				alternative='two-sided')
			
			t_df.iloc[j, i] = p_value
	
	return write_df_to_csv(folder + '/wilcoxon', t_df, name)
	

def evaluate_argparse(args):
	if args.fv is None or not os.path.exists(args.fv):
		print("Enter a valid path to a feature vector...")
		sys.exit(0)
	
	df = csv_read_drop_index(args.fv)
	
	evaluate(df, args.fv)
