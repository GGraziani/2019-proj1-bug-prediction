import os

import pandas as pd

import sklearn
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

from utils.misc import ones, indent, mkdir

DEF_EVAL_DIR = 'res/evaluations'


def cross_validate(clf, data, labels):
	return sklearn.model_selection.cross_validate(
		clf, data, labels,
		cv=5,
		return_train_score=True,
		scoring={'f1': 'f1', 'precision': 'precision', 'recall': 'recall'})


def run_cross_validation(clf, data, labels):
	scores = cross_validate(clf, data, labels)
	df_out = pd.DataFrame(scores)

	for i in range(1, 20):
		scores = cross_validate(clf, data, labels)
	
		df_tmp = pd.DataFrame(scores)
		df_out = df_out.append(df_tmp)
	
	return df_out


def make_boxplot_all(metrics, folder):
	
	b_folder = mkdir(folder + '/boxplots')
		
	for key, val in metrics.items():
		make_boxplot(val, key, b_folder)
	
	print(indent('\n- Boxplots written to folder "%s"' % b_folder))
	

def make_boxplot(df, title, folder):
	
	plt.figure(figsize=(12, 12))
	df.boxplot()
	plt.title(title + ' boxplot')
	
	path = folder + '/' + title.replace(" ", "") + '.png'
	plt.savefig(path)
	plt.clf()


def split_and_compute_stats(data, labels):
	x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)
	return precision_recall_fscore_support(y_test, ones(len(y_test)), average='binary')
