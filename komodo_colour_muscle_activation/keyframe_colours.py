
from distutils.dep_util import newer_group
from locale import RADIXCHAR
from math import sqrt,cos,sin,radians
import maya.cmds as cmds
import os
import csv
# ~constants~ 
#controller channel names

#        
"""
ILTIB_right	AMBd_right	AMBv_right	FTIB_right	ILFEM_right	AFEM_right	PIFE_right	PIFI_right	PIT_right
	PTIB_right	FTE_right	FTId_right	FTIs_right	ILFIB_right	CFEML_right	CFEMB_right	femGAST_right	
    tibGAST_right	PLONG_right	PBREV_right	TIBA_right	EDL_right	FDL_right	FX	FY	FZ	MX	MY	MZ	
    L_hip_flex-ext_reserve	L_hip_abd-add_reserve	L_hip_LAR_reserve	L_knee_flex-ext_reserve	L_crus_pron-sup_reserve	L_ankle_flex-ext_reserve
    L_MTP_flex-ext_reserve	R_hip_flex-ext_reserve	R_hip_adb-add_reserve	R_hip_LAR_reserve	
    R_knee_flex-ext_reserve	R_crus_pron-sup_reserve	R_ankle_flex-ext_reserve	R_MTP_flex-ext_reserve
"""
# the main krux function is brought to you by this lifesaver https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio 

def remap_to_scalefactor(value): # takes the 0 - 1 float values and remaps them such that the max is orange and the min is blue
    OldMin = 0.0
    OldMax = 0.38325485961699
    NewMin = 1
    NewMax = 2.77
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((value - OldMin) * abs(NewRange)) / OldRange) + NewMin
    return NewValue
#print(remap_value( .5, 1, 0,.361,.006498)) #DEBUGGING LOG
#
def remap_to_rgbfloat(value): # takes the 0 - 1 float values and remaps them such that the max is orange and the min is blue
    OldMin = 0
    OldMax = 255
    NewMin = 0
    NewMax = 1
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((value - OldMin) * abs(NewRange)) / OldRange) + NewMin
    return NewValue
#print(remap_value( .5, 1, 0,.361,.006498)) #DEBUGGING LOG
#
def remap_scale_factor(value,NewMax): # takes the 0 - 1 float values and remaps them such that the max is orange and the min is blue
    OldMin = 1.
    OldMax = 2.77
    NewMin = 1
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  
    NewValue = (((value - OldMin) * abs(NewRange)) / OldRange) + NewMin
    return NewValue
#print(remap_value( .5, 1, 0,.361,.006498)) #DEBUGGING LOG
# test case sF:  2.6637248687132713 new colour: 245.06268792162095 642.3044963009766 638.7858919942236


def clamp(v):
    if v < 0:
        return 0
    if v > 255:
        return 255
    return int(v + 0.5)

class RGBRotate(object):
    def __init__(self):
        self.matrix = [[1,0,0],[0,1,0],[0,0,1]]
        self.r = 92
        self.g = 24
        self.b = 2
        self.brightness_scale_factor = 1


    def set_brightness(self, scale):
        self.brightness_scale_factor = scale


    def apply_brightness(self):
        new_r =  self.r * self.brightness_scale_factor 
        new_g = self.g * self.brightness_scale_factor * remap_scale_factor(self.brightness_scale_factor,255/(self.g * 2.7))
        new_b = self.b * self.brightness_scale_factor * remap_scale_factor(self.brightness_scale_factor,255/(self.b * 2.7))
        # new_r =  self.r * self.brightness_scale_factor 
        # new_g = self.g * self.brightness_scale_factor 
        # new_b = self.b * self.brightness_scale_factor 
        print("sF: ", self.brightness_scale_factor, "new colour:" , new_r, new_g, new_b)
        return(clamp(new_r), clamp(new_b), clamp(new_g))




def create_material(mesh : str)   -> str:
    shader = cmds.shadingNode("lambert", asShader = True , name = mesh + "_material")
    shader_SG = cmds.sets( renderable = True, noSurfaceShader = True, 
                          empty = True, name = '{0}SG'.format(shader) )
    cmds.connectAttr( '{0}.outColor'.format(shader),  '{0}.surfaceShader'.format(shader_SG) )
    cmds.select(mesh)
    cmds.hyperShade(assign = shader)
    return shader



objs = [ "ILTIB_iliotibialis_l", "AMB_ambiens_l", "FTIB_femorotibialis_l" , "AFEM_adductor_femoralis_v2__l", "PIF_puboischiofemoralis1_l", "PIT_Pubioischiotibialis_l", 
"PTIB_pubotibialis_l", "FTE_flex_tib_externus_l", "FTI_flex_tib_internus_l","ILFIB_iliofibularis_l", "caudalfemoralislongus_l" , "GAST_gastrocnemius_l", "PLONG_peroneus_longus_l", 
"PBREV_peroneus_brevis_l" , "TIBA_tibus_anterior_l", "EDL_extensor_digitorum_longus_l" ]
#print(len(objs))
# #creating shaders for each obj (geting their colour attribute)
shaders_colour = []
for obj in objs:
    shader = create_material(obj)
    shaders_colour.append(shader + ".color") #CHANGE TO ".baseColor" FOR ARNOLD



# #delete existing keyframes:
# def delete_keyframes(p_controller: list)-> None:
#     for each in p_controller:
#         cmds.selectKey(each,add = True,keyframe = True)
#         cmds.cutKey(animation = "keys", clear = True)
# delete_keyframes(shaders_colour)


#rgetting the rows from the csv file.
os.chdir("/Users/paulmerzliakov/Desktop/programming/dev/3D_stuff/Komodo_dragon_scripts/komodo_colour_muscle_activation")

rows = []
with open('smoothed_hind_muscle_activations.csv') as csv_f:
    freader = csv.reader(csv_f,delimiter =',')
    flines = list(freader)
    for i in range(len(flines)): #these are the lines that have the actual values
        rows.append(flines[i])
print(len(rows[1]))
"""
0.361 0.0951235 0.006498  = orange
0.006498 0.250762 0.361 = blue 

0.183749  0.17 , .1873749 midpoint colour for testing: 

rewritten midpoint


setAttr "lambert1.color" -type double3 0.006498 0.250762 0.361 ;
reformatted to python command:
cmds.setAttr("lambert1.color", 0.361 , 0.0951235, 0.006498, type = "double3")
"""





start_frame = 1
frame = start_frame
end_frame = len(rows[::87])
animation_ranges = [] # this is a multi dimensional array, for animation_ranges[i][j] i acesses which shader, j test whether its the first or last (o or 2)
for row in rows[::87]:
    cmds.currentTime( frame )
    colour_vals = [float(x.strip()) for x in row]
    for i in range(len(colour_vals)):
        rgb = RGBRotate() #this is actually the max activity colour we multiply based on this
        #print(shaders_colour[i], " being hue shifted by ", remap_to_hue_rot(colour_vals[i]), "degrees from red." )
        rgb.set_brightness(remap_to_scalefactor(colour_vals[i]))
        #print("\n",rgb.apply_brightness()[0])
        cmds.setAttr(shaders_colour[i],remap_to_rgbfloat(rgb.apply_brightness()[0]),remap_to_rgbfloat(rgb.apply_brightness()[1]),remap_to_rgbfloat(rgb.apply_brightness()[2]), type = "double3")
        cmds.setKeyframe(shaders_colour[i])
    # print(shaders_colour[i], "rotates ", colour_vals[i], "degrees" ) # DEBUGGING
    # storring the beginning and end values for interpolation
    if frame == end_frame:
        for i in range(len(colour_vals)):
            animation_ranges[i][1] = colour_vals[i]
            #print("end frame of{} is value{}".format(shaders_colour[i],colour_vals[i]))
    elif frame == start_frame:
        for i in range(len(colour_vals)):
            animation_ranges.append([colour_vals[i],0]) # this 0 is just a placeholder to ensure each item is an array
            #print("begining frame of{} is value{}".format(shaders_colour[i],colour_vals[i]))
    
    frame += 1
for each in animation_ranges:
    print("end frame of{} is value{}".format(each, colour_vals[i]))
    print("begining frame of{} is value{}".format(shaders_colour[i],colour_vals[i]))
    

for each in shaders_colour:
    #use linear interpolation where time is x and value is y
    value_0 = animation_ranges[shaders_colour.index(each)][1]
    value_f = animation_ranges[shaders_colour.index(each)][0]
    time_0 = 1
    time_f = 5 # number of frames to add minus 2 
    #print(each,"value_0 is: ",value_0, "value_f is: ", value_f) # DEBUGGING
    for time_n in range(time_0+1,time_f+1): # this should produce three interpolated points
            cmds.currentTime(end_frame+time_n - 1)
            #print(cmds.currentTime(query = True))
            value_n = value_0 + ((value_f - value_0) / (time_f - time_0))*(time_n - time_0)
            #print(each, " time_n is: ", time_n, "value_n is: ", value_n) # DEBUGGING LOG
            rgb = RGBRotate() #this is actually the max activity colour we multiply based on this
            rgb.set_brightness(remap_to_scalefactor(value_n))
            cmds.setAttr(each,remap_to_rgbfloat(rgb.apply_brightness()[0]),remap_to_rgbfloat(rgb.apply_brightness()[1]),remap_to_rgbfloat(rgb.apply_brightness()[2]), type = "double3")
            cmds.setKeyframe(each)






