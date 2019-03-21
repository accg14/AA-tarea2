import numpy, pdb

def entropy(entry_values):
    total = sum(entry_values)
    pi = list(map(lambda x: x/total),entry_values)
    for p_i in pi:
        ent += (-p_i)*numpy.log2(p_i)
    return ent
 
if __name__== "__main__":
    f = open('data_set.txt', 'r')
    #columns = len(f.readline().split(',')) - 1
    
    p_i = [0,0,0]
    each_column = [[],[],[],[]]
    
    for line in f:
        values = line.split(',')
        values[len(values)-1] = values[len(values)-1].replace('\n','')
        #print(values)
        if (values[4] == 'Iris-setosa'):
            p_i[0] += 1
        elif (values[4] == 'Iris-versicolor'):
            p_i[1] += 1
        else:
            p_i[2] += 1
        for i in range(0,4):
            print(i)
            #print('before')
            #print(each_column[i])
            each_column[i].append(float(values[i]))
            #print('after: ')
            #print(each_column[i])

    sorted_data = [[],[],[],[]]
    for i in range(0,4):
        sorted_data[i] = sorted(each_column[i]) 
        print(sorted_data[i])
    set_entropy = entropy(p_i)




