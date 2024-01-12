import maya.cmds as cmds
parent_constraint_list = cmds.ls("Geo_*",type= "parentConstraint")
for each in parent_constraint_list:
    cmds.delete(each)
