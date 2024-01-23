# this takes the mot data, smooths it and then saves it into a csv file that can be read in maya and used to plug in all the numbers. this is because the maya scripting enviornemnt doesnt natively support mupy scipy ect.
import os
from scipy.signal import savgol_filter
import numpy

# Hindlimb Offsets
HIPZ_OFFSET = 10
HIPX_OFFSET = 115
PELVISY_OFFSET = 165
KNEE_OFFSET = 85
ANKLE_OFFSET = 115
# Forelimb Offsets
SHOULDERZ_OFFSET = 10
SHOULDERX_OFFSET = 115
ELBOW_OFFSET = 80
TWIST_OFFSET = 125
WRIST_OFFSET = 60
HAND_OFFSET = 20

HIND_DEFAULT_SELECTION = [0, 1, 2, 3, 4, 5, 13, 14, 15, 16, 17, 18, 19]
FORE_DEFAULT_SELECTION = [0, 1, 2, 13, 14, 15, 16, 17, 18, 19]


class DenoiseFileData():
    def __init__(self):
        self.num_of_lines = 0
        self.animation_channels = []
        self.mot_fpath = ""
        self.csv_fpath = ""
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
        input: list of in
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
        if self.is_hind == True and selected_channel_indexs == HIND_DEFAULT_SELECTION:
            for each in anim_keys_array:
                # pelvis pitch/ rotatex
                each[0] *= -.5
                # pelvis roll/ rotatez
                each[1] += HIPZ_OFFSET
                # pelvis yaw/ rotatey
                each[2] -= PELVISY_OFFSET
                # pelvis foward
                each[3] *= -100
                # pelvis side to side translate
                each[4] *= 100
                # hip extension/ flexion  (yrotation)
                each[6] = -(each[6] / 1.1)
                # hip abduction, (zrotation)g
                each[7] += 10
                # hip lar, (xrotation)
                each[8] = -(each[8] / 1.)
                # knee flexion
                each[9] += KNEE_OFFSET
                # twist
                each[10] = -each[10]
                # ankle controller
                each[11] += ANKLE_OFFSET + 20

        elif selected_channel_indexs == FORE_DEFAULT_SELECTION:
            for each in anim_keys_array:
                # chest Yaw/y
                each[2] -= 170
                # shoulder_y
                each[3] /= 2
                # shoulder_z
                each[4] = -each[4] - 20
                # shoulder_x
                each[5] = -each[5] - 15
                # elbowx
                each[6] = -each[6] - ELBOW_OFFSET
                # twist
                each[7] = -each[7] + TWIST_OFFSET
                # wrist
                each[8] = -each[8] - WRIST_OFFSET
                # knee flexion
                each[9] -= HAND_OFFSET

# right leg
# generate_csv( "komodo06_run12_left_hind_IK.mot",True, (1,7), "Varius_right_hind_smoothed.csv" )
# generate_csv( "komodo06_run12_left_fore_IK_output rotmat_v2.mot",False, (1,4), "Varius_right_fore_smoothed.csv" )
