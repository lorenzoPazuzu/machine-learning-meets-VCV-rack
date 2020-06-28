import json
import matplotlib
import mido
import math
import mido

#opening JSON file
f = open('data.json',)

#returns JSON object as dictionary
data = json.load(f)

#looks at the input file index in the list
file_position = data.get('filenames')

def find_index(name_of_the_file):
    for index, file_name in enumerate(file_position):
        if file_name == name_of_the_file:
            return index
        else:
            pass

##############################################################################

#input here the name of the file you are looking for
index_file = find_index('bird.wav')

##############################################################################

# MFCC DATA
x = data.get('pcamfcc')
x = x[index_file]
#pulls out the single element in the dictionary
for elem in x:
    myPoint = x.get(elem)

# compute the euclidean distance
dots_in_space = []

def complex_dict_to_list(type):
    dots_in_space = []
    y = data.get(type)
    # all the dots. They're dictionary containing each dot's position
    for index, elem in enumerate(y):
        coord_dict = y[index]
        #loop to pull out the unique element of the dictionary
        for coordinate in coord_dict:
            #list with actual coordinates of the points
            coord = coord_dict.get(coordinate)
            dots_in_space.append(coord)
    return dots_in_space


def euclidean_distance(coord1_list, coord2_list):
    result = (coord1_list[0] - coord2_list[0])**2 + (coord1_list[1] - coord2_list[1])**2
    result = math.sqrt(result)
    return result

def closest_neighbors(type):
    # big number
    closest_point = math.inf;
    val = 0
    # takes index and coord of the wanted point
    wanted_file_index = find_index('bird.wav')  ######################################## change here!
    wanted_coordinates = complex_dict_to_list(type)
    wanted_coordinates = wanted_coordinates[wanted_file_index]
    #print(wanted_file_index)
    #print(wanted_coordinates)
    for index, elem in enumerate(complex_dict_to_list(type)):
        if index == wanted_file_index:
            pass
        else:
            val = euclidean_distance(wanted_coordinates, elem)
            # resolve this: it can't be the same point, but the check shouldnt be twice
            if val < closest_point and val != 0:
                closest_point = val
                i = index
                element = elem

    return i

def soundindex_patch_converter(name):
    name = name.replace('patch', '')
    name = name.replace('.wav', '')
    offset = int(name) // 2
    return int(name)

#opening JSON file
g = open('sent_cc.json',)

#returns JSON object as dictionary
controls = json.load(g)


# here transforms the dictionary into an ordered list
control_list = []
for key, value in controls.items():
    temp = [key, value]
    control_list.append(temp)




print('the closest patch for PCA with MFCC is ', file_position[closest_neighbors('pcamfcc')])

print('the closest patch for PCA with WAVENET is ', file_position[closest_neighbors('pcawavenet')])

print('the closest patch for T-SNE with MFCC is (00) ', file_position[closest_neighbors('tsnemfcc00')])

print('the closest patch for T-SNE with MFCC is (01) ', file_position[closest_neighbors('tsnemfcc01')])

print('the closest patch for T-SNE with MFCC is (02) ', file_position[closest_neighbors('tsnemfcc02')])

print('the closest patch for T-SNE with MFCC is (03) ', file_position[closest_neighbors('tsnemfcc03')])

print('the closest patch for T-SNE with MFCC is (10) ', file_position[closest_neighbors('tsnemfcc10')])

print('the closest patch for T-SNE with MFCC is (11) ', file_position[closest_neighbors('tsnemfcc11')])

print('the closest patch for T-SNE with MFCC is (12) ', file_position[closest_neighbors('tsnemfcc12')])

print('the closest patch for T-SNE with MFCC is (13) ', file_position[closest_neighbors('tsnemfcc13')])

print('the closest patch for T-SNE with MFCC is (20) ', file_position[closest_neighbors('tsnemfcc20')])

print('the closest patch for T-SNE with MFCC is (21) ', file_position[closest_neighbors('tsnemfcc21')])

print('the closest patch for T-SNE with MFCC is (22) ', file_position[closest_neighbors('tsnemfcc22')])

print('the closest patch for T-SNE with MFCC is (23) ', file_position[closest_neighbors('tsnemfcc23')])

print('the closest patch for T-SNE with MFCC is (30) ', file_position[closest_neighbors('tsnemfcc30')])

print('the closest patch for T-SNE with MFCC is (31) ', file_position[closest_neighbors('tsnemfcc31')])

print('the closest patch for T-SNE with MFCC is (32) ', file_position[closest_neighbors('tsnemfcc32')])

print('the closest patch for T-SNE with MFCC is (33) ', file_position[closest_neighbors('tsnemfcc33')])




print('the closest patch for T-SNE with MFCC is (20) ', file_position[closest_neighbors('tsnemfcc20')])

print('the closest patch for T-SNE with MFCC is (30) ', file_position[closest_neighbors('tsnemfcc30')])



f.close()