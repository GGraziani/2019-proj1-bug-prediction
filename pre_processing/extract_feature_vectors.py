import os
import sys


def extract_feature_vectors(god_classes):
	pass


def extract_feature_vectors_argparse(args):
	if args.source is None or not os.path.exists(args.source):
		print("Enter a valid path to a source code...")
		sys.exit(0)

	extract_feature_vectors(args.source)
