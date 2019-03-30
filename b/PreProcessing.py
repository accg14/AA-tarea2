import numpy, pdb, random, os

attributes_id = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
target_class = ''

def entropy(entry_values):
    #pdb.set_trace()
    sample_size = len(entry_values)
    if sample_size == 0:
        return sample_size

    total_samples = sum(entry_values)
    pi = list(map(lambda x: x/total_samples, entry_values))
    ent = 0
    for p_i in pi:
        if p_i > 0:
            ent += (-p_i)*numpy.log2(p_i)
    if ent > 1:
        return 1
    else:
        return ent

def gain(set_entropy, dic, index):
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

    print("Q1 entropy for attribute " + str(index) + ": " + str(q1_entropy) )
    print("Q2 entropy for attribute " + str(index) + ": " + str(q2_entropy) )
    print("Q3 entropy for attribute " + str(index) + ": " + str(q3_entropy) )
    print("Q4 entropy for attribute " + str(index) + ": " + str(q4_entropy) )
    print()

    total_gain = set_entropy - ((q1_size*q1_entropy)+(q2_size*q2_entropy)+(q3_size*q3_entropy)+(q4_size*q4_entropy))/120
    return total_gain

def divide_data(sorted_attributes, file_name):
    main_return = []
    quantils_array = []
    for i in range(0,len(sorted_attributes)):
        q1 = numpy.quantile(sorted_attributes[i], 0.25)
        q2 = numpy.quantile(sorted_attributes[i], 0.5)
        q3 = numpy.quantile(sorted_attributes[i], 0.75)
        q4 = numpy.quantile(sorted_attributes[i], 1.0)

        quantils_array.append([attributes_id[i], q1, q2, q3, q4])

        first_quarter = []
        second_quarter = []
        third_quarter = []
        fourth_quarter = []

        for j in range(0,len(sorted_attributes[i])):
            if (sorted_attributes[i][j] < q1):
                first_quarter.append(sorted_attributes[i][j])
            elif(sorted_attributes[i][j] < q2):
                second_quarter.append(sorted_attributes[i][j])
            elif(sorted_attributes[i][j] < q3):
                third_quarter.append(sorted_attributes[i][j])
            else:
                fourth_quarter.append(sorted_attributes[i][j])

        first_flowers = [0,0]
        second_flowers = [0,0]
        third_flowers = [0,0]
        fourth_flowers = [0,0]

        f = open(file_name, 'r')
        for line in f:
            values = line.split(',')
            values[len(values)-1] = values[len(values)-1].replace('\n','')

            if (float(values[i]) < q1):
                if (values[4] == target_class):
                    first_flowers[0] += 1
                else:
                    first_flowers[1] += 1
            elif(float(values[i]) < q2):
                if (values[4] == target_class):
                    second_flowers[0] += 1
                else:
                    second_flowers[1] += 1
            elif(float(values[i]) < q3):
                if (values[4] == target_class):
                    third_flowers[0] += 1
                else:
                    third_flowers[1] += 1
            else:
                if (values[4] == target_class):
                    fourth_flowers[0] += 1
                else:
                    fourth_flowers[1] += 1

        dic = {
            'q1' : [first_quarter, first_flowers],
            'q2' : [second_quarter, second_flowers],
            'q3' : [third_quarter, third_flowers],
            'q4' : [fourth_quarter, fourth_flowers]
        }

        main_return.append(dic)
    return main_return, quantils_array

def trainning_samples(a,b):
    samples_id = []
    while len(samples_id) < 40:
        x = random.randint(a,b)
        if not x in samples_id:
                samples_id.append(x)

    return samples_id

def custom_main(class_id):
    global target_class
    target_class = class_id

    
    if not (os.path.isfile('train_set.txt')):
        f = open('data_set.txt', 'r')
        train_samples = trainning_samples(1, 50)
        train_samples += trainning_samples(51, 100)
        train_samples += trainning_samples(101,150)

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

    

    p_i = [0,0]
    each_column = [[],[],[],[]]

    train_f = open('train_set.txt', 'r')

    for line in train_f:
        values = line.split(',')
        values[len(values)-1] = values[len(values)-1].replace('\n','')
        #pdb.set_trace()
        if (values[4] == target_class):
            p_i[0] += 1
        else:
            p_i[1] += 1
        for i in range(0,4):
            each_column[i].append(float(values[i]))

    sorted_data = [[],[],[],[]]
    for i in range(0,4):
        sorted_data[i] = sorted(each_column[i])

    dic_quantiles, arr_quantiles = divide_data(sorted_data,'train_set.txt')
    set_entropy = entropy(p_i)
    print("Set_entropy: ", set_entropy)
    print()

    gains = []
    fst_attr_gain = gain (set_entropy, dic_quantiles, 0)
    gains.append(fst_attr_gain)
    snd_attr_gain = gain (set_entropy, dic_quantiles, 1)
    gains.append(snd_attr_gain)
    thr_attr_gain = gain (set_entropy, dic_quantiles, 2)
    gains.append(thr_attr_gain)
    fth_attr_gain = gain (set_entropy, dic_quantiles, 3)
    gains.append(fth_attr_gain)
    print("Gains: ", gains)
    print()

    final_attr_ordered = []
    final_quantil_ordered = []
    for i in gains:
        final_quantil_ordered.append(arr_quantiles[gains.index(max(gains))])
        final_attr_ordered.append(gains.index(max(gains)))
        gains[gains.index(max(gains))] = -1

    return final_attr_ordered, final_quantil_ordered

def data_order(attributes_order, file_name):
    file = open(file_name, 'r')
    ordered_data = []
    for line in file:
        split_line = line.split(',')
        split_line[-1] = split_line[-1].replace('\n', '')
        ordered_line = []
        for index in attributes_order:
            ordered_line.append(float(split_line[index]))
        ordered_line.append(split_line[-1])
        ordered_data.append(ordered_line)
    file.close()
    return ordered_data
