import sys

min_level = 0
max_level = 4

pipe = '|'


#TEMPORAL
choices = [['A', 0.25, 0.5, 0.75, 1], ['B', 0.25, 0.5, 0.75, 1], ['C', 0.25, 0.5, 0.75, 1], ['D', 0.25, 0.5, 0.75, 1]]
global_tuples = [[0.1,0.5,0.1,0.1,'Iris-setosa'],[0.1,0.1,0.4,0.1,'Iris-versicolor'],[0.1,0.1,0.4,0.1,'Iris-versicolor'],[0.1,0.8,0.4,0.5,'Iris-versicolor'],[0.4,0.5,0.4,0.1,'Iris-versicolor'],[0.4,0.1,0.1,0.1,'Iris-setosa'],[0.6,0.5,0.1,0.5,'Iris-setosa']]
#TEMPORAL


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


class Node:
	def __init__(self, is_leaf, label):
		self.is_leaf = is_leaf
		self.label = label


	def get_label(self):
		return self.label


	def is_leaf(self):
		return self.is_leaf


	def get_childs(self):
		if not (self.is_leaf):
			return self.childs
		else:
			return -1


	def set_childs(self, childs):
		self.childs = childs


def ID3(level, tuples):
	if (level < max_level and tuples):
		is_unique_flower, flower = verify_uniqueness(create_flowers_set(), tuples)
		if (is_unique_flower):
			return Node(True, flower)
		else:
			node = Node(False, choices[level][0])
			childs = {}
			for branch in range(1, 5):
				filtered_tuples = filter(create_flowers_set(), tuples, choices, branch, level)
				childs[choices[level][branch]] = ID3(level + 1, filtered_tuples)
			node.set_childs(childs)
			return node
	else:
		if (tuples):
			return Node(True, count_tuples(create_flowers_set(), tuples))
		else:
			return Node(True, count_tuples(create_flowers_set(), global_tuples))


def print_tree(indentation, tree):
	printable = indentation + tree.get_label()
	print(printable)
	indentation += pipe
	childs = tree.get_childs()
	if (childs != -1):
		for child in childs:
			print_tree(indentation, childs[child])


if __name__== "__main__":
	tree = ID3(0, global_tuples)
	print_tree(pipe, tree)
