import sys

MIN_LEVEL = 0
MAX_LEVEL = 4

choices = [['A', 0.25, 0.5, 0.75, 1], ['B', 0.25, 0.5, 0.75, 1], ['C', 0.25, 0.5, 0.75, 1], ['D', 0.25, 0.5, 0.75, 1]]
elements = [[0.1,0.5,0.1,0.1,'Iris-setosa'], [0.1,0.5,0.1,0.1,'Iris-setosa'], [0.1,0.5,0.1,0.1,'Iris-setosa'], [0.1,0.5,0.1,0.1,'Iris-setosa']]


def create_flowers_set():
	return {'Iris-setosa':0, 'Iris-versicolor':0, 'Iris-virginica':0}


def verify_uniqueness(flowers_set, tuples):
	tuples_lenght = len(tuples)

	for tuple in tuples:
		flowers_set[tuple[-1]] += 1

	for flower in flowers_set:
		if (flowers_set[flower] == tuples_lenght):
			return True, flower
	return False


def count_tuples(flowers_set, filtered_tuples):
	for tuple in tuples:
		flowers_set[tuple[-1]] += 1

	return max(flowers_set)


def filter(flowers, elements, condition, branch, level):
	new_elements = []
	if (branch == 1):
		for element in elements:
			if(element[level] < condition[level][branch]):
				new_elements.append(element)
				flowers[element[-1]] += 1
	else:
		for element in elements:
			if(element[level] < range(condition[level][branch - 1], condition[level][branch])):
				new_elements.append(element)
				flowers[element[-1]] += 1
	return new_elements


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


	def set_childs(self, childs):
		self.childs = childs


def ID3(level, tuples):
	if (level < MAX_LEVEL):
		unique, flower = is_unique_flower = verify_uniqueness(create_flowers_set(), tuples)

		if (unique):
			return Node(True, flower)
		else:
			node = Node(False, choices[level][0])
			childs = {}
			for branch in range(1, 4):
				filtered_tuples = self.filter(tuples, choices, branch, level)
				childs[choices[level][branch]] = ID3(level + 1, filtered_tuples)
			node.set_childs(childs)
			return node
	else:
		return Node(True, count_tuples(create_flowers_set(), tuples))


if __name__== "__main__":
	tree = ID3(0, elements)
	
