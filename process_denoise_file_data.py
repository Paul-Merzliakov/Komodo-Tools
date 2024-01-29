# this takes the mot data, smooths it and then saves it into a csv file that can be read in maya and used to plug in all the numbers. this is because the maya scripting enviornemnt doesnt natively support mupy scipy ect.
import os
from scipy.signal import savgol_filter
import numpy
import csv
import constants as consts


# Hindlimb Offsets
# Forelimb Offsets

def get_anim_keys_from_csv(csv_fpath: str) ->list: 
    """
    this is used exclusively by import animation frames 
    it takes in a csv_file_path and returns that csv file's animation keys in the form of a 2 dimensional list of floats 
    """
    existing_csv_directory,existing_csv_name = os.path.split(csv_fpath)

    os.chdir(existing_csv_directory)
    raw_csv_data= []
    with open(existing_csv_name) as csv_f:
        freader = csv.reader(csv_f,delimiter =',')
        flines = list(freader)#these are the lines that have the actual values
        for line_i in range(len(flines)): 
            raw_csv_data.append(flines[line_i])
    anim_keys =[]
    for str_keys_row in raw_csv_data[::consts.DEFAULT_ANIM_DATA_STEP]:
        keys_row = [float(str_key.strip()) for str_key in str_keys_row]
        anim_keys.append(keys_row)
    return anim_keys    


class DenoiseFileData():
    def __init__(self):
        self.num_of_lines = 0
        self.animation_channels = []
        self.mot_fpath = ""
        self.csv_fpath = ""
        self.existing_csv_fpath = ""
        self.is_hind = True
        self.default_sel_indexes = []

    def get_anim_channels(self) -> None:
        """
        Parses the animation channel names from the mot file, using get_end_of_header
            input class vars: mot_fpath
         output: sets the value of the num_of_lines &  annimation_channels class vars
        """
        f_dir, mot_file_name = os.path.split(self.mot_fpath)
        os.chdir(f_dir)
        str_lines = []
        self.num_of_lines = 0
        with open(mot_file_name) as f:
            flines = f.readlines()
            self.num_of_lines += len(flines)
            for line_num in range(self.num_of_lines):  # these are the str_lines that have the actual values
                str_lines.append(flines[line_num])

        endheader_index = self.get_end_of_header(str_lines)
        self.animation_channels = str_lines[endheader_index].split('\t')[1:]

        

    def get_end_of_header(self, f_string_list: list) -> int:
        """
        returns index of the the line containing the "endheader" indicator
        input: string list of the lines of the mot file
        output: an int index of the endheader line.
        """
        count = 0
        i = 0
        while count < 1:
            count += f_string_list[i].count("endheader")
            i += 1
        return i

    def generate_csv(self, selected_channel_indexs: list) -> None:
        """
        input: list of ints
        input class_vars: mot_fpath, is_hind
        outputs: csv file with smoothed data.
        """
        channel_indexs_for_motf = [i + 1 for i in selected_channel_indexs]
        f_dir, mot_file_name = os.path.split(self.mot_fpath)
        smoothed_dir, csv_file_name = os.path.split(self.csv_fpath)
        os.chdir(f_dir)
        str_lines = []
        num_of_lines = 0
        if self.is_hind:
            start = 451
        else:
            start = 11
        with open(mot_file_name) as f:
            f_lines = f.readlines()
            num_of_lines += len(f_lines)
            for i in range(start, num_of_lines):  # these are the str_lines that have the actual values we want
                str_lines.append(f_lines[i])
        anim_keys_array = []
        for str_line in str_lines:
            row_of_string_keys = [str_val.strip() for str_val in str_line.split("\t")]
            row_of_anim_keys = [float(row_of_string_keys[i]) for i in channel_indexs_for_motf]
            anim_keys_array.append(row_of_anim_keys)
        self.apply_offsets(anim_keys_array, selected_channel_indexs)
        csv_array = savgol_filter(anim_keys_array, 555, 3, axis=0)
        # print(csv_array[0]) 
        # csv_array = numpy.anim_keys_array(anim_keys_array)
        os.chdir(smoothed_dir)
        numpy.savetxt(csv_file_name, csv_array, fmt='%.3f', delimiter=",")
        print("Smoothened csv ", csv_file_name, " has been created in: ", smoothed_dir )

    def apply_offsets(self, anim_keys_array, selected_channel_indexs):
        """
        takes a 2 dimensional list and applies offsets to each channel.
        atm this only runs  if using the default file and selection index.
        """
        if self.is_hind == True and selected_channel_indexs == self.default_sel_indexes:
            for each in anim_keys_array:
                # pelvis pitch
                each[0] *= consts.PELVIS_ROT_X_MODIFIER
                # pelvis roll
                each[1] += consts.PELVIS_ROT_Z_MODIFIER
                # pelvis yaw
                each[2] -= consts.PELVIS_ROT_Y_MODIFIER
                # pelvis foward
                each[3] *= consts.PELVIS_TRANSL_Z_MODIFIER
                # pelvis side to side translate
                each[4] *= consts.PELVIS_TRANSL_X_MODIFIER
                # hip extension/ flexion 
                each[6] = -(each[6] / consts.HIP_ROT_Y_MODIFIER)
                # hip abduction,
                each[7] += consts.HIP_ROT_Z_MODIFIER
                # hip lar,
                each[8] *= consts.HIP_ROT_X_MODIFIER
                # knee flexion(rotate Z)
                each[9] += consts.KNEE_MODIIFIER
                # twist(rotate x)
                each[10] *= consts.LEG_TWIST_X_MODIFIER
                # ankle controller (rotate z)
                each[11] = (.6 * each[11])  + consts.ANKLE_MODIFIER

        elif selected_channel_indexs == self.default_sel_indexes:
            for each in anim_keys_array:
                # chest Yaw/y
                each[2] -= consts.CHEST_ROT_Y_MODIFIER
                # shoulder extension / flexion
                each[3] /= consts.SHOULDER_ROT_Y_MODIFIER
                # shoulder abdduction/adduction
                each[4] = -each[4] - consts.SHOULDER_ROT_Z_MODIFIER
                # shoulder lar
                each[5] = -each[5] - consts.SHOULDER_ROT_X_MODIFIER
                # elbow (rotate z)
                each[6] = -each[6] - consts.ELBOW_MODIFIER
                # twist(rotatex
                each[7] = -each[7] + consts.ARM_TWIST_MODIFIER
                # wrist (rotate z)
                each[8] = -each[8] - consts.WRIST_MODIFIER
                # fingers (rotatez )
                each[9] -= consts.HAND_MODIFIER

# right leg
# generate_csv( "komodo06_run12_left_hind_IK.mot",True, (1,7), "Varius_right_hind_smoothed.csv" )
# generate_csv( "komodo06_run12_left_fore_IK_output rotmat_v2.mot",False, (1,4), "Varius_right_fore_smoothed.csv" )
