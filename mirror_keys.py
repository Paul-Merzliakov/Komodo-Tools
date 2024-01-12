"""
copyKey -time ":" -float ":" -hierarchy none -controlPoints 0 -shape 1 {"FKHip_R.rotateX", "FKHip_R.rotateY", "FKHip_R.rotateZ"};
select -r FKHip_L ;
selectKey -clear ;
currentTime 10 ;
pasteKey -time 10 -float 10 -option merge -copies 1 -connect 0 -timeOffset 0 -floatOffset 0 -valueOffset 0;
scaleKey -scaleSpecifiedKeys 1 -autoSnap 0 -time ":" -float ":" -timeScale -1 -timePivot 48.5 -floatScale -1 -floatPivot 48.5 -valueScale 1 -valuePivot 0 -hierarchy none -controlPoints 0 -shape 1 {"FKHip_L.rotateX", "FKHip_L.rotateY", "FKHip_L.rotateZ"};

USE BEFORE LOOP ANIMATION SCRIPT

"""
import maya.cmds as cmds
def mirror(*args):
    all_controls = cmds.ls(transforms = True) 
    keyed_controls  = []
    for each in all_controls:
        cmds.select(cl=True)
        if cmds.selectKey(each) > 0:
            keyed_controls.append(each)

    attributes = [] 
    for each in keyed_controls:
        control_attributes  = [each + "." + x for x in cmds.listAttr(each, keyable = True)]
        #print( each )
        for attr in control_attributes:
            if cmds.keyframe(attr, q = True) != None and attr.count("_R") > 0:
                #print(each, attr)
                attributes.append(attr)
    for attr in attributes:
        cntrl, attribute_only = attr.split('.')
        l_cntrl,junk =  cntrl.split("_R")
        print(cntrl)
        l_cntrl += "_L"
        cmds.copyKey(cntrl, attribute = attribute_only, time = (39,78))
        cmds.pasteKey(l_cntrl, attribute = attribute_only, time = (-100,-100),option = "merge")
        cmds.select(cl=True)
        cmds.copyKey(cntrl, attribute = attribute_only, time = (0,39))
        cmds.pasteKey(l_cntrl, attribute = attribute_only,time = (-61,-61), option = "merge" )
        cmds.keyframe(l_cntrl +"."+ attribute_only, edit = True, timeChange = 101, option = "over",relative = True)
        cmds.select(cl=True)

