import sys
import argparse


# add one gateway function for each functionality
from utils.doc_utils import MODULE_DOCSTRINGS, DOCSTRING
from utils.misc import list_get


def extract_feature_vectors_gateway(args):
	from pre_processing import extract_feature_vectors
	extract_feature_vectors.extract_feature_vectors_argparse(args)
	
	
def label_feature_vectors_gateway(args):
	pass


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# add subparser for extract_feature_vectors
p_extract_feature_vectors = subparsers.add_parser('extract_feature_vectors')
p_extract_feature_vectors.add_argument('-s', '--source', dest='source', default=None)
p_extract_feature_vectors.set_defaults(func=extract_feature_vectors_gateway)

# add subparser for label_feature_vectors
p_label_feature_vectors = subparsers.add_parser('label_feature_vectors')
p_label_feature_vectors.add_argument('-fv', '--feature_vector', dest='fv', default=None)
p_label_feature_vectors.add_argument('-b', '--buggy_classes', dest='buggy', default=None)
p_label_feature_vectors.set_defaults(func=label_feature_vectors_gateway)


def main(argv):
	helpstrings = {'', '-h', '--help'}

	command = list_get(argv, 0, '').lower()

	# The user did not enter a command, or the entered command is not recognized.
	if command not in MODULE_DOCSTRINGS:
		print(DOCSTRING)
		if command == '':
			print('You are seeing the default help text because you did not choose a command.')
		elif command not in helpstrings:
			print('You are seeing the default help text because "%s" was not recognized' % command)
		return 1

	# The user entered a command, but no further arguments, or just help.
	argument = list_get(argv, 1, '').lower()
	if argument in helpstrings:
		print(MODULE_DOCSTRINGS[command])
		return 1

	args = parser.parse_args(argv)
	args.func(args)

	return 0


if __name__ == '__main__':
	raise SystemExit(main(sys.argv[1:]))
