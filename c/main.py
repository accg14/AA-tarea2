import PreProcessing, Processing, PostProcessing

train_set_file = 'training_set.txt'
test_set_file = 'testing_set.txt'

iris_setosa = 'Iris-setosa'
iris_versicolor = 'Iris-versicolor'
iris_virginica = 'Iris-virginica'

if __name__== "__main__":
	attributes_order, attributes_label = PreProcessing.custom_main()
	train_tuples = PreProcessing.data_order(attributes_order, train_set_file)

	tree = Processing.init_ID3(attributes_label, train_tuples, '-1')

	test_tuples = PreProcessing.data_order(attributes_order, test_set_file)
	result = PostProcessing.verify_tree(tree, test_tuples, iris_setosa)
	
	print(str(result))
