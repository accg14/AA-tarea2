{
    nodo: {
        label: string,
        quantiles: float[],
    }
}

q5 = [['sepal lenght in cm', 0.25, 0.5, 0.75, 1]]
elementos = [...]

class node:
    def __init__(self, level, elements):
        self.flowers = ['','','']
        if (level < 4):
            self.label = q5[level][0]
            self.childs = self.set_childs(level, elements)
        else:
            self.label = 

    def set_childs(self, level, elements):
        for i in range(1, 5):
            new_elements = filter(lambda x : x[i] < q5[level][i], elements.copy())

            flowers = {
                'Iris-setosa': 0,
                'Iris-versicolor': 0,
                'Iris-virginica': 0,
            }

            for e in new_elements:
                flowers[e[-1]] += 1

            new_elements_lenght = len(new_elements)

            for flower in flowers:
                if (flower == new_elements_lenght)
                    
            if alguna_flor==len(new_elements)
            self.child[q5[level][i]] = new Node(level + 1, new_elements)

    def filter()

