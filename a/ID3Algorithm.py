import sys

choices = [['A', 0.25, 0.5, 0.75, 1], ['B', 0.25, 0.5, 0.75, 1], ['C', 0.25, 0.5, 0.75, 1], ['D', 0.25, 0.5, 0.75, 1]]
elements = [[0.1,0.5,0.1,0.1,'Iris-setosa'], [0.1,0.5,0.1,0.1,'Iris-setosa'], [0.1,0.5,0.1,0.1,'Iris-setosa'], [0.1,0.5,0.1,0.1,'Iris-setosa']]

class Node:
	def __init__(self, level, elements):
		if(level < 4):
			self.is_leaf = False
			self.label = choices[level][0]
			self.childs = {}
			self.set_childs(level, elements)
		else:
			self.is_leaf = True
			self.value = elements

	def create_flowers_set(self):
		return {'Iris-setosa':0, 'Iris-versicolor':0, 'Iris-virginica':0}

	def is_leaf(self):
		return self.is_leaf

	def get_value(self):
		if (self.is_leaf):
			return self.value

	def filter(self, flowers, elements, condition, level):
		new_elements = []
		for element in elements:
			if(element[level] < condition):
				new_elements.append(element)
				flowers[element[-1]] += 1
		return new_elements

	def get_childs(self):
		if not (self.is_leaf):
			return self.childs

	def set_childs(self, level, elements):
		for branch in range(1, 4):
			new_elements = elements.copy()
			flowers = self.create_flowers_set()

			new_elements = self.filter(flowers, new_elements, choices[level][branch], level)

			if(new_elements):
				new_elements_lenght = len(new_elements)
				flag = True
				for flower in flowers:
					if(flowers[flower] == new_elements_lenght):
						self.childs[choices[level][branch]] = Node(5, flower)
						flag = False
						break
				if (flag):
					self.childs[choices[level][branch]] = Node(level + 1, new_elements)
			else:
				self.childs[choices[level][branch]] = Node(5, 'Iris-setosa')

	def print_tree(self):
		if(self.is_leaf):
			print(str(self.value))
		else:
			for branch in self.childs:
				self.childs[branch].print_tree()

if __name__== "__main__":
	Test = Node(int(sys.argv[1]), elements)
	Test.print_tree()