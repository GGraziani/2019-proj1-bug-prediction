import os


DEF_LFV_DIR = 'res/labeled_feature_vectors'


def get_buggy_classes_in_file(path, file):
	buggy_classes = []
	if file.endswith(".src"):
		f = open(path + "/" + file, "r")
		for line in f.readlines():
			class_name = get_buggy_class_name(line)
			if class_name is not None:
				buggy_classes.append(class_name)
	
	return buggy_classes


def get_buggy_class_name(line):
	class_name = None
	
	line = line.rstrip()
	if ".jscomp." in line:
		class_name = line.split(".")[-1]
	
	return class_name


def get_dir_time_suffix(path, suffix):
	return os.path.splitext(os.path.basename(path))[0].replace(suffix, '')
