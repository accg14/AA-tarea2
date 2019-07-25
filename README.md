# Decision tree & Evaluation
The main porpuse of this project is to build decision trees using ID3 algorithm, and evaluate them with some metrics (F1 for instance).
The scenario includes working with continuos attributes.
The data sets are:
- (the well know) [Iris dataset](https://archive.ics.uci.edu/ml/datasets/iris)
- [Covertype](https://archive.ics.uci.edu/ml/datasets/Covertype)
## Customization of the process
The numeric attributes where splitted in quantiles, so possible atypical values can not affect the performance of the classification task. Something that could happen if the ranges would have been made with the median.
Besides, the election of the attributes for each level of the tree through the computation of the gain were made once at the beggining, therefore there is a plenty save of time computing.

The normalization taken for qualitative attributes was one hot encoding, avoiding possible mistakes.

When the trees votes for classify an instance, the election could take these cases:
- If all trees votes the instance as negative, the classification is made within the minimum probability.
- If at least there is a positive vote, the classification is made within the maximum probability.
## Prerequisites
- numpy (1.16.3)
- python (3.7.2)
- colorama
## Usage
```python
python main.py # A and B
python main.py tree_type #C | -1 for multiclass tree, any other value to generate 'uniclass' tree
```
## Conclusions (so far)
The classification with multiclass tress in the iris data set was quite succesfull (0.89 F1 metric). Additionally, the classification made with the forest has also succed but less than the previos one (there are a few assumptions of why this is happening).

The multiclass tree for the covertype data set reached an F1 metric of 0.59, which may be explained because the imbalance of the data set.

Future improvement are being  discussed by the team.

## Authors
- [@accg14](https://github.com/accg14)
- [@joaquirrem](https://github.com/joaguirrem)
- [@gonzanunezcano](https://github.com/gonzanunezcano)
## License 
[MIT](https://choosealicense.com/licenses/mit/)
