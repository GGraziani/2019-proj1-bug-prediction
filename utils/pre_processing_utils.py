import javalang as jl

# returns the AST of a java file
def get_tree(path):
	with open(path) as f:
		return jl.parse.parse(f.read())


def get_num_of_public_methods(p_class):
	n = 0
	for path, node in p_class.filter(jl.tree.MethodDeclaration):
		if 'public' in node.modifiers:
			n += 1
	return n


def get_num_of_called_methods(p_class):
	n = 0
	for m in p_class.methods:
		print(len(m.filter(jl.tree.Invocation)))
		for path, node in m.filter(jl.tree.Invocation):
			n += 1

	return n
