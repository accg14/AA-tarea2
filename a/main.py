import ID3
import preProcessing

train_set_file = 'train_set.txt'
test_set_file = 'test_set.txt'

if __name__== "__main__":
	attributes_order, quantiles = preProcessing.custom_main()
	train_tuples = preProcessing.data_order(attributes_order, train_set_file)

	tree = ID3.init(quantiles, train_tuples)

	test_tuples = preProcessing.data_order(attributes_order, test_set_file)
	result = ID3.verify_tree(tree, test_tuples)
	print(str(result))
