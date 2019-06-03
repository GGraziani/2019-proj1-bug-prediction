import os
import javalang as jl

from utils.misc import add_delimiter

DEF_FV_DIR = 'res/feature_vectors'
FV_COLS = ['class', 'MTH', 'FLD', 'RFC', 'INT', 'SZ', 'CPX', 'EX', 'RET', 'BCM', 'NML', 'WRD', 'DCM']


def get_avg_method_name_len(methods):
	sum_len = 0
	
	if len(methods) == 0:
		return 0
	
	for method in methods:
		sum_len += len(method.name)

	return sum_len / len(methods)


# Returns the method metrics for one single metrics
def get_method_metrics(method):
	sz, cpx, ex, ret = 0, 0, 0, 0
	
	for path, node in method:
		sz += 1 if type(node).__base__ is jl.tree.Statement and type(node) is not jl.tree.BlockStatement else 0
		
		cpx += 1 if type(node) in [
			jl.tree.IfStatement,
			jl.tree.SwitchStatement,
			jl.tree.WhileStatement,
			jl.tree.DoStatement,
			jl.tree.WhileStatement,
			jl.tree.ForStatement] else 0
		
		ret += 1 if type(node) is jl.tree.ReturnStatement else 0
		
		ex += len(node.throws) if type(node) is jl.tree.MethodDeclaration and node.throws is not None else 0
	
	return sz, cpx, ex, ret


def get_num_of_called_methods(p_class):
	n = 0
	
	for method in p_class.methods:
		for _ in method.filter(jl.tree.Invocation):
			n += 1

	return n


def get_num_of_public_methods(p_class):
	n = 0
	for path, node in p_class.filter(jl.tree.MethodDeclaration):
		if 'public' in node.modifiers:
			n += 1
	return n


def get_num_of_statements(methods):
	num_of_stmts = 0
	
	for m in methods:
		for path, node in m.filter(jl.tree.Statement):
			if not isinstance(node, jl.tree.BlockStatement):
				num_of_stmts += 1
	
	return num_of_stmts


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
