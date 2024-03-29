import maya.cmds as cmds


def loop_keys(p_loop_mode : int = 0, loop_val: int = 300,endframe: int = 78,*args):
    # loop val is a generic input variable that gets copied to a loop_count or loop endpoint depending on the mode.
    all_controls = cmds.ls(transforms = True) 
    print(p_loop_mode, loop_val, endframe)
    keyed_controls  = []
    for control in all_controls:
        cmds.select(cl=True)
        if cmds.selectKey(control) > 0:
            keyed_controls.append(control)

    attributes = [] 
    for keyed_control in keyed_controls:
        control_attributes  = [keyed_control + "." + x for x in cmds.listAttr( keyed_control,  keyable = True)]
        for attr in control_attributes:
            if cmds.keyframe(attr, q = True) != None:
                attributes.append(attr)

    #this block of code sets all animation keys to 0 at frame -10. This  make muscle simulating easier
    cmds.currentTime(-10)
    for cntrl in keyed_controls:
        cntrl_attrs = [x for x in cmds.listAttr(cntrl, keyable = True) if cmds.keyframe(cntrl + "." + x , q = True) != None]
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

