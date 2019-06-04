import os
import sys

from utils.label_utils import get_dir_time_suffix
from utils.misc import csv_read_drop_index, write_df_to_csv
from utils.training_utils import *

from utils.training_utils import DEF_TR_DIR, CLASSIFIERS


def train_classifiers(fv, fv_path):
	print('\n> Training the classifiers for feature vector "%s"' % fv_path)
	
	classes, data, labels = split_labeled_fv(fv)
	
	tt, r_num = produce_trainings_and_tests(data, labels)
	
	run_all_classifiers(CLASSIFIERS, fv_path, tt, r_num)
	
	
def run_all_classifiers(classifiers, fv_path, tt, r_num):
	for key, value in classifiers.items():
		run_training(value, key, fv_path, tt, r_num)
	

def run_training(classifier, classifier_name, fv_path, tt, r_num):
	l_precision, l_recall, l_fscore, l_accurancy = [], [], [], []
	
	print(indent('\n- Training classifier "%s"...' % classifier_name))
	
	for i in range(0, len(r_num)):
		pred, acc = run_classifier(
			classifier,
			tt['x_trains'][i],
			tt['x_tests'][i],
			tt['y_trains'][i],
			tt['y_tests'][i])
		
		prec, rec, f1 = get_prec_recall_fscore(tt['y_tests'][i], pred)

		l_accurancy.append(acc)
		l_precision.append(prec)
		l_recall.append(rec)
		l_fscore.append(f1)

	df = pd.DataFrame(
		{
			"r_num": r_num,
			"accuracy": l_accurancy,
			"precision": l_precision,
			"recall": l_recall,
			"fscore": l_fscore
		})

	tr_folder = DEF_TR_DIR + '/' + get_dir_time_suffix(fv_path, 'label_feature_vector-')

	path = write_df_to_csv(tr_folder, df, classifier_name.replace(' ', ''))
	print(indent('\nResults written to file "%s"' % path, spaces=10))
	
	print_averages(df)
	
	make_plot(r_num, df[['accuracy', 'precision', 'recall', 'fscore']], classifier_name, tr_folder)
	
	
def run_classifier(clf, x_train, x_test, y_train, y_test):
	
	clf = clf.fit(x_train, y_train)
	prediction = clf.predict(x_test)
	accuracy = clf.score(x_test, y_test)

	return prediction, accuracy


def train_classifiers_argparse(args):
	if args.fv is None or not os.path.exists(args.fv):
		print("Enter a valid path to a feature vector...")
		sys.exit(0)
	
	df = csv_read_drop_index(args.fv)
	
	train_classifiers(df, args.fv)
