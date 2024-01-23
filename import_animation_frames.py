#google doc where i wrote all the offset and indexes: https://docs.google.com/document/d/1usQFBsIDIb3GYtrkZipqxZCao5WlkD5OW86M34yLkz8/edit?usp=sharing
import maya.cmds as cmds
import os
import csv
# ~constants~ 
#controller channel names

def delete_keyframes(p_controller: list)-> None:
    for each in p_controller:
        if cmds.selectKey(each) > 0:
            cmds.selectKey(each,add = True,keyframe = True)
            cmds.cutKey(animation = "keys", clear = True)

def set_key(cntroller,start_frame,data):
    frame = start_frame
    end_frame = start_frame + len(data[::100])-1
    animation_ranges = []
    for each in data[::100]:
        cmds.currentTime( frame )
        final_keyframes = [float(x.strip()) for x in each]
        for i in range(len(final_keyframes)):
            if i == len(final_keyframes) - 1: #for all the finger/toe controlls.
                for j in range(5):
                    cmds.setAttr(cntroller[i+j],final_keyframes[i])
                    cmds.setKeyframe(cntroller[i+j])
            else:
                cmds.setAttr(cntroller[i],  final_keyframes[i])
                cmds.setKeyframe(cntroller[i])
            # print(cntroller[i], "rotates ", final_keyframes[i], "degrees" )
        if frame == end_frame:
            for i in range(len(final_keyframes)):
                animation_ranges[i][1] = final_keyframes[i]
        elif frame == start_frame:
            for each in final_keyframes:
                animation_ranges.append([each,0])

 
        frame += 1
    print(animation_ranges)
    for each in cntroller[:len(cntroller) - 5]:
        #use linear interpolation where time is x and value is y
        if each == "Main.translateZ":
            continue
        else:
            value_0 = animation_ranges[cntroller.index(each)][1]
            value_f = animation_ranges[cntroller.index(each)][0]
            time_0 = 1
            time_f = 5 # number of frames to add minus 2
            for time_n in range(time_0+1,time_f+1): # this should produce three interpolated points
                    cmds.currentTime(end_frame+time_n - 1)
                    value_n = value_0 + ((value_f - value_0) / (time_f - time_0))*(time_n - time_0)
                    # print("time_n is: ", time_n, "value_n is: ", value_n)
                    cmds.setAttr(each, value_n)
                    cmds.setKeyframe(each)
                    cmds.setInfinity(each, postInfinite = "cycle")
                    cmds.setInfinity(each, preInfinite = "cycle")



def create_animation(hind_path, fore_path ,*args):
    hind_controller_names = [
        "IKSpine1_M.rotateX","IKSpine1_M.rotateZ", "IKSpine1_M.rotateY","Main.translateZ","Main.translateX"
        ,"Main.translateY","FKHip_R.rotateY","FKHip_R.rotateZ","FKHip_R.rotateX",
        "FKKnee_R.rotateZ","FKTwistLeg_R.rotateX","FKToes1_R.rotateX","FKBigToe1_R.rotateZ","FKIndexToe1_R.rotateZ"
        ,"FKMiddleToe1_R.rotateZ", "FKRingToe1_R.rotateZ", "FKPinkyToe1_R.rotateZ"
        ]
    fore_controller_names = [
        'IKSpine3_M.rotateX', 'IKSpine3_M.rotateZ', 'IKSpine3_M.rotateY', 'FKShoulder_R.rotateY', 'FKShoulder_R.rotateZ'
        , 'FKShoulder_R.rotateX', 'FKElbow_R.rotateZ', 'FKTwistArm_R.rotateX',
        'FKFingers1_R.rotateZ','FKThumbFinger1_R.rotateZ','FKIndexFinger1_R.rotateZ', 'FKMiddleFinger1_R.rotateZ',
        'FKRingFinger1_R.rotateZ', "FKPinkyFinger1_R.rotateZ"
        ]
    #delete existing keyframes:
    delete_keyframes(hind_controller_names)
    delete_keyframes(fore_controller_names)
    

    print("full path:", hind_path)
    directory,file_name1 = os.path.split(hind_path)
    print("full_path:", hind_path, "\nfile_name:", file_name1)#debugg
    
    os.chdir(directory)
    hind_data= []
    with open(file_name1) as csv_f:
        freader = csv.reader(csv_f,delimiter =',')
        flines = list(freader)
        for i in range(len(flines)): #these are the lines that have the actual values
            hind_data.append(flines[i])
    #forelimb
    file_name2 = os.path.basename(fore_path) 
    fore_data = []
    with open(file_name2) as csv_f:
        freader = csv.reader(csv_f,delimiter =',')
        flines = list(freader)
        for i in range(len(flines)): #these are the lines that have the actual values
            fore_data.append(flines[i])

    set_key(hind_controller_names,1,hind_data)
    set_key(fore_controller_names,22,fore_data)
    



