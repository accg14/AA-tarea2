import pdb
import ProcessingStep

def verify_tree(tree, tuples, selected_flower):
	#[True, False, Should be True, Should be False]
	result = [0, 0, 0, 0]
	for tuple in tuples:
		leaf_value = ProcessingStep.get_leaf_value(tree, tuple)
		if (leaf_value):
			if (selected_flower == tuple[-1]):
				result[0] += 1
			else:
				result[2] += 1
		else:
			if not (selected_flower == tuple[-1]):
				result[1] += 1
			else:
				result[3] += 1
	return result

def classify(tree, tuple):
	if (tree.is_leaf()):
		#pdb.set_trace()
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
		#pdb.set_trace()
		if (tree_result[0]):
			positive_results.append([tree[0], tree_result[1]])
		else:
			negative_results.append([tree[0], tree_result[1]])
	#pdb.set_trace()
	if positive_results:
		pdb.set_trace()
		j = 0
		for i in range(0,len(positive_results)):
		#	pdb.set_trace()
			if (positive_results[i][1] > positive_results[j][1]):
				j = i
		return (positive_results[j][0])
	else:
		pdb.set_trace()
		j = 0
		for i in range(0,len(negative_results)):
			if (negative_results[i][1] < negative_results[j][1]):
				j = i
		return (negative_results[j][0])

def measure_tree_cluster(trees, tuples):
	result = [0,0]
	for tuple in tuples:
		#pdb.set_trace()
		#print(tuple[-1])
		#g = get_consensus(trees,tuple)
		#print("resultado de la funcion: ")
		#print(g)
		if (tuple[-1] == get_consensus(trees,tuple)):
			result[0] += 1
		else:
			result[1] += 1
	return result