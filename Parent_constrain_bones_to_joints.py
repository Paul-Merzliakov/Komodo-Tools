import maya.cmds as cmds
#clean


def constrain_spine() ->None:
    dorsal_verterbra = cmds.ls("Geo_dorsal_vert*", type = "transform" )
    dorsal_spine_joints = [x for x in cmds.ls("Spine*", type = "joint") if x.count("M") == 1]
    for i in range(len(dorsal_verterbra)):
        if i< 20:
            cmds.parentConstraint(dorsal_spine_joints[i], dorsal_verterbra[i],maintainOffset = True)
            # print("{} parented to {}".format(dorsal_verterbra[i],dorsal_spine_joints[i]))
        else: 
            cmds.parentConstraint("Chest_M", dorsal_verterbra[i],maintainOffset = True)
            


#simplified arm version. 
def constrain_arm(side: int ) ->None: # side denotes whether its left or right, so its either"L" or "R"

    namespace = "Geo_"
    if side == 'L':
        geo_char = 'l_'
    elif side == 'R':
        geo_char = 'r_'
    
    #formatting bone mesh names
    scapula = "".join([namespace, geo_char, "scapula_lp"])
    humerus = "".join([namespace, geo_char, "humerus_lp"])
    ulna = "".join([namespace, geo_char, "ulna_lp"])
    radius = "".join([namespace, geo_char, "radius_lp"])
    carpals = "".join([namespace, geo_char, "carpals_lp"])
    metacarpals = "".join([namespace, geo_char, "meta_carpals_lp"])
    thumb = "".join([namespace, geo_char,"thumb_lp"])
    indexfinger = "".join([namespace, geo_char, "index_finger_lp"])
    middlefinger = "".join([namespace, geo_char, "middlefinger_lp"])
    ringfinger = "".join([namespace, geo_char, "ringfinger_lp"])
    pinkyfinger = "".join([namespace, geo_char, "pinkie_lp"])


    #formatting joint names
    scapula_jnt = "".join(["Scapula_", side])
    shoulder_jnt = "".join(["Shoulder_",side])
    elbow_jnt = "".join(["Elbow_",side])
    twist_jnt = "".join(["TwistArm_",side])
    wrist_jnt = "".join(["Wrist_",side])
    hand_jnt = "".join(["Fingers1_",side])
    thumb_jnt  = "".join(["ThumbFinger1_",side])
    index_finger_jnt = "".join(["IndexFinger1_", side])
    middlefinger_jnt = "".join(["MiddleFinger1_", side])
    ringfinger_jnt = "".join(["RingFinger1_",side])
    pinky_finger_jnt = "".join(["PinkyFinger1_", side])

    #actual Parent constraints   ###DONT FORGET TO ADD MAINTAIN OFFSET TRUE FLAG 
    cmds.parentConstraint( scapula_jnt, scapula, maintainOffset = True )
    cmds.parentConstraint( shoulder_jnt, humerus, maintainOffset = True )
    cmds.parentConstraint( elbow_jnt, ulna, maintainOffset = True)
    cmds.parentConstraint( twist_jnt, radius, maintainOffset = True)
    cmds.parentConstraint( wrist_jnt, carpals,maintainOffset = True)
    cmds.parentConstraint( hand_jnt, metacarpals,maintainOffset = True)
    cmds.parentConstraint( thumb_jnt, thumb,maintainOffset = True)
    cmds.parentConstraint( index_finger_jnt, indexfinger, maintainOffset = True)
    cmds.parentConstraint( middlefinger_jnt, middlefinger, maintainOffset = True)
    cmds.parentConstraint( ringfinger_jnt, ringfinger, maintainOffset = True)
    cmds.parentConstraint( pinky_finger_jnt, pinkyfinger, maintainOffset = True)

def constrain_tail() ->None:
    caudal_verterbra = cmds.ls("Geo_caudal_verterbra*", type = "transform" )
    caudal_spine_joints = [x for x in cmds.ls("Tail*", type = "joint") if x.count("M") == 1]
    pelvis = cmds.ls("Geo_leg_pelvic_girdle_lp", type = "transform")[0]
    tail0 = cmds.ls("Tail0_M",type = "joint")[0]
    cmds.parentConstraint(tail0, pelvis,maintainOffset = True)
    for i in range(len(caudal_verterbra)- 1):
            cmds.parentConstraint(caudal_spine_joints[i+1],caudal_verterbra[i],maintainOffset = True)
            print("{} parented to {}".format(caudal_verterbra[i],caudal_spine_joints[i+1]))


def constrain_leg(side: int ) ->None: # side denotes whether its left or right, so its either"L" or "R"

    Gnamespace = "Geo_"
    if side == 'L':
        geo_char = 'l_'
    elif side == 'R':
        geo_char = 'r_'
    
    #formatting bone mesh names
    femur = "".join([Gnamespace, geo_char, "femur_lp"])
    tibia = "".join([Gnamespace, geo_char, "tibia_lp"])
    fibula = "".join([Gnamespace, geo_char, "fibula_lp"])
    tarsals = "".join([Gnamespace, geo_char, "tarsals_lp"])
    astra = "".join([Gnamespace,geo_char, "astragalocalcaneum_lp"])
    big_toe=  "".join([Gnamespace, geo_char,"bigtoe_lp"])
    index_toe = "".join([Gnamespace, geo_char, "indextoe_lp"])
    middle_toe = "".join([Gnamespace, geo_char, "middletoe_lp"])
    ring_toe = "".join([Gnamespace, geo_char, "ringtoe_lp"])
    pinky_toe = "".join([Gnamespace, geo_char, "pinkytoe_lp"])




    #formatting joint names
    hip_jnt = "".join(["Hip_",side])
    knee_jnt = "".join(["Knee_",side])
    twist_jnt = "".join(["TwistLeg_",side])
    ankle_jnt = "".join(["Ankle_",side])
    foot_jnt = "".join(["Toes1_",side])
    big_toe_jnt  = "".join(["BigToe1_",side])
    index_jnt = "".join(["IndexToe1_",side])
    middle_jnt = "".join(["MiddleToe1_",side])
    ring_jnt = "".join(["RingToe1_",side])
    pinky_jnt = "".join(["PinkyToe1_",side])

    #actual Parent constraints   ###DONT FORGET TO ADD MAINTAIN OFFSET TRUE FLAG 
    cmds.parentConstraint( hip_jnt, femur, maintainOffset = True )
    cmds.parentConstraint( knee_jnt, tibia, maintainOffset = True)
    cmds.parentConstraint( twist_jnt, fibula, maintainOffset = True)
    # cmds.parentConstraint( ankle_jnt, astra,maintainOffset = True)
    cmds.parentConstraint( foot_jnt, tarsals,maintainOffset = True)
    cmds.parentConstraint(big_toe_jnt,big_toe ,maintainOffset = True)
    cmds.parentConstraint(index_jnt,index_toe ,maintainOffset = True)
    cmds.parentConstraint(middle_jnt,middle_toe ,maintainOffset = True)
    cmds.parentConstraint(ring_jnt,ring_toe ,maintainOffset = True)
    cmds.parentConstraint(pinky_jnt,pinky_toe ,maintainOffset = True)


def constrain_neck() ->None:
    cervical_verterbra = cmds.ls("Geo_cervical_verterbra*", type = "transform" )
    cervical_spine_joints = [x for x in cmds.ls("Neck*", type = "joint") if x.count("M") == 1]
    for i in range(len(cervical_verterbra)):
            cmds.parentConstraint(cervical_spine_joints[i],cervical_verterbra[i],maintainOffset = True)
            print("{} parented to {}".format(cervical_verterbra[i],cervical_spine_joints[i]))



def constrain_bones(*args):
    parent_constraint_list = cmds.ls("Geo_*",type= "parentConstraint")
    for each in parent_constraint_list:
        cmds.delete(each)
    constrain_spine()
    constrain_leg('L')
    constrain_leg('R')
    constrain_arm('L')
    constrain_arm('R')
    constrain_neck()
    constrain_tail()
