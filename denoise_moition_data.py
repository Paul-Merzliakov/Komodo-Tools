#this takes the mot data, smooths it and then saves it into a csv file that can be read in maya and used to plug in all the numbers. this is because the maya scripting enviornemnt doesnt natively support mupy scipy ect.
import os
from scipy.signal import savgol_filter
import numpy


#offsets
#leg
HIPZ_OFFSET = 10
HIPX_OFFSET = 115
PELVISY_OFFSET = 165
KNEE_OFFSET = 85
ANKLE_OFFSET = 115
#arm
SHOULDERZ_OFFSET = 10
SHOULDERX_OFFSET = 115
ELBOW_OFFSET = 80
TWIST_OFFSET = 125
WRIST_OFFSET = 60
HAND_OFFSET = 20

def generate_csv(mot_file_path: str,csv_file_path: str,hind: bool,collum_endpoint: int):  
    f_dir, mot_file_name = os.path.split(mot_file_path)
    smoothed_dir,csv_file_name = os.path.split(csv_file_path)
    #print("f_dir is", f_dir)
    #print("mot_file_name_is", mot_file_name)
    
    os.chdir(f_dir)
    str_lines= []
    num_of_lines = 0
    if hind == True:
        start = 451
    else:
        start = 11
    with open(mot_file_name) as f:
        flines = f.readlines()
        num_of_lines += len(flines)
        for i in range(start,num_of_lines): #these are the str_lines that have the actual values
            str_lines.append(flines[i])
    array= []
    for each in str_lines:
        splitlines = []
        for val in each.split("\t"):
            splitlines.append(float(val.strip()))
        array.append(splitlines[1:collum_endpoint] + splitlines[14:21])
    print("length", len(array[0]))
    print(array[0] )
    if hind == True:
        for each in array:
        #pelvis pitch
            each[0] *= -.5
        #pelvis roll/ rotatez
            each[1] +=  10
        #pelvis yaw/pelvis y
            each[2] -= PELVISY_OFFSET
        # pelvis foward
            each[3] *= -100
        #pelvis side to side translate
            each[4] *= 100
        #hip extension/ flexion  (yrotation)
            each[6] = -(each[6]/1.1)
        #hip abduction, (zrotation)g
            each[7] += 10
        #hip lar, (xrotation) 
            each[8] = -(each[8]/1.)
        #knee flexion
            each[9] += KNEE_OFFSET
        #twist
            each[10]  = -each[10]
        #ankle controller
            each[11] += ANKLE_OFFSET +20
    else: #for forelimb
        for each in array:
     
        #chest Yaw/y 
            each[2] -= 170
        #shoulder_y 
            each[3] /= 2
        #shoulder_z
            each[4] = -each[4] - 20
        #shoulder_x
            each[5] = -each[5] - 15
        #elbowx
            each[6] = -each[6] - ELBOW_OFFSET
        #twist
            each[7] = -each[7] + TWIST_OFFSET
        #wrist
            each[8] = -each[8] - WRIST_OFFSET
        #knee flexion
            each[9] -= HAND_OFFSET

    csv_array = savgol_filter(array,555,3,axis = 0)#right leg joints are index 14 to 20
    # print(csv_array[0]) 
    # csv_array = numpy.array(array)
    os.chdir(smoothed_dir)
    numpy.savetxt(csv_file_name, csv_array,fmt = '%.3f',delimiter = ",")

#right leg
#generate_csv( "komodo06_run12_left_hind_IK.mot",True, (1,7), "Varius_right_hind_smoothed.csv" )
#generate_csv( "komodo06_run12_left_fore_IK_output rotmat_v2.mot",False, (1,4), "Varius_right_fore_smoothed.csv" )

