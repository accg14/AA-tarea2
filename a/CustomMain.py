import numpy









def entropy(entry_values):
    total = sum(entry_values)
    pi = list(map(lambda x: x/total),entry_values)
    for p_i in pi:
        ent += (-p_i)*numpy.log2(p_i)
    return ent

def profit(entropy):
    

if __name__== "__main__":

    f = open('data_set.txt', 'r')
    columns = len(f.readline().split(',')) - 1

    p_i = [0,0,0]
    for line in f:
        values = line.split(',')
        if (values[4] == 'Iris-setosa'):
            p_i[0] += 1
        elif (values[4] == 'Iris-versicolor')):
            p_i[1] += 1
        else:
            p_i[2] += 1
    set_entropy = entropy(p_i)




