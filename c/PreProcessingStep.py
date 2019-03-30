import numpy, pdb, random, os, threading, asyncio
from operator import itemgetter

cont_attributes_id = ['elevation', 'aspect', 'slope', 'horizontal_distance_hydrology', 'vertical_distance_hydrology', 'horizontal_dist_roadways', 'hillshade_9am','hillshade_noon' , 'hillshade_3pm', 'horizontal_dist_f_points']
wa_id = ['wa_0', 'wa_1', 'wa_2', 'wa_3']
st_id_first = ['st_0', 'st_1', 'st_2', 'st_3', 'st_4', 'st_5', 'st_6', 'st_7', 'st_8', 'st_9', 'st_10']
st_id_second = ['st_11', 'st_12', 'st_13', 'st_14', 'st_15', 'st_16', 'st_17', 'st_18', 'st_19', 'st_20', 'st_21']
st_id_third = ['st_22', 'st_23', 'st_24', 'st_25', 'st_26', 'st_27', 'st_28', 'st_29', 'st_30', 'st_31', 'st_32']
st_id_fourth = ['st_33', 'st_34', 'st_35', 'st_36', 'st_37', 'st_38', 'st_39', 'st_40', 'st_41', 'st_42', 'st_43']

disc_attribute_id = wa_id + st_id_first + st_id_second + st_id_third + st_id_fourth

train_set_size = 464810
offset = 10
mutex = asyncio.Semaphore()
arr_binary = []

def get_column_attr(attr_name):
    attr_code = attr_name.split('_')
    if (attr_code[0] == 'wa'):
        return (int(attr_code[1]) + 10)
    else:
        return (int(attr_code[1]) + 14)

def entropy(entry_values):
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

def gain(set_entropy, dic, index, type_attr):
    if type_attr == 'continue':
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

        #print("q1 entropy for " + str(index) + " attribute: " + str(q1_entropy) )
        #print("q2 entropy for " + str(index) + " attribute: " + str(q2_entropy) )
        #print("q3 entropy for " + str(index) + " attribute: " + str(q3_entropy) )
        #print("q4 entropy for " + str(index) + " attribute: " + str(q4_entropy) )

        total_gain = set_entropy - ((q1_size*q1_entropy)+(q2_size*q2_entropy)+(q3_size*q3_entropy)+(q4_size*q4_entropy))/train_set_size
        return total_gain
    else:
        k = index
        #pdb.set_trace()
        zero_size = sum(dic.get(k).get('0'))
        zero_entropy = entropy(dic.get(k).get('0'))

        one_size = sum(dic.get(k).get('1'))
        one_entropy = entropy(dic.get(k).get('1'))

        total_gain = set_entropy - ((one_size*one_entropy)+(zero_size*zero_entropy))/train_set_size
        return total_gain

def divide_binary_data(attribute, loaded_file, attr_tag):
    zero_forest = [0, 0, 0, 0, 0, 0, 0]
    one_forest = [0, 0, 0, 0, 0, 0, 0]
    
    j = 0
    for tuple in loaded_file:
        tuple[-1] = tuple[-1].replace('\n','')
        #tuple = tuple[offset:]

        forest_class = int(tuple[-1]) - 1
        
        if (int(attribute[j]) == 0):
            zero_forest[forest_class] += 1
        else:
            one_forest[forest_class] += 1  
        j += 1

    binary_dic = {
        '0' : zero_forest,
        '1' : one_forest
    }
    tagged_dic = {
        attr_tag : binary_dic
    }
    mutex.acquire()
    arr_binary.append(tagged_dic)
    mutex.release()

def divide_continue_data(sorted_attributes, file_name):
    main_return = []
    quantils_array = []

    for i in range(0, len(sorted_attributes)):
        q1 = numpy.quantile(sorted_attributes[i], 0.25)
        q2 = numpy.quantile(sorted_attributes[i], 0.5)
        q3 = numpy.quantile(sorted_attributes[i], 0.75)
        q4 = numpy.quantile(sorted_attributes[i], 1.0)

        quantils_array.append([cont_attributes_id[i], q1, q2, q3, q4])

        first_quarter = []
        second_quarter = []
        third_quarter = []
        fourth_quarter = []

        for j in range(0,len(sorted_attributes[i])):
            #print(sorted_attributes[i][j])
            if (int(sorted_attributes[i][j]) < q1):
                first_quarter.append(sorted_attributes[i][j])
            elif(int(sorted_attributes[i][j]) < q2):
                second_quarter.append(sorted_attributes[i][j])
            elif(int(sorted_attributes[i][j]) < q3):
                third_quarter.append(sorted_attributes[i][j])
            else:
                fourth_quarter.append(sorted_attributes[i][j])

        first_forest = [0, 0, 0, 0, 0, 0, 0]
        second_forest = [0, 0, 0, 0, 0, 0, 0]
        third_forest = [0, 0, 0, 0, 0, 0, 0]
        fourth_forest = [0, 0, 0, 0, 0, 0, 0]

        f = open(file_name, 'r')
        for line in f:
            values = line.split(',')
            values[len(values)-1] = values[len(values)-1].replace('\n','')

            if (float(values[i]) < q1):
                first_forest[int(values[-1]) -1] += 1
            elif(float(values[i]) < q2):
                second_forest[int(values[-1]) - 1] += 1
            elif(float(values[i]) < q3):
                third_forest[int(values[-1]) - 1] += 1
            else:
                #if (int(values[-1]) > 7):
                #pdb.set_trace()
                fourth_forest[int(values[-1]) - 1] += 1
        f.close()

        dic = {
            'q1' : [first_quarter, first_forest],
            'q2' : [second_quarter, second_forest],
            'q3' : [third_quarter, third_forest],
            'q4' : [fourth_quarter, fourth_forest]
        }

        main_return.append(dic)
    return main_return, quantils_array


def custom_main():
    p_i = [0, 0, 0, 0, 0, 0, 0]
    each_column = []

    for i in range(0,54):
        each_column.append([])

    train_f = open('training_set.txt', 'r')
    for line in train_f:
        values = line.split(',')
        values[-1] = values[-1].replace('\n','')
        p_i[int(values[-1])-1] += 1

        for i in range(0, len(values) - 1):
            each_column[i].append(int(values[i]))
    train_f.close()

    sorted_data = []
    for i in range(0,10):
        sorted_data.append(sorted(each_column[i]))
    sorted_data.extend(each_column[10:])
    print("data ordenada")

    set_entropy = entropy(p_i)
    print("entropia calculada")

    dic_quantiles, arr_quantiles = divide_continue_data(sorted_data[:10],'training_set.txt') #just quantitive attributes

    continue_gains = []
    for i in range(0,len(dic_quantiles)):
        continue_gains.append(gain(set_entropy, dic_quantiles, i, 'continue'))

    continue_attr_ordered = []
    continue_quantil_ordered = []
    for i in continue_gains:
        continue_quantil_ordered.append(arr_quantiles[continue_gains.index(max(continue_gains))])
        continue_attr_ordered.append([continue_gains.index(max(continue_gains)), max(continue_gains)])
        continue_gains[continue_gains.index(max(continue_gains))] = -1
    
    print('atributos continuos ok')

    loaded_file = []
    f = open('training_set.txt', 'r')
    for line in f:
        values = line.split(',')
        loaded_file.append(values)
    f.close()

    
    stop_values = [17, 25, 33, 41, 49]
    thread_pool = []
    global disc_attribute_id
    disc_attribute_id_cp = disc_attribute_id.copy()
    for i in range(10, len(sorted_data)):
        th = threading.Thread(target=divide_binary_data, args = (sorted_data[i], loaded_file, disc_attribute_id_cp[0]))
        disc_attribute_id_cp = disc_attribute_id_cp[1:]
        thread_pool.append(th)
        th.start()
        if (i in stop_values):
            for th in thread_pool:
                th.join()
                thread_pool = []
    for th in thread_pool:
        th.join()

    disc_gain = []
    for attribute in arr_binary:
        for k in attribute:
            disc_gain.append([get_column_attr(k),gain(set_entropy, attribute, k, 'discrete')])
    sorted_disc_gain = sorted(disc_gain, key = itemgetter(1), reverse = True)

    all_attr = sorted_disc_gain + continue_attr_ordered

    sorted_all_attr = sorted(all_attr, key = itemgetter(1), reverse = True)
    
    process_result = []
    
    tmp = []

    for attr in sorted_all_attr:
        tmp.append(attr[0])
        if (attr[0] < 10):
            attr_info = [continue_quantil_ordered[0][0], 'C']
            for i in range(1,5):
                attr_info.append(continue_quantil_ordered[0][i])
            continue_quantil_ordered = continue_quantil_ordered[1:]
        else:
            label = disc_attribute_id[attr[0] - offset]
            attr_info = [label, 'B', 0, 1]
        process_result.append(attr_info)

    pdb.set_trace()  


    
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
