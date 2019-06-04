import numpy

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt

from utils.misc import indent

T_LOOPS = 70


# separate classes, data and buggies
def split_labeled_fv(fv):
	buggies = fv['buggy'].values
	classes = fv['class'].values
	data = fv.drop(['class', 'buggy'], axis=1)
	
	return classes, data, buggies


def print_averages(df):
	averages = df[['accuracy', 'precision', 'recall', 'fscore']].mean(axis=0)
	
	print(indent('\nPrinting averages:', spaces=10))
	
	for label, avg in averages.iteritems():
		print(indent('* Average %s: %s' % (label, str(avg)), spaces=14))
		

def produce_trainings_and_tests(data, labels):
	x_trains, x_tests, y_trains, y_tests, r_num = [], [], [], [], []
	
	r = 0
	for i in range(0, T_LOOPS):
		x_train, x_test, y_train, y_test = train_test_split(data, labels, train_size=0.8, test_size=0.2, random_state=i)
		
		x_trains.append(x_train)
		x_tests.append(x_test)
		y_trains.append(y_train)
		y_tests.append(y_test)
		r += 1
		r_num.append(r)
	
	return {'x_trains': x_trains, 'x_tests': x_tests, 'y_trains': y_trains, 'y_tests': y_tests}, r_num


def make_plot(x, data, title, folder):
	plt.figure(figsize=(26, 10))
	plt.title(title)
	
	plt.xlabel('Run')
	plt.ylabel('Accuracies')
	for col in data.columns:
		plt.plot(x, data[col].values,	marker='o', markersize=4, label=col)
	
	plt.legend()
	plt.grid(True)
	path = folder + '/' + title.replace(" ", "") + '.png'
	plt.savefig(path)
	plt.clf()
	
	print(indent('\nPlot saved to "%s"' % path, spaces=10))


def get_prec_recall_fscore(y_test, p_labels):
	prec, rec, f1, sup = precision_recall_fscore_support(y_test, p_labels, average='binary')
	
	return prec, rec, f1
