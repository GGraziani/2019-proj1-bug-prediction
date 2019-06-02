

def indent(text, spaces=4):
	spaces = ' ' * spaces
	return '\n'.join(spaces + line if line.strip() != '' else line for line in text.split('\n'))


def list_get(li, index, fallback=None):
	try:
		return li[index]
	except IndexError:
		return fallback
