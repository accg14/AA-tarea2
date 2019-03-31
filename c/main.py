import colorama, sys, time
import PreProcessing, Processing, PostProcessing

train_set_file = 'training_set.txt'
test_set_file = 'testing_set.txt'

color_start = '\033[33m'
color_end = '\033[0m'

#attributes_label = [['A', 'B', 0, 1],['B', 'C', 0.25, 0.5, 0.75, 1.0],['C', 'B', 0, 1],['D', 'C', 0.25, 0.50, 0.75, 1.0]]
#train_tuples = [[0, 0.5, 1, 0.75, '1'],[0, 0.5, 1, 0.75, '2'],[1, 0.5, 0, 0.5, '2']]
#test_tuples = [[0, 0.5, 1, 0.75, '1'],[0, 0.5, 1, 0.75, '2'],[1, 0.5, 0, 0.5, '2'],[0, 0.4, 1, 1.0, '1'],[0, 0.5, 0, 0.75, '1'],[0, 0.5, 1, 0.75, '2']]

if __name__== "__main__":
	colorama.init()
	start_time = time.time()

	attributes_order, attributes_label = PreProcessing.custom_main()
	train_tuples = PreProcessing.data_order(attributes_order, train_set_file)
	training_tuples_time = time.time()
	print(color_start, "\n > Training tuples calculated in:", str(round(training_tuples_time - start_time, 5)), "seconds\n", color_end)

	if (int(sys.argv[1]) == -1):
		tree = Processing.init_ID3(attributes_label, train_tuples, '-1')
		tree_time = time.time()
		print(color_start, "\n > Tree created in:", str(round(tree_time - training_tuples_time, 5)), "seconds\n", color_end)

		test_tuples = PreProcessing.data_order(attributes_order, test_set_file)
		result = PostProcessing.verify_single_tree(tree, test_tuples)
		verify_tree_time = time.time()

	else:
		tree = []
		tree_time = []
		for index in range(1, 8):
			tree.append(Processing.init_ID3(attributes_label, train_tuples, str(index)))
			tree_time.append(time.time())
			if (index == 1):
				print(color_start, "\n > Tree created in:", str(round(tree_time[index - 1] - training_tuples_time, 5)), "seconds\n", color_end)
			else:
				print(color_start, "\n > Tree created in:", str(round(tree_time[index - 1] - tree_time[index - 2], 5)), "seconds\n", color_end)

		test_tuples = PreProcessing.data_order(attributes_order, test_set_file)

		result = []
		verify_tree_time = []
		for index in range(1, 8):
			result.append(PostProcessing.verify_multiple_tree(tree[index - 1], test_tuples, str(index)))
			verify_tree_time.append(time.time())


	print(color_start, "-----", color_end)
	print(color_start, "> Training tuples calculated in\t|", str(round(training_tuples_time - start_time, 5)), "seconds", color_end)
	if (int(sys.argv[1]) == -1): 
		print(color_start, "> Tree created in\t\t\t|", str(round(tree_time - training_tuples_time, 5)), "seconds", color_end)
		print(color_start, "> Tree verified in\t\t\t|", str(round(verify_tree_time - tree_time, 5)), "seconds", color_end)
		print(color_start, "> Total time elapsed\t\t\t|", str(round(verify_tree_time - start_time, 5)), "seconds\n", color_end)
	else:
		for index in range(0, 7):
			if (index == 0):
				print(color_start, "> Tree", str(index + 1), "created in\t\t\t|", str(round(tree_time[index] - training_tuples_time, 5)), "seconds", color_end)
				print(color_start, "> Tree", str(index + 1), "verified in\t\t\t|", str(round(verify_tree_time[index] - tree_time[index], 5)), "seconds", color_end)
			else:
				print(color_start, "> Tree", str(index + 1), "created in\t\t\t|", str(round(tree_time[index] - tree_time[index - 1], 5)), "seconds", color_end)
				print(color_start, "> Tree", str(index + 1), "verified in\t\t\t|", str(round(verify_tree_time[index] - verify_tree_time[index - 1], 5)), "seconds", color_end)
		print(color_start, "> Total time elapsed\t\t\t|", str(round(verify_tree_time[6] - start_time, 5)), "seconds\n", color_end)

	print(str(result))
	colorama.deinit()
