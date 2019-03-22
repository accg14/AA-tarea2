import numpy, pdb, random

def entropy(entry_values):
    #pdb.set_trace()
    sample_size = len(entry_values)
    total = sum(entry_values)
    if sample_size == 0:
        return sample_size

    pi = list(map(lambda x: x/total, entry_values))
    #pdb.set_trace()
    ent = 0
    for p_i in pi:
        if p_i > 0:
            ent += (-p_i)*numpy.log2(p_i)
    if ent > 1:
        return 1
    else:
        return ent

def gain(set_entropy, dic, index):
    #pdb.set_trace()
    q1_values = dic[index].get('q1')[0]
    q1_size = len(q1_values)
    q1_entropy = entropy(dic[index].get('q1')[1])

    q2_values = dic[index].get('q2')[0]
    q2_size = len(q2_values)
    q2_entropy = entropy(dic[index].get('q2')[1])

    q3_values = dic[index].get('q3')[0]
    q3_size = len(q3_values)
    q3_entropy = entropy(dic[index].get('q3')[1])

    q4_values = dic[index].get('q4')[0]
    q4_size = len(q4_values)
    q4_entropy = entropy(dic[index].get('q4')[1])

    print("q1 entropy for " + str(index) + "attribute: " + str(q1_entropy) )
    print("q2 entropy for " + str(index) + "attribute: " + str(q2_entropy) )
    print("q3 entropy for " + str(index) + "attribute: " + str(q3_entropy) )
    print("q4 entropy for " + str(index) + "attribute: " + str(q4_entropy) )
    #pdb.set_trace()
    total_gain = set_entropy - ((q1_size*q1_entropy)+(q2_size*q2_entropy)+(q3_size*q3_entropy)+(q4_size*q4_entropy))/120
    return total_gain

def divide_data(sorted_attributes, file_name):
    main_return = []
    for i in range(0,len(sorted_attributes)):
        q1 = numpy.quantile(sorted_attributes[i], 0.25)
        q2 = numpy.quantile(sorted_attributes[i], 0.5)
        q3 = numpy.quantile(sorted_attributes[i], 0.75)

        first_quarter = []
        second_quarter = []
        third_quarter = []
        fourth_quarter = []

        #if i == 2:
        #pdb.set_trace()
        for j in range(0,len(sorted_attributes[i])):
            if (sorted_attributes[i][j] < q1):
                first_quarter.append(sorted_attributes[i][j])
            elif(sorted_attributes[i][j] < q2):
                second_quarter.append(sorted_attributes[i][j])
            elif(sorted_attributes[i][j] < q3):
                third_quarter.append(sorted_attributes[i][j])
            else:
                fourth_quarter.append(sorted_attributes[i][j])

        first_flowers = [0,0,0]
        second_flowers = [0,0,0]
        third_flowers = [0,0,0]
        fourth_flowers = [0,0,0]
        #pdb.set_trace()
        #print("BEFORE READ FILE")
        f = open(file_name, 'r')
        for line in f:
            #print("READ FILE")
            values = line.split(',')
            values[len(values)-1] = values[len(values)-1].replace('\n','')
            #pdb.set_trace()
            if (float(values[i]) < q1):
                if (values[4] == "Iris-setosa"):
                    first_flowers[0] += 1
                elif(values[4] == "Iris-versicolor"):
                    first_flowers[1] += 1
                else:
                    first_flowers[2] += 1
            elif(float(values[i]) < q2):
                if (values[4] == "Iris-setosa"):
                    second_flowers[0] += 1
                elif(values[4] == "Iris-versicolor"):
                    second_flowers[1] += 1
                else:
                    second_flowers[2] += 1
            elif(float(values[i]) < q3):
                if (values[4] == "Iris-setosa"):
                    third_flowers[0] += 1
                elif(values[4] == "Iris-versicolor"):
                    third_flowers[1] += 1
                else:
                    third_flowers[2] += 1
            else:
                if (values[4] == "Iris-setosa"):
                    fourth_flowers[0] += 1
                elif(values[4] == "Iris-versicolor"):
                    fourth_flowers[1] += 1
                else:
                    fourth_flowers[2] += 1


        dic = {
            'q1' : [first_quarter, first_flowers],
            'q2' : [second_quarter, second_flowers],
            'q3' : [third_quarter, third_flowers],
            'q4' : [fourth_quarter, fourth_flowers]
        }

        main_return.append(dic)
    return main_return

def trainning_samples(a,b):
    samples_id = []
    while len(samples_id) < 40:
        x = random.randint(a,b)
        if not x in samples_id:
                samples_id.append(x)
    #pdb.set_trace()
    return samples_id


if __name__== "__main__":
    train_samples = trainning_samples(1, 50)
    train_samples += trainning_samples(51, 100)
    train_samples += trainning_samples(101,150)

    f = open('data_set.txt', 'r')
    train_f = open('train_set.txt', 'a')
    test_f = open('test_set.txt', 'a')
    i  = 1
    for line in f:
        if i in train_samples:
            train_f.write(line)
        else:
            test_f.write(line)
        i += 1

    test_f.close()
    f.close()
    train_f.close()

    p_i = [0,0,0]
    each_column = [[],[],[],[]]

    train_f = open('train_set.txt', 'r')
    for line in train_f:
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
            each_column[i].append(float(values[i]))

    sorted_data = [[],[],[],[]]
    for i in range(0,4):
        sorted_data[i] = sorted(each_column[i])

    dic_quantiles = divide_data(sorted_data,'train_set.txt')
    set_entropy = entropy(p_i)
    print(set_entropy)

    gains = []
    fst_attr_gain = gain (set_entropy, dic_quantiles, 0)
    gains.append(fst_attr_gain)
    snd_attr_gain = gain (set_entropy, dic_quantiles, 1)
    gains.append(snd_attr_gain)
    thr_attr_gain = gain (set_entropy, dic_quantiles, 2)
    gains.append(thr_attr_gain)
    fth_attr_gain = gain (set_entropy, dic_quantiles, 3)
    gains.append(fth_attr_gain)
    print(gains)

    final_attr_order = []
    for i in gains:
        final_attr_order.append(gains.index(max(gains)))
        gains[gains.index(max(gains))] = -1
    print(final_attr_order)


