
DEFAULT_HIND_SELECTION = [0, 1, 2, 3, 4, 5, 13, 14, 15, 16, 17, 18, 19]
DEFAULT_FORE_SELECTION = [0, 1, 2, 13, 14, 15, 16, 17, 18, 19]
DEFAULT_HIND_MOT_FILENAME = "komodo06_run12_left_hind_IK.mot"
DEFAULT_FORE_MOT_FILENAME = "komodo06_run12_left_fore_IK_output rotmat_v2.mot"
DEFAULT_HIND_ANIM_ATTRS = [
        "IKSpine1_M.rotateX","IKSpine1_M.rotateZ", "IKSpine1_M.rotateY","Main.translateZ","Main.translateX"
        ,"Main.translateY","FKHip_R.rotateY","FKHip_R.rotateZ","FKHip_R.rotateX",
        "FKKnee_R.rotateZ","FKTwistLeg_R.rotateX","FKToes1_R.rotateZ","FKBigToe1_R.rotateZ","FKIndexToe1_R.rotateZ"
        ,"FKMiddleToe1_R.rotateZ", "FKRingToe1_R.rotateZ", "FKPinkyToe1_R.rotateZ"
        ]
DEFAULT_FORE_ANIM_ATTRS = [
        'IKSpine3_M.rotateX', 'IKSpine3_M.rotateZ', 'IKSpine3_M.rotateY', 'FKShoulder_R.rotateY', 'FKShoulder_R.rotateZ'
        , 'FKShoulder_R.rotateX', 'FKElbow_R.rotateZ', 'FKTwistArm_R.rotateX',
        'FKFingers1_R.rotateZ','FKThumbFinger1_R.rotateZ','FKIndexFinger1_R.rotateZ', 'FKMiddleFinger1_R.rotateZ',
        'FKRingFinger1_R.rotateZ', "FKPinkyFinger1_R.rotateZ"
        ]

DEFAULT_NON_LOOPING_ANIM_ATTR = "Main.translateZ"
DEFAULT_ANIM_DATA_STEP = 100
DEFAULT_HIND_ANIM_START_FRAME = 1
DEFAULT_FORE_ANIM_START_FRAME = 22
# ~~ Hind Modifiers ~~
PELVIS_ROT_X_MODIFIER = -.5
PELVIS_ROT_Z_MODIFIER = 10
PELVIS_ROT_Y_MODIFIER = 165
PELVIS_TRANSL_Z_MODIFIER = -100
PELVIS_TRANSL_X_MODIFIER = 100
HIP_ROT_Y_MODIFIER = 1.1
HIP_ROT_Z_MODIFIER = 10
HIP_ROT_X_MODIFIER = -1
KNEE_MODIIFIER = 85
LEG_TWIST_X_MODIFIER = -1
ANKLE_MODIFIER = 100
# ~~ Fore Modifiers ~~
CHEST_ROT_Y_MODIFIER = 170
SHOULDER_ROT_Y_MODIFIER = 2
SHOULDER_ROT_Z_MODIFIER = 20
SHOULDER_ROT_X_MODIFIER = 15
ELBOW_MODIFIER = 80
ARM_TWIST_MODIFIER = 125
WRIST_MODIFIER = 60
HAND_MODIFIER = 20
