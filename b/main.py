import ID3Algorithm
import PreProcessingStep

train_set_file = 'train_set.txt'
test_set_file = 'test_set.txt'

iris_setosa = 'Iris-setosa'
iris_versicolor = 'Iris-versicolor'
iris_virginica = 'Iris-virginica'

if __name__== "__main__":
	attributes_order, quantiles = PreProcessingStep.custom_main()
	train_tuples = PreProcessingStep.data_order(attributes_order, train_set_file)

	iris_setosa_tree = ID3Algorithm.init_ID3(quantiles, train_tuples, iris_setosa)
	iris_versicolor_tree = ID3Algorithm.init_ID3(quantiles, train_tuples, iris_versicolor)
	iris_virginica_tree = ID3Algorithm.init_ID3(quantiles, train_tuples, iris_virginica)

	test_tuples = PreProcessingStep.data_order(attributes_order, test_set_file)
	iris_setosa_result = ID3Algorithm.verify_tree(iris_setosa_tree, test_tuples, iris_setosa)
	iris_versicolor_result = ID3Algorithm.verify_tree(iris_versicolor_tree, test_tuples, iris_versicolor)
	iris_virginica_result = ID3Algorithm.verify_tree(iris_virginica_tree, test_tuples, iris_virginica)
	print('iris_setosa_result', str(iris_setosa_result))
	print('iris_versicolor_result', str(iris_versicolor_result))
	print('iris_virginica_result', str(iris_virginica_result))
