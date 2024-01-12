import maya.cmds as cmds
def rename_dorsal_spine(dorsal_verts) -> None:

    #centre pivots
    for each in dorsal_verts:
        cmds.xform(each, centerPivots = True)

    #renaming dorsalbverts based on z pivot position
    dors_verter_z_pivot =  [cmds.xform(each,query = True, scalePivot = True)[2] for each in dorsal_verts]
    sorted_dors_v = sorted(dors_verter_z_pivot)
    dors_vert_numbering = [sorted_dors_v.index(each)for each in dors_verter_z_pivot] 
    for i in range(len(dorsal_verts)):
        cmds.select(dorsal_verts[i])
        cmds.rename("dorsal_verterbra{}_lp".format(dors_vert_numbering[i]+1))

    #getting rid of 1s on the end.
    updated_dorsal_verterbra = cmds.ls("dorsal_verterbra*",transforms = True)
    for each in updated_dorsal_verterbra:
        if each.split("lp")[1] == "1":
            cmds.select(each)
            cmds.rename(each[:len(each) - 1])
rename_dorsal_spine(cmds.ls("dorsal_verterbra*",transforms = True))