import ID3Algorithm
import PreProcessingStep

train_set_file = 'train_set.txt'
test_set_file = 'test_set.txt'

if __name__== "__main__":
	attributes_order, quantiles = PreProcessingStep.custom_main()
	train_tuples = PreProcessingStep.data_order(attributes_order, train_set_file)

	tree = ID3Algorithm.init_ID3(quantiles, train_tuples)

	test_tuples = PreProcessingStep.data_order(attributes_order, test_set_file)
	result = ID3Algorithm.verify_tree(tree, test_tuples)
	print(str(result))
