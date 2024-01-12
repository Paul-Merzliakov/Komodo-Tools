"""
FIX LOOP KEYS - NOT WORKING TEST IN ISOLATION WITH THE UI THEN WITH IT TO FIND WHATS WRONG
instead of adding an identical animation endframe widget to both stacks, why dont you add it to the layout and just have the two different ones in the stack?
"""
import maya.cmds as cmds

#loop val is a generic input variable that gets copied to a loop_count or loop endpoint depending on the mode. this is redundant but thought it would be good for clarity. 
def loop_keys(p_loop_mode : int = 0, loop_val: int = 300,endframe: int = 78,*args):
    all_controls = cmds.ls(transforms = True) 
    print(p_loop_mode, loop_val, endframe)
    keyed_controls  = []
    for each in all_controls:
        cmds.select(cl=True)
        if cmds.selectKey(each) > 0:
            keyed_controls.append(each)

    attributes = [] 
    for each in keyed_controls:
        control_attributes  = [each + "." + x for x in cmds.listAttr(each, keyable = True)]
        for attr in control_attributes:
            if cmds.keyframe(attr, q = True) != None:
                attributes.append(attr)

    cmds.currentTime(-10)
    for cntrl in keyed_controls:
        cntrl_attrs = [x for x in cmds.listAttr(each, keyable = True) if cmds.keyframe(cntrl + "." + x , q = True) != None]
        for attr in cntrl_attrs:
            cmds.setKeyframe( cntrl, attribute = attr, v = 0)
            print("set keyframe for ", attr)#debugg

    #for everything repeating it to 300
    new_attributes = [x for x in attributes if x != "Main.translateZ"]
    
    cmds.selectKey(new_attributes,time = (1,endframe), addTo = True, keyframe = True) #adding item to selection
    cmds.copyKey()
    if p_loop_mode == 0:
        loop_count = loop_val
        for i in range(1,loop_count):
            #print(i)
            cmds.pasteKey(time = (endframe * i,endframe * i), option = "merge", copies = 1)# because maya.cmds are dumb I have to put the frame i want to copy to twice in a tuple. 
        
    else:
        loop_endpoint = loop_val
        for i in range(endframe,loop_endpoint,endframe-1):
            #print(i)
            cmds.pasteKey(time = ( i,i), option = "merge", copies = 1)

        


    


