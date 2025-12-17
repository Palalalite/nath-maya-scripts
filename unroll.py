import maya.cmds as cmd

#get driverJnt
twoJoints = cmd.ls(sl = 1)

jntA = twoJoints[0]
jntB = twoJoints[1]

side = jntA.split("_")[0]
partA = jntA.split("_")[1]
partB = jntB.split("_")[1]

print(side, partA, partB)

#pour l'épaule
def twistBase(jntA, jntB):
    #duplicate Bras joints
    print(jntA, jntB)
    
    brasJnt = cmd.duplicate(jntA, jntB, po = 1, n = side + "_" + partA + "Unroll_01")
    
    unrollJnt = []
    
    for item in brasJnt:
        newItem = cmd.rename(item, item + "_jnt")
        print(newItem)
        unrollJnt.append(newItem)
        
    print(unrollJnt)
    
    #cmd.parent(unrollJnt[0], side + "_Clavicule_01_CTRL")
   
    
    #create ikHandle (rotate plane solver)
    ikBase = cmd.ikHandle(sj = unrollJnt[0], ee = unrollJnt[1], n = side + "_" + partA + 'Unroll_01_ikH', sol = 'ikRPsolver', ap = 0, eh = 1, see = 1, s = 0, p = 1, w = 1, pw = 1)
    
    cmd.parent(ikBase[0], side + "_" + partB + "Offset_01_CTRL")
    
    for attributeA in [".tx", ".ty", ".tz", ".poleVectorX", ".poleVectorY", ".poleVectorZ"]:
        cmd.setAttr(ikBase[0] + attributeA, 0.0)
        


#pour le poignet
def twistTip(jntA, jntB):
    print(jntA, jntB)
    
    locators = []
    
    for i in range(3):
        newItem = cmd.spaceLocator(n = side + "_" + partB + "Unroll_0" + str(i) + "_loc")
        
        locators.append(newItem)
    
    print(locators)
    
    cmd.parent(locators[1], locators[0])
    cmd.parent(locators[0], side + "_" + partB + "Offset_01_CTRL", r = 1)
    cmd.parent(locators[2], side + "_" + partA + "Bendy_03_GRP", r = 1)
    
    #déplacer le locator 02, appliquer la contrainte Aim et parenter le locator 02 bendy manuellement

if partA == "Bras" or partA == "Jambe":
    print("c'est le twist " + partA)
    twistBase(jntA, jntB)
    

elif partA == "Coude" or partA == "Genou":
    print("c'est le twist " + partA)
    twistTip(jntA, jntB)

else:
    print("Choisir deux joints valides svp")