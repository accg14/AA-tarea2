import sys, pdb

attributes = []
global_tuples = []
min_level = 0
max_level = 4
pipe = '|'

class Node:
	def __init__(self, leaf, value):
		self.leaf = leaf
		if (leaf):
			self.value = value
		else:
			self.label = value

	def get_value_or_label(self):
		if (self.leaf):
			return self.value
		else:
			return self.label

	def is_leaf(self):
		return self.leaf

	def get_childs(self):
		if not (self.leaf):
			return self.childs
		else:
			return -1

	def set_childs(self, childs):
		self.childs = childs


def create_flowers_set():
	return {'Iris-setosa':0, 'Iris-versicolor':0, 'Iris-virginica':0}


def verify_uniqueness(flowers_set, tuples):
	tuples_lenght = len(tuples)

	for tuple in tuples:
		flowers_set[tuple[-1]] += 1

	for flower in flowers_set:
		if (flowers_set[flower] == tuples_lenght):
			return True, flower

	return False, -1


def count_tuples(flowers_set, tuples):
	for tuple in tuples:
		flowers_set[tuple[-1]] += 1

	max = -1
	selected_flower = -1
	for flower in flowers_set:
		if (max < flowers_set[flower]):
			max = flowers_set[flower]
			selected_flower = flower

	return selected_flower


def filter(flowers, tuples, condition, branch, level):
	new_tuples = []
	if (branch == 1):
		for tuple in tuples:
			if(tuple[level] < condition[level][branch]):
				new_tuples.append(tuple)
				flowers[tuple[-1]] += 1
	else:
		for tuple in tuples:
			if(condition[level][branch - 1] <= tuple[level] and tuple[level] < condition[level][branch]):
				new_tuples.append(tuple)
				flowers[tuple[-1]] += 1

	return new_tuples


def print_tree(indentation, tree):
	if (tree.is_leaf()):
		node_value = tree.get_value_or_label()
		if (node_value[0]):
			printable = indentation + 'True with ' + str(node_value[1]) + ' percent accurancy'
		else:
			printable = indentation + 'False with ' + str(node_value[1]) + ' percent accurancy'
	else:
		printable = indentation + tree.get_value_or_label()

	print(printable)
	indentation += pipe
	childs = tree.get_childs()
	if (childs != -1):
		for child in childs:
			print_tree(indentation, childs[child])


def ID3(level, tuples, selected_flower):
	if (level < max_level and tuples):
		is_unique_flower, flower = verify_uniqueness(create_flowers_set(), tuples)
		if (is_unique_flower):
			return Node(True, [selected_flower == flower, 100])
		else:
			node = Node(False, attributes[level][0])
			childs = {}
			for branch in range(1, 5):
				filtered_tuples = filter(create_flowers_set(), tuples, attributes, branch, level)
				childs[attributes[level][branch]] = ID3(level + 1, filtered_tuples, selected_flower)
			node.set_childs(childs)
			return node
	else:
		if (tuples):
			pdb.set_trace()
			#percent = 
			return Node(True, [selected_flower == count_tuples(create_flowers_set(), tuples), 60])
		else:
			return Node(True, [selected_flower == count_tuples(create_flowers_set(), global_tuples), 60])

def get_percent_value(flower, tuples):
	total = 0
	for tuple in tuples:
		if (flower == tuple[-1]):
			total += 1
	return (int(total * (5 / 6) * 100)) 


def get_leaf_value(tree, tuple):
	if (tree.is_leaf()):
		return tree.get_value_or_label()[0]
	else:
		childs = tree.get_childs()
		for child in childs:
			if (tuple[0] < child):
				return get_leaf_value(childs[child], tuple[1:])


def init_ID3(Attributes, Global_Tuples, selected_flower):
	global attributes
	global global_tuples

	attributes = Attributes
	global_tuples = Global_Tuples
	tree = ID3(0, global_tuples, selected_flower)
	print_tree(pipe, tree)
	return tree
