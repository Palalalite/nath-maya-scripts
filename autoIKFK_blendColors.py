import maya.cmds as cmd
import maya.OpenMaya as om


#user variables
IKlabel = 'Pied' # 'Main' ou 'Pied'
arm = 0
ctlScale = 9
PVdistance = .8
stretchy = 1
offset = 1

#get driverJnt
driverJnt = cmd.ls(sl = 1)


#define bras, coude and poignet
baseJnt = driverJnt[0]
midJnt = driverJnt[1]
endJnt = driverJnt[2]

print('driverJnt = ' + str(driverJnt))


#determine the label by splitting the names of the joints....
labels = driverJnt.copy()
for item in labels:
    newItem = item.split('_') #ex : we get [G, bras, 01, jnt]
    labels[labels.index(item)] = '_'.join(newItem[0:2]) #ex : keep 'G_Bras_01'

print('labels = ' + str(labels))


#determine color of the ctrls
ctlColor = 0

if "G" in newItem:
    ctlColor = 6

elif "D" in newItem:
    ctlColor = 13


#determine orientation of driver joints (which way is the elbow oriented?), this is for placing the PV correctly
#vector variable
translateVector = [0, 0, 0]
normals = [0, 0, 0]


#check joint chain direction (X, Y, Z, +, - ?)
for item in driverJnt:
    #check the joint chain orientation, by checking child translates
    if driverJnt.index(item) < 2:
        childJnt = cmd.listRelatives(item, c = 1)
    
    
        #get child joint's translates for custom CTRL orienting
        if childJnt :
            print (str(item) + ' child is ' + str(childJnt[0]))
            translatesRaw = [cmd.getAttr(childJnt[0] + '.translateX'), cmd.getAttr(childJnt[0] + '.translateY'), cmd.getAttr(childJnt[0] + '.translateZ')]
        else :
            print (str(item) + ' has no child')
            translatesRaw = [cmd.getAttr(str(item) + '.translateX'), cmd.getAttr(str(item) + '.translateY'), cmd.getAttr(str(item) + '.translateZ')]
            
        print ('translatesRaw = ' + str(translatesRaw))
    
        translatesAbs = [abs(item) for item in translatesRaw]
        #this is called list comprehension https://python.doctor/page-comprehension-list-listes-python-cours-debutants
        #abs(x) returns absolute value of a number https://docs.python.org/3/library/functions.html#abs
    
        print ('translatesAbs = ' + str(translatesAbs))
        
        highestTranslatesAbs = max(translatesAbs)
        
        
        #if the max value is at index n, then make the corresponding variable true
        if translatesAbs.index(highestTranslatesAbs) == 0:
            if translatesRaw[translatesAbs.index(highestTranslatesAbs)] > 0 :
                translateVector[0] = 1
            if translatesRaw[translatesAbs.index(highestTranslatesAbs)] < 0 :
                translateVector[0] = -1

        if translatesAbs.index(highestTranslatesAbs) == 1:
            if translatesRaw[translatesAbs.index(highestTranslatesAbs)] > 0 :
                translateVector[1] = 1
            if translatesRaw[translatesAbs.index(highestTranslatesAbs)] < 0 :
                translateVector[1] = -1

        if translatesAbs.index(highestTranslatesAbs) == 2:
            if translatesRaw[translatesAbs.index(highestTranslatesAbs)] > 0 :
                translateVector[2] = 1
            if translatesRaw[translatesAbs.index(highestTranslatesAbs)] < 0 :
                translateVector[2] = -1
                
                
        #if the max value is at index n, then make the corresponding variable true
        if translatesAbs.index(max(translatesAbs)) == 0:
            normals[0] = 1
    
        if translatesAbs.index(max(translatesAbs)) == 1:
            normals[1] = 1
            
        if translatesAbs.index(max(translatesAbs)) == 2:
            normals[2] = 1


print('translateVector = ' + str(translateVector))
print('normals = ' + str(normals))


#find joint orient axis...
orientRaw = [cmd.getAttr(midJnt + '.jointOrientX'), cmd.getAttr(midJnt + '.jointOrientY'), cmd.getAttr(midJnt + '.jointOrientZ')]
print('orientRaw = ' + str(orientRaw))

orientAbs = [abs(angle) for angle in orientRaw]
print('orientAbs = ' + str(orientAbs))

highestOrientAbs = max(orientAbs)

orientVector = [0, 0, 0]

if orientAbs.index(highestOrientAbs) == 0:
    if orientRaw[orientAbs.index(highestOrientAbs)] > 0 :
        orientVector[0] = 1
    if orientRaw[orientAbs.index(highestOrientAbs)] < 0 :
        orientVector[0] = -1

if orientAbs.index(highestOrientAbs) == 1:
    if orientRaw[orientAbs.index(highestOrientAbs)] > 0 :
        orientVector[1] = 1
    if orientRaw[orientAbs.index(highestOrientAbs)] < 0 :
        orientVector[1] = -1

if orientAbs.index(highestOrientAbs) == 2:
    if orientRaw[orientAbs.index(highestOrientAbs)] > 0 :
        orientVector[2] = 1
    if orientRaw[orientAbs.index(highestOrientAbs)] < 0 :
        orientVector[2] = -1

print('orientVector = ' + str(orientVector))


#where do we move the PV orig and switch?
translateAmount = translatesRaw[translatesAbs.index(max(translatesAbs))] * 2 #get the farthest translate of the mid jnt and multiply
switchTranslate = translatesRaw[translatesAbs.index(max(translatesAbs))] * .6

switchNormals = [abs(normal) for normal in translateVector]

translates = [0, 0, 0]

print('translateAmount = ' + str(translateAmount))
print('switchTranslate = ' + str(switchTranslate))


#determine orientation of the orig 
if translateVector[0] != 0: #if there is a translate on the X axis...
    
    if orientVector[1] != 0: #if there is a joint orient on the Y axis...
        translates[2] = translateAmount * orientVector[1] #move this amount on the Z axis.
        
        
    elif orientVector[2] != 0: #if there is a joint orient on the Z axis...
        translates[1] = translateAmount * -orientVector[2] #move this amount on the Y axis.
        
        
elif translateVector[1] != 0: #if there is a translate on the Y axis...
    
    if orientVector[0] != 0: #if there is a joint orient on the X axis...
        translates[2] = translateAmount * -orientVector[0] #move this amount on the Z axis.
        
    elif orientVector[2] != 0: #if there is a joint orient on the Z axis...
        translates[0] = translateAmount * orientVector[2] #move this amount on the X axis.
    
    
elif translateVector[2] != 0: #if there is a translate on the Z axis...
    
    if orientVector[0] != 0: #if there is a joint orient on the X axis...
        translates[1] = translateAmount * orientVector[0] #move this amount on the Y axis.
        
        
    elif orientVector[1] != 0: #if there is a joint orient on the Y axis...
        translates[0] = translateAmount * -orientVector[1] #move this amount on the X axis.
        
     
else:
    print("The joint angle orientation check didn't work.")
    

print('switchNormals = ' + str(switchNormals))
print('translates = ' + str(translates))


#IK duplicates
cmd.select(baseJnt, midJnt, endJnt, r = 1)

IKchain = cmd.duplicate(po = 1, rc = 1) #children are duplicated too

print('IKchain (old) = ' + str(IKchain))


#rename the IKchain and update the list
#if having trouble with getting indexes of lists from item names in loops...
#please check this https://www.dataquest.io/blog/tutorial-advanced-for-loops-python-pandas/
for item in IKchain:
    newItem = cmd.rename(item, labels[IKchain.index(item)] + 'IK_01_jnt')
    IKchain[IKchain.index(item)] = newItem
    
print('IKchain = ' + str(IKchain))

#set radius, outliner color and color of the joints
for item in IKchain:
    radius = cmd.getAttr(item + '.radius')
    cmd.setAttr(item + '.radius', radius * 1.1)
    cmd.setAttr(item + '.overrideEnabled', 1)
    cmd.setAttr(item + '.overrideColor', 13)
    cmd.setAttr(item + '.useOutlinerColor', 1)
    cmd.setAttr(item + '.outlinerColorR', 1)
    cmd.setAttr(item + '.outlinerColorG', 0)
    cmd.setAttr(item + '.outlinerColorB', 0)


#define ik joint variables
baseIK = IKchain[0]
midIK = IKchain[1]
endIK = IKchain[2]


#create ik handle
ikHand = cmd.ikHandle(sj = baseIK, ee = endIK, n = labels[0] + '_ikHandle', sol = 'ikRPsolver', ap = 0, eh = 1, see = 1, s = 0, p = 1, w = 1, pw = 1)
print('ikHand = ' + str(ikHand))

#create PV CTRL and PV Orig
PVctrl = cmd.circle(n = labels[0] + 'PV_01_CTRL' , r = ctlScale * 0.4 , nr = (orientVector[0] * -1.0, orientVector[1] * -1.0, orientVector[2] * -1.0) , d = 1, s = 4)

print('PVctrl = ' + PVctrl[0])
PVorig2 = cmd.group(n = PVctrl[0][:-8] + '_02_GRP')
PVorig1 = cmd.group(n = PVorig2[:-7] + '_01_GRP')


#define position of the joints
baseJntPos = cmd.xform(baseJnt, q = 1, ws = 1, t = 1)
midJntPos = cmd.xform(midJnt, q = 1, ws = 1, t = 1)
endJntPos = cmd.xform(endJnt, q = 1, ws = 1, t = 1)

print('baseJntPos = ' + str(baseJntPos))


#define PV orig position https://www.youtube.com/watch?v=bB_HL1tBVHY
baseJntVec = om.MVector(baseJntPos[0], baseJntPos[1], baseJntPos[2])
midJntVec = om.MVector(midJntPos[0], midJntPos[1], midJntPos[2])
endJntVec = om.MVector(endJntPos[0], endJntPos[1], endJntPos[2])

line = (endJntVec - baseJntVec)
point = (midJntVec - baseJntVec)

scaleValue = (line * point) / (line * line)
projVec = line * scaleValue + baseJntVec

baseToMidLen = (midJntVec - baseJntVec).length()
midToEndLen = (endJntVec - midJntVec).length()
totalLen = baseToMidLen + midToEndLen

poleVecPos = (midJntVec - projVec).normal() * (totalLen * PVdistance) + midJntVec


#place PV Orig at precedently calculated position
cmd.move(poleVecPos[0], poleVecPos[1], poleVecPos[2], PVorig1, r = 0, os = 1, wd = 1)


#orient PV Orig
cmd.aimConstraint(midJnt, PVorig1, aim = (0.0, 0.0, 1.0), u = (0.0, 1.0, 0.0), wut = "scene")
cmd.delete(PVorig1, cn = 1)


#create PV constraint
cmd.poleVectorConstraint(PVctrl[0], ikHand[0], w = 1)


#create IK ctrl
IKctrl = cmd.circle(n = str(labels[0]) + 'IK_01_CTRL' , r = ctlScale, nr = (normals), d = 1, s = 4)
cmd.delete(ch = 1)
print('IKctrl = ' + str(IKctrl))

IKorig2 = cmd.group(n = IKctrl[0][:-8] + '_02_GRP')
IKorig1 = cmd.group(n = IKorig2[:-7] + '_01_GRP')
cmd.matchTransform(IKorig1, endIK, pos = 1, rot = arm)

if arm:
    offset = 0
else:
    offset = 1

cmd.orientConstraint(IKctrl[0], endIK, mo = offset)


#parent only the ikHandle under IK ctrl and hide it
cmd.parent(ikHand[0], IKctrl[0])
cmd.setAttr(ikHand[0] + '.v', 0)


#color the ctrls
for item in PVctrl[0], IKctrl[0]:
    cmd.setAttr(item + '.overrideEnabled', 1)
    cmd.setAttr(item + '.overrideColor', ctlColor)

#end of IK part.


#duplicate FK
cmd.select(baseJnt, midJnt, endJnt, r = 1)

FKchain = cmd.duplicate(po = 1, rc = 1) #children are duplicated too

print('FKchain (old) = ' + str(FKchain))


#rename the FKchain and update the list
#if having trouble with getting indexes of lists from item names in loops...
#please check this https://www.dataquest.io/blog/tutorial-advanced-for-loops-python-pandas/
for item in FKchain:
    newItem = cmd.rename(item, labels[FKchain.index(item)] + 'FK_01_jnt')
    FKchain[FKchain.index(item)] = newItem
    
print('FKchain = ' + str(FKchain))


#set radius, outliner color and color of the joints
for item in FKchain:
    radius = cmd.getAttr(item + '.radius')
    cmd.setAttr(item + '.radius', radius * 1.2)
    cmd.setAttr(item + '.overrideEnabled', 1)
    cmd.setAttr(item + '.overrideColor', 6)
    cmd.setAttr(item + '.useOutlinerColor', 1)
    cmd.setAttr(item + '.outlinerColorR', 0)
    cmd.setAttr(item + '.outlinerColorG', 0)
    cmd.setAttr(item + '.outlinerColorB', 1)


#define fk joint variables
baseFK = FKchain[0]
midFK = FKchain[1]
endFK = FKchain[2]


#create ctrl for each FK joints, and parent them automatically
for item in FKchain:    
    ctrl = cmd.circle(n = str(labels[FKchain.index(item)]) + 'FK_01_CTRL' , r = ctlScale, nr = (switchNormals))
    cmd.delete(ch = 1)
    orig = cmd.group(n = ctrl[0][:-5] + '_GRP')
    
    cmd.setAttr(ctrl[0] + '.overrideEnabled', 1)
    cmd.setAttr(ctrl[0] + '.overrideColor', ctlColor)
    
    print('ctrl = ' + str(ctrl))
    
    cmd.matchTransform(orig, item, pos = 1, rot = 1)
    
    cmd.pointConstraint(ctrl[0], item, mo = 0)
    cmd.orientConstraint(ctrl[0], item, mo = 0)
    
    
    
    #parent the orig under the parent's ctrl
    #check if we are at item[1] in this loop, then execute parentJnt check
    if FKchain.index(item) > 0:
        
        parentJnt = cmd.listRelatives(item, p = 1)
        
        if parentJnt :
            print (str(item) + "'s parent is " + str(parentJnt[0]))
            childOrig = orig
            print('childOrig = ' + childOrig)
            parentCtrl = str(labels[FKchain.index(item) - 1]) + 'FK_01_CTRL'
            print('parentCtrl = ' + parentCtrl)
            
            cmd.parent(childOrig, parentCtrl)

#end of FK part.


#create IKFK switch
switchCtrl = cmd.circle(n = labels[0] + 'Switch_01_CTRL' , r = ctlScale * .3 , nr = (switchNormals[1], switchNormals[2], switchNormals[0]))

cmd.setAttr(switchCtrl[0] + '.overrideEnabled', 1)
cmd.setAttr(switchCtrl[0] + '.overrideColor', 14)
cmd.setAttr(switchCtrl[0] + '.scaleX', 0.8)
cmd.setAttr(switchCtrl[0] + '.scaleY', 0.8)
cmd.setAttr(switchCtrl[0] + '.scaleZ', 0.8)
cmd.select(switchCtrl[0], r = 1)
cmd.makeIdentity(apply=True, t=1, r=1, s=1, n=2)
cmd.delete(ch = 1)

switchOrig = cmd.group(n = switchCtrl[0][:-5] + '_GRP')
print('switchCtrl = ' + str(switchCtrl))


#constrain it to endJnt
cmd.parentConstraint(endJnt, switchOrig, mo = 0, sr = 'none', st = 'none')


#select switchCtrl control vertices and translate along Z axis
cmd.select(switchCtrl[0] + '.cv[:]', r = 1)
cmd.move(switchTranslate, x = switchNormals[1], y = switchNormals[0], z = switchNormals[2], r = 1, os = 1, wd = 1)


#add IKFK attribute to switchCtrl (add 'keyable = 1' so it appears in channel box!)
cmd.select(switchCtrl[0], r = 1)
cmd.addAttr(longName='SwitchIKFK', keyable = 1, at = 'double', min = 0, max = 1, dv = 0)


#lock and hide the other channel box attributes
cmd.setAttr(switchCtrl[0] + '.tx', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] + '.ty', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] + '.tz', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] + '.rx', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] + '.ry', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] + '.rz', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] + '.sx', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] + '.sy', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] + '.sz', lock = 1, keyable = 0, channelBox = 0)
cmd.setAttr(switchCtrl[0] +  '.v', lock = 1, keyable = 0, channelBox = 0)


#create the constraints for the joints
for (fkJoint, ikJoint, drvJoint) in zip(FKchain, IKchain, driverJnt):
    blendPos = cmd.createNode("blendColors", n = str(labels[driverJnt.index(drvJoint)]) + '_BCT')
    blendRot = cmd.createNode("blendColors", n = str(labels[driverJnt.index(drvJoint)]) + '_BCR')
    blendScl = cmd.createNode("blendColors", n = str(labels[driverJnt.index(drvJoint)]) + '_BCS')
    
    cmd.connectAttr(fkJoint + ".translate", blendPos + ".color1")
    cmd.connectAttr(ikJoint + ".translate", blendPos + ".color2")  
    
    cmd.connectAttr(fkJoint + ".rotate", blendRot + ".color1")
    cmd.connectAttr(ikJoint + ".rotate", blendRot + ".color2")
    
    cmd.connectAttr(fkJoint + ".scale", blendScl + ".color1")
    cmd.connectAttr(ikJoint + ".scale", blendScl + ".color2")
    
    cmd.connectAttr(blendPos + ".output", drvJoint + ".translate")
    cmd.connectAttr(blendRot + ".output", drvJoint + ".rotate")
    cmd.connectAttr(blendScl + ".output", drvJoint + ".scale")
    
    cmd.connectAttr(switchCtrl[0] + '.SwitchIKFK', blendPos + ".blender")
    cmd.connectAttr(switchCtrl[0] + '.SwitchIKFK', blendRot + ".blender")
    cmd.connectAttr(switchCtrl[0] + '.SwitchIKFK', blendScl + ".blender")


#create the reverse node, if it doesn't exists
if cmd.objExists(str(labels[0]) + '_reverse'):
    reverseNode = str(labels[0]) + '_reverse'
    
else:
    reverseNode = cmd.shadingNode('reverse', asUtility = 1, n = str(labels[0]) + '_reverse')

print('reverseNode = ' + str(reverseNode))


#connect attributes
#set the visibility of ctrls according to switch
FKvis = str(labels[0]) + 'FK_01_GRP', baseFK
print('FKvis = ' + str(FKvis))


IKvis = PVorig1, IKorig1, baseIK
print('IKvis = ' + str(IKvis))

#switch into reverse
cmd.connectAttr(switchCtrl[0] + '.SwitchIKFK', reverseNode + '.inputX', f = 1)

#connect switch into FKvis
for item in FKvis:
    output = switchCtrl[0] + '.SwitchIKFK'
    input = item + '.v'
    
    print(output + ' connected to ' + input)
    
    cmd.connectAttr(output, input, f = 1)


#connect reverse into IKvis
for item in IKvis:
    output = reverseNode + '.outputX'
    input = item + '.v'
    
    print(output + ' into ' + input)
    
    cmd.connectAttr(output, input, f = 1)

#Lock controllers' scale and vis attributes
lockCTRL = [item + 'FK_01_CTRL' for item in labels]
lockCTRL.append(IKctrl[0])

lockAttr = [".sx", ".sy", ".sz", ".v"]

print(lockCTRL + lockAttr)

for ctrl in lockCTRL:
    for attr in lockAttr:
        print(ctrl + attr)
        cmd.setAttr(ctrl + attr, lock = 1, keyable = 0, channelBox = 0)


#Lock PV's rotate attributes also
lockPV = ['.rx', '.ry', '.rz']
lockPV.extend(lockAttr)

print(PVctrl + lockPV)

for attr in lockPV:
    cmd.setAttr(PVctrl[0] + attr, lock = 1, keyable = 0, channelBox = 0)


#Stretch and squash
if stretchy:
    #Create attribute
    cmd.select(IKctrl[0], r = 1)
    cmd.addAttr(longName='Stretch', keyable = 1, at = 'enum', en = "Stretchy:Compress:Both:None:")
    
    #Create locators
    locA = cmd.spaceLocator(n = labels[0] + "Stretch_01_loc")
    locB = cmd.spaceLocator(n = labels[0] + "Stretch_02_loc")
    
    cmd.pointConstraint(baseJnt, locA)
    cmd.pointConstraint(IKctrl[0], locB)
    
    #Get arm length
    distance = cmd.createNode("distanceBetween", n = labels[0] + "_DBT")
    
    cmd.connectAttr(locA[0] + ".worldMatrix", distance + ".inMatrix1")
    cmd.connectAttr(locB[0] + ".worldMatrix", distance + ".inMatrix2")
    
    armLength = totalLen
    print(armLength)
    
    #MultiplyDivide and Condition nodes
    armMD = cmd.createNode("multiplyDivide", n = labels[0] + "_MD")
    cmd.setAttr(armMD + ".operation", 2)
    
    cmd.connectAttr(distance + ".distance", armMD + ".input1X")
    cmd.setAttr(armMD + ".input2X", armLength)
    
    cond = cmd.createNode("condition", n = labels[0] + "_COND")
    
    cmd.setAttr(cond + ".secondTerm", 1.0)
    cmd.connectAttr(armMD + ".outputX", cond + ".colorIfTrueR")
    cmd.connectAttr(armMD + ".outputX", cond + ".firstTerm")
    
    #Create driven keys
    valuesA = [0, 1, 2, 3]
    valuesB = [3, 5, 1, 0]
    
    for (valueA, valueB) in zip(valuesA, valuesB):
        cmd.setAttr(IKctrl[0] + ".Stretch", valueA)
        cmd.setAttr(cond + ".operation", valueB)
        
        cmd.setDrivenKeyframe(cond + ".operation" , cd = IKctrl[0] + ".Stretch")
    
    #get scale attr to connect to
    for item in IKchain:
        if normals == [1, 0, 0]:
            print(normals)
            cmd.connectAttr(cond + ".outColorR", item + ".scaleX")
            
        if normals == [0, 1, 0]:
            print(normals)
            cmd.connectAttr(cond + ".outColorR", item + ".scaleY")
            
        if normals == [0, 0, 1]:
            print(normals)
            cmd.connectAttr(cond + ".outColorR", item + ".scaleZ")

#Create Offset CTRLs
if offset:
    offsetCtrl = []
    offsetOrig1 = []
    offsetOrig2 = []
    
    for jnt in driverJnt:
        ctrl = cmd.circle(n = labels[driverJnt.index(jnt)] + "Offset_01_CTRL", r = 8, nr = (normals), d = 1, s = 8)
        offsetCtrl.append(ctrl)
        
        cmd.setAttr(ctrl[0] + '.overrideEnabled', 1)
        cmd.setAttr(ctrl[0] + '.overrideColor', ctlColor)
        
        orig1 = cmd.group(n = labels[driverJnt.index(jnt)] + "Offset_01_GRP")
        offsetOrig1.append(orig1)
    
    print(offsetCtrl)
    print(offsetOrig1)
    
    for (orig, ctrl) in zip(offsetOrig1[0:2], offsetCtrl):
        cmd.select(cl = 1)
        orig2 = cmd.group(n = labels[offsetOrig1.index(orig)] + "Offset_02_GRP", em = 1)
        
        cmd.parent(ctrl, orig2)
        cmd.parent(orig2, orig)
        
        offsetOrig2.append(orig2)
    
    print(offsetOrig2)
    
    for (orig, jnt) in zip(offsetOrig1, driverJnt):
        cmd.parentConstraint(jnt, orig, mo = 0)
