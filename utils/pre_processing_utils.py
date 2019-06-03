import os
import javalang as jl

from utils.misc import add_delimiter


def get_num_of_called_methods(p_class):
	n = 0
	for m in p_class.methods:
		print(len(m.filter(jl.tree.Invocation)))
		for path, node in m.filter(jl.tree.Invocation):
			n += 1
	
	return n


def get_num_of_public_methods(p_class):
	n = 0
	for path, node in p_class.filter(jl.tree.MethodDeclaration):
		if 'public' in node.modifiers:
			n += 1
	return n


# returns all classes that have the same name as the container java file
def get_top_classes(root):
	top_classes = []
	for (path, dirs, files) in os.walk(root):
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


# returns the AST of a java file
def get_tree(path):
	with open(path) as f:
		return jl.parse.parse(f.read())
