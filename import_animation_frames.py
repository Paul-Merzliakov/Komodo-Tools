#google doc where i wrote all the offset and indexes: https://docs.google.com/document/d/1usQFBsIDIb3GYtrkZipqxZCao5WlkD5OW86M34yLkz8/edit?usp=sharing
import maya.cmds as cmds
import constants
import process_denoise_file_data as denoise

def delete_existing_keyframes(anim_attributes: list)-> None:
    for attribute in anim_attributes:
        if cmds.selectKey(attribute) > 0:
            cmds.selectKey(attribute,add = True,keyframe = True)
            cmds.cutKey(animation = "keys", clear = True)

def linearly_interpolate_keys(anim_attributes : list, end_frame : int, animation_ranges: list) -> None:
    """
    uses linear interpolation where time is x and value is y
    """
    for attribute in anim_attributes[:len(anim_attributes) - 5]:
        if attribute == constants.DEFAULT_NON_LOOPING_ANIM_ATTR:
            continue
        else:
            value_0 = animation_ranges[anim_attributes.index(attribute)][1]
            value_f = animation_ranges[anim_attributes.index(attribute)][0]
            time_0 = 1
            time_f = 5 # number of frames to add minus 2
            for time_n in range(time_0+1,time_f+1): 
                    cmds.currentTime(end_frame+time_n - 1)
                    value_n = value_0 + ((value_f - value_0) / (time_f - time_0))*(time_n - time_0)
                    cmds.setAttr(attribute, value_n)
                    cmds.setKeyframe(attribute)
                    cmds.setInfinity(attribute, postInfinite = "cycle")
                    cmds.setInfinity(attribute, preInfinite = "cycle")


def set_anim_keys(anim_attributes: list,start_frame: int,anim_keys_raw_fpath: str) ->None:
    """
    takes in a start frame, list of anim_attributes, and the csv data you want to read from (as a list of strings)
    """
    delete_existing_keyframes(anim_attributes)
    anim_keys = denoise.get_anim_keys_from_csv(anim_keys_raw_fpath)

    frame = start_frame
    end_frame = start_frame + len(anim_keys)-1
    animation_ranges = []

    for row_of_keys in anim_keys:
        cmds.currentTime( frame )
        for anim_key_index in range(len(row_of_keys)):
            last_key_index = len(row_of_keys) - 1
            if anim_key_index is last_key_index:
                #this if case is for setting the toe/finger(digit) keys. since the anim data has only one key to use for all digit anim_attributes, we have to iterate set the value for each digit attribute attr
                #since the toes or fingers will always bee the last anim value in the data we process we can use that to check.
                for digit_controllr_i in range(5):
                    cmds.setAttr(anim_attributes[ anim_key_index + digit_controllr_i ] ,row_of_keys[anim_key_index])
                    cmds.setKeyframe(anim_attributes[ anim_key_index + digit_controllr_i])
            else:
                cmds.setAttr(anim_attributes[anim_key_index],  row_of_keys[anim_key_index])
                cmds.setKeyframe(anim_attributes[anim_key_index])
        #updating the animation ranges for use in linear interpolation function 
        if frame == end_frame:
            for i in range(len(row_of_keys)):
                animation_ranges[i][1] = row_of_keys[i]
        elif frame == start_frame:
            for row_of_keys in row_of_keys:
                animation_ranges.append([row_of_keys,0])
        frame += 1
    linearly_interpolate_keys(anim_attributes, end_frame, animation_ranges)




# def create_animation(hind_path: str, fore_path: str ,*args) -> None:
  

#     print("full path:", hind_path)
#     directory,file_name1 = os.path.split(hind_path)
#     print("full_path:", hind_path, "\nfile_name:", file_name1)#debugg
    
#     os.chdir(directory)
#     hind_data= []
#     with open(file_name1) as csv_f:
#         freader = csv.reader(csv_f,delimiter =',')
#         flines = list(freader)
#         for i in range(len(flines)): #these are the lines that have the actual values
#             hind_data.append(flines[i])
#     #forelimb
#     file_name2 = os.path.basename(fore_path) 
#     fore_data = []
#     with open(file_name2) as csv_f:
#         freader = csv.reader(csv_f,delimiter =',')
#         flines = list(freader)
#         for i in range(len(flines)): #these are the lines that have the actual values
#             fore_data.append(flines[i])

#     set_key(constants.DEFAULT_HIND_ANIM_ATTRS,1,hind_data)
#     set_key(constants.DEFAULT_FORE_ANIM_ATTRS,22,fore_data)
    



