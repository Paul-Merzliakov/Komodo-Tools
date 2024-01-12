import maya.cmds as cmds
#most stupid and bad code ive ever written

def parent_chain(bones) -> None:
    for i in range(len(bones)):
       if i < len(bones)-1:
           cmds.parent(bones[i+1], bones[i])

def parent_ribs_to_verter(bones, parent_bones) -> None:
    for i in range(len(bones)):
        cmds.parent(bones[i], parent_bones[i+1])

def parent_true_ribs_to_ribs(bones,parent_bones) -> None: 
    for i in range(3):
        cmds.parent(bones[i], parent_bones[i+15])
def parent_legs(side) ->None: #side is l or r(left or right)
    prefix = side + "_"
    cmds.parent( "".join([ prefix,"tibia_lp"]), "".join([ prefix,"femur_lp"]) )
    cmds.parent( "".join( [ prefix,"fibula_lp"]), "".join([ prefix,"femur_lp"]) )
    cmds.parent( "".join( [ prefix,"astragalocalcaneum_lp"]), "".join([ prefix,"fibula_lp"]) )
    cmds.parent( "".join( [ prefix,"tarsals_lp"]), "".join([ prefix,"astragalocalcaneum_lp"]) )
    cmds.parent( "".join( [ prefix,"meta_tarsals_lp"]), "".join([ prefix,"tarsals_lp"]) )
    cmds.parent( "".join( [ prefix,"back_phalanges_lp"]), "".join([ prefix,"meta_tarsals_lp"]) )
    cmds.parent( "".join( [ prefix,"hind_claws_lp"]), "".join([ prefix,"back_phalanges_lp"]) )

def parent_arms(side): 
    prefix = side + "_"
    cmds.parent( "".join([ prefix,"clavicle_lp"]), "".join([ prefix,"epicoracoid_lp"]) )
    cmds.parent( "".join([ prefix,"scapula_lp"]), "".join([ prefix,"epicoracoid_lp"]) )
    cmds.parent( "".join( [ prefix,"humerus_lp"]), "".join([ prefix,"scapula_lp"]) )
    cmds.parent( "".join( [ prefix,"ulna_lp"]), "".join([ prefix,"humerus_lp"]) )
    cmds.parent( "".join( [ prefix,"radius_lp"]), "".join([ prefix,"humerus_lp"]) )
    cmds.parent( "".join( [ prefix,"carpals_lp"]), "".join([ prefix,"radius_lp"]) )
    cmds.parent( "".join( [ prefix,"meta_carpals_lp"]), "".join([ prefix,"carpals_lp"]) )
    cmds.parent( "".join( [ prefix,"front_phalanges_lp"]), "".join([ prefix,"meta_carpals_lp"]) )
    cmds.parent( "".join( [ prefix,"front_claws_lp"]), "".join([ prefix,"front_phalanges_lp"]) )

#rename dorsal verterbae

dorsal_verterbra = cmds.ls("dorsal_verterbra*",transforms = True)
print(dorsal_verterbra)
#parenting dorsal verterbra to one another
parent_chain(dorsal_verterbra)

#parenting ribs to dorsal verterbra
left_ribs = cmds.ls("l_rib*",transforms = True)
right_ribs = cmds.ls("r_rib*",transforms = True)
parent_ribs_to_verter(left_ribs, dorsal_verterbra)
parent_ribs_to_verter(right_ribs,dorsal_verterbra)

#parenting true ribs to ribs
left_true_ribs = cmds.ls("l_true_rib*", transforms = True)
right_true_ribs = cmds.ls("r_true_rib*", transforms = True)
parent_true_ribs_to_ribs(left_true_ribs,left_ribs)
parent_true_ribs_to_ribs(right_true_ribs,right_ribs)

#parenting caudal verterbra to one another
caudal_verterbra = cmds.ls("caudal_verterbra*", transforms = True)
parent_chain(caudal_verterbra)
#parenting sacral verterbrae
sacral_verterbra =  cmds.ls("sacral_verterbrae*",transforms = True)
parent_chain(sacral_verterbra)
#making sacral the root
cmds.parent(caudal_verterbra[0],sacral_verterbra[0])
cmds.parent(dorsal_verterbra[0], sacral_verterbra[len(sacral_verterbra)-1])
#making pelvis the root
pelvis = cmds.ls("leg_pelvic_girdle_lp")[0]
cmds.parent(sacral_verterbra[0],pelvis)

#parenting legs to pelvis and one another
cmds.parent("r_femur_lp", pelvis)
cmds.parent("l_femur_lp", pelvis)
parent_legs("r")
parent_legs("l")

#parenting sternum to 16th dorsal rib
cmds.parent( "sternum_lp",dorsal_verterbra[15] )
#parenting: episternum- >sternum, l_epicoraoid & r_epicoraoid - > sternum 
cmds.parent(  "episternum_lp" ,  "sternum_lp" )
cmds.parent(  "l_epicoracoid_lp" ,  "sternum_lp" )
cmds.parent(  "r_epicoracoid_lp" ,  "sternum_lp" )
#parenting arms to another
parent_arms("r")
parent_arms("l") 
#parenting neck verterbra to one another(using parent_chain function)
cervical_verterbra = cmds.ls("cervical_vertebra*", transforms = True)
parent_chain(cervical_verterbra)
#parenting teeth, eyesockets, gular bones to skull
cmds.parent("gular_bones_lp" ,"skull_lp")
cmds.parent( "bottom_teeth_lp","skull_lp")
cmds.parent( "top_teeth_lp","skull_lp")
cmds.parent( "eyesockets_lp","skull_lp")
#parenting skull to last cervical:
cmds.parent("skull_lp",cervical_verterbra[4])
#parenting first cervical to last dorsal
cmds.parent( cervical_verterbra[0],dorsal_verterbra[20] )