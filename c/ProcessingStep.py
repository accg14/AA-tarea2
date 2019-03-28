import sys

attributes = []
global_tuples = []
min_level = 0
max_level = 0
empty = ''
pipe = '|'
binary = 'B'
continuous = 'C'

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


def create_forests_set():
	return {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0}


def verify_uniqueness(forests_set, tuples):
	tuples_lenght = len(tuples)

	for tuple in tuples:
		forests_set[tuple[-1]] += 1

	for forest in forests_set:
		if (forests_set[forest] == tuples_lenght):
			return True, forest

	return False, -1


def count_tuples(forests_set, tuples):
	for tuple in tuples:
		forests_set[tuple[-1]] += 1

	max = -1
	selected_forest = -1
	for forest in forests_set:
		if (max < forests_set[forest]):
			max = forests_set[forest]
			selected_forest = forest

	return selected_forest


def filter_continuous(forests, tuples, condition, branch, level):
	new_tuples = []
	if (branch == 2):
		for tuple in tuples:
			if(tuple[level] < condition[level][branch]):
				new_tuples.append(tuple)
				forests[tuple[-1]] += 1
	else:
		for tuple in tuples:
			if(condition[level][branch - 1] <= tuple[level] and tuple[level] < condition[level][branch]):
				new_tuples.append(tuple)
				forests[tuple[-1]] += 1

	return new_tuples


def filter_binary(forests, tuples, condition, branch, level):
	new_tuples = []
	for tuple in tuples:
		if(tuple[level] == condition[level][branch]):
			new_tuples.append(tuple)
			forests[tuple[-1]] += 1
	return new_tuples


def print_single_tree(level, indentation, tree):
	if (1 < level):
		new_indentation = empty
		for index in range(1, level):
			new_indentation += '║ '
		new_indentation += indentation[-2]
		new_indentation += indentation[-1]
		indentation = new_indentation

	printable = indentation + tree.get_value_or_label()
	print(printable)

	childs = tree.get_childs()
	if (childs != -1):
		index = 1
		for child in childs:
			if (index == len(childs)):
				print_single_tree(level + 1, indentation + '╚═', childs[child])
			else:
				print_single_tree(level + 1, indentation + '╠═', childs[child])
			index += 1


def print_multiple_tree(level, indentation, tree):
	if (1 < level):
		new_indentation = empty
		for index in range(1, level):
			new_indentation += '║ '
		new_indentation += indentation[-2]
		new_indentation += indentation[-1]
		indentation = new_indentation

	if (tree.is_leaf()):
		node_value = tree.get_value_or_label()
		if (node_value[0]):
			printable = indentation + 'True -> ' + str(node_value[1]) + '%'
		else:
			printable = indentation + 'False -> ' + str(node_value[1]) + '%'
	else:
		printable = indentation + tree.get_value_or_label()

	print(printable)

	childs = tree.get_childs()
	if (childs != -1):
		index = 1
		for child in childs:
			if (index == len(childs)):
				print_multiple_tree(level + 1, indentation + '╚═', childs[child])
			else:
				print_multiple_tree(level + 1, indentation + '╠═', childs[child])
			index += 1


def ID3_single(level, tuples):
	if (level < max_level and tuples):
		is_unique_forest, forest = verify_uniqueness(create_forests_set(), tuples)
		if (is_unique_forest):
			return Node(True, forest)
		else:
			node = Node(False, attributes[level][0])
			childs = {}

			if (attributes[level][1] == binary):
				for branch in range(2, 4):
					filtered_tuples = filter_binary(create_forests_set(), tuples, attributes, branch, level)
					childs[attributes[level][branch]] = ID3_single(level + 1, filtered_tuples)
			elif (attributes[level][1] == continuous):
				for branch in range(2, 6):
					filtered_tuples = filter_continuous(create_forests_set(), tuples, attributes, branch, level)
					childs[attributes[level][branch]] = ID3_single(level + 1, filtered_tuples)

			node.set_childs(childs)
			return node
	else:
		if (tuples):
			return Node(True, count_tuples(create_forests_set(), tuples))
		else:
			return Node(True, count_tuples(create_forests_set(), global_tuples))


def ID3_multiple(level, tuples, selected_forest):
	if (level < max_level and tuples):
		is_unique_forest, forest = verify_uniqueness(create_forests_set(), tuples)
		if (is_unique_forest):
			return Node(True, [selected_forest == forest, 100.0])
		else:
			node = Node(False, attributes[level][0])
			childs = {}

			if (attributes[level][1] == binary):
				for branch in range(2, 4):
					filtered_tuples = filter_binary(create_forests_set(), tuples, attributes, branch, level)
					childs[attributes[level][branch]] = ID3_multiple(level + 1, filtered_tuples, selected_forest)
			elif (attributes[level][1] == continuous):
				for branch in range(2, 6):
					filtered_tuples = filter_continuous(create_forests_set(), tuples, attributes, branch, level)
					childs[attributes[level][branch]] = ID3_multiple(level + 1, filtered_tuples, selected_forest)

			node.set_childs(childs)
			return node
	else:
		if (tuples):
			boolean_selected_forest = selected_forest == count_tuples(create_forests_set(), tuples)
			return Node(True, [boolean_selected_forest, get_percent_value(selected_forest, tuples, boolean_selected_forest)])
		else:
			boolean_selected_forest = selected_forest == count_tuples(create_forests_set(), global_tuples)
			return Node(True, [boolean_selected_forest, get_percent_value(selected_forest, global_tuples, boolean_selected_forest)])


def get_percent_value(forest, tuples, is_selected_forest):
	total = 0
	if (is_selected_forest):
		for tuple in tuples:
			if (forest == tuple[-1]):
				total += 1
	else:
		for tuple in tuples:
			if not (forest == tuple[-1]):
				total += 1
	return round(total * 100 / len(tuples), 1)


def get_leaf_value(tree, tuple):
	if (tree.is_leaf()):
		return tree.get_value_or_label()[0]
	else:
		childs = tree.get_childs()
		for child in childs:
			if (tuple[0] < child):
				return get_leaf_value(childs[child], tuple[1:])


def init_ID3_single(Attributes, Global_Tuples):
	global attributes
	global global_tuples
	global max_level

	attributes = Attributes
	global_tuples = Global_Tuples
	max_level = len(Attributes)
	tree = ID3_single(0, global_tuples)
	print_single_tree(0, empty, tree)
	return tree


def init_ID3_multiple(Attributes, Global_Tuples, selected_forest):
	global attributes
	global global_tuples
	global max_level

	attributes = Attributes
	global_tuples = Global_Tuples
	max_level = len(Attributes)
	tree = ID3_multiple(0, global_tuples, selected_forest)
	print_multiple_tree(0, empty, tree)
	return tree


if __name__== "__main__":
	attributes = [['A', 'B', 0, 1],['B', 'C', 0.25, 0.5, 0.75, 1.0],['C', 'B', 0, 1],['D', 'C', 0.25, 0.50, 0.75, 1.0]]
	global_tuples = [[0, 0.5, 0.75, 1, '1'],[0, 0.5, 0.75, 1, '2'],[1, 0.5, 0.75, 1, '2']]

	tree = init_ID3_multiple(attributes, global_tuples, '1')
	print(tree)