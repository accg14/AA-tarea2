import Processing

def verify_single_tree(tree, tuples):
	# [Correct values, Incorrect values]
	result = [0, 0]
	for tuple in tuples:
		leaf_value = Processing.get_leaf_value(tree, tuple)
		if (leaf_value == tuple[-1]):
			result[0] += 1
		else:
			result[1] += 1
	return result

def verify_multiple_tree(tree, tuples, selected_forest):
	#[True, False, Should be True, Should be False]
	result = [0, 0, 0, 0]
	for tuple in tuples:
		leaf_value = Processing.get_leaf_value(tree, tuple)
		if (leaf_value):
			if (selected_forest == tuple[-1]):
				result[0] += 1
			else:
				result[2] += 1
		else:
			if not (selected_forest == tuple[-1]):
				result[1] += 1
			else:
				result[3] += 1
	return result

def classify(tree, tuple):
	if (tree.is_leaf()):
		if (tree.get_value_or_label()[0]):
			return [1, tree.get_value_or_label()[1]]
		else:
			return [0, tree.get_value_or_label()[1]]
	else:
		childs = tree.get_childs()
		for child in childs:
			if (tuple[0] < child):
				return classify(childs[child], tuple[1:])

def get_consensus(trees, tuple):
	negative_results = []
	positive_results = []
	for tree in trees:
		tree_result = classify(tree[1], tuple)
		if (tree_result[0]):
			positive_results.append([tree[0], tree_result[1]])
		else:
			negative_results.append([tree[0], tree_result[1]])
	if positive_results:
		j = 0
		for i in range(0,len(positive_results)):
			if (positive_results[i][1] > positive_results[j][1]):
				j = i
		return (positive_results[j][0])
	else:
		j = 0
		for i in range(0,len(negative_results)):
			if (negative_results[i][1] < negative_results[j][1]):
				j = i
		return (negative_results[j][0])

def measure_tree_cluster(trees, tuples):
	result = [0,0]
	for tuple in tuples:
		if (tuple[-1] == get_consensus(trees,tuple)):
			result[0] += 1
		else:
			result[1] += 1
	return result