import PreProcessingStep, Processing, PostProcessingStep

train_set_file = 'train_set.txt'
test_set_file = 'test_set.txt'

iris_setosa = 'Iris-setosa'
iris_versicolor = 'Iris-versicolor'
iris_virginica = 'Iris-virginica'

if __name__== "__main__":
	attributes_order, quantiles = PreProcessingStep.custom_main(iris_setosa)
	train_tuples = PreProcessingStep.data_order(attributes_order, train_set_file)
	iris_setosa_tree = Processing.init_ID3(quantiles, train_tuples, iris_setosa)
	test_tuples = PreProcessingStep.data_order(attributes_order, test_set_file)
	iris_setosa_result = PostProcessingStep.verify_tree(iris_setosa_tree, test_tuples, iris_setosa)

	attributes_order, quantiles = PreProcessingStep.custom_main(iris_versicolor)
	train_tuples = PreProcessingStep.data_order(attributes_order, train_set_file)
	iris_versicolor_tree = Processing.init_ID3(quantiles, train_tuples, iris_versicolor)
	test_tuples = PreProcessingStep.data_order(attributes_order, test_set_file)
	iris_versicolor_result = PostProcessingStep.verify_tree(iris_versicolor_tree, test_tuples, iris_versicolor)

	attributes_order, quantiles = PreProcessingStep.custom_main(iris_virginica)
	train_tuples = PreProcessingStep.data_order(attributes_order, train_set_file)
	iris_virginica_tree = Processing.init_ID3(quantiles, train_tuples, iris_virginica)
	test_tuples = PreProcessingStep.data_order(attributes_order, test_set_file)
	iris_virginica_result = PostProcessingStep.verify_tree(iris_virginica_tree, test_tuples, iris_virginica)
	
	print('iris_setosa_result', str(iris_setosa_result))
	print('iris_versicolor_result', str(iris_versicolor_result))
	print('iris_virginica_result', str(iris_virginica_result))

	#forest = [['Iris-setosa',iris_setosa_tree],['Iris-versicolor',iris_versicolor_tree], ['Iris-virginica',iris_virginica_tree]]
	#cluster_work = PostProcessingStep.measure_tree_cluster(forest, test_tuples)
	#print(cluster_work)