import ID3Algorithm
import PreProcessingStep

#TEMPORAL
attributes = [['A', 0.25, 0.5, 0.75, 1], ['B', 0.25, 0.5, 0.75, 1], ['C', 0.25, 0.5, 0.75, 1], ['D', 0.25, 0.5, 0.75, 1]]
global_tuples = [[0.1,0.5,0.1,0.1,'Iris-setosa'],[0.1,0.1,0.4,0.1,'Iris-versicolor'],[0.1,0.1,0.4,0.1,'Iris-versicolor'],[0.1,0.8,0.4,0.5,'Iris-versicolor'],[0.4,0.5,0.4,0.1,'Iris-versicolor'],[0.4,0.1,0.1,0.1,'Iris-setosa'],[0.6,0.5,0.1,0.5,'Iris-setosa']]
#TEMPORAL

if __name__== "__main__":
	tree = ID3Algorithm.init_ID3(attributes, global_tuples)
