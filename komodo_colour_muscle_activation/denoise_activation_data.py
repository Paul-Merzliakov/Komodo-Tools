#this takes the mot data, smooths it and then saves it into a csv file that can be read in maya and used to plug in all the numbers. this is because the maya scripting enviornemnt doesnt natively support mupy scipy ect.
import os
from scipy.signal import savgol_filter
import numpy

os.chdir(r"/Users/paulmerzliakov/Desktop/programming/dev/3D_stuff/Komodo_dragon_scripts/komodo_colour_muscle_activation")
rows= []
num_of_rows = 0
start = 10
with open("komodo6_run12_left_hind_StaticOptimization_activation.sto") as f:
    frows = f.readlines()
    num_of_rows += len(frows)
    for i in range(start,num_of_rows): 
        rows.append(frows[i])
array= []
for each in rows:
    splitrows = []
    for val in each.split("\t"):
        splitrows.append(float(val.strip()))
    splitrows_final = [splitrows[1],splitrows[3], splitrows[4], splitrows[6], splitrows[7], splitrows[9], splitrows[10],splitrows[11], splitrows[12], splitrows[14],splitrows[15],
                           splitrows[17],splitrows[18], splitrows[20],splitrows[21], splitrows[22]]#im so fucking done cant be fucked to find the smarter way to do this  - 30/7/23   
    
    array.append(splitrows_final)
    # array.append(splitrows)




csv_array = savgol_filter(array,100,3,axis = 0)
min = numpy.min(csv_array, axis = (0,1)) # outputs -0.000256453559363748

for i in range(len(csv_array)):
    for j in range(len(csv_array[i])):
       csv_array[i][j] +=  (0 - min)
#inverting the data make adjusting colour easier. 
max = numpy.max(csv_array, axis = (0,1))
print(max)
for i in range(len(csv_array)):
    for j in range(len(csv_array[i])):
        csv_array[i][j] = max - csv_array[i][j]
       
numpy.savetxt("smoothed_hind_muscle_activations.csv", csv_array,fmt = '%.8f',delimiter = ",")





