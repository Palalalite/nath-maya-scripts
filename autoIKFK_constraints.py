import maya.cmds as cmd

print('--------------------------------------IKFK Start!--------------------------------------')

#user variables
IKlabel = 'Pied' # inscrire 'Main' ou 'Pied'


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
    newItem = item.split('_') #ex : we get [G, bras, jnt]
    labels[labels.index(item)] = '_'.join(newItem[0:2]) #ex : keep 'G_Bras'

print('labels = ' + str(labels))

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
switchTranslate = translatesRaw[translatesAbs.index(max(translatesAbs))] * 1.2

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
    newItem = cmd.rename(item, labels[IKchain.index(item)] + '_IK' + '_jnt')
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
PVctrl = cmd.circle(n = labels[0] + '_PV_CTRL' , r = 5, nr = (orientVector))
cmd.delete(ch = 1) #delete history
print('PVctrl = ' + str(PVctrl))
PVorig = cmd.group(n = PVctrl[0] + '_Orig')


#place PV Orig at elbow and offset it
cmd.pointConstraint(midIK, PVorig, mo = 0)
cmd.orientConstraint(midIK, PVorig, mo = 0)
cmd.delete(PVorig, cn = 1)

cmd.move(translates[0], translates[1], translates[2], r = 1, os = 1, wd = 1)


#create PV constraint
cmd.poleVectorConstraint(PVctrl[0], ikHand[0], w = 1)


#create IK ctrl
#cmd.file('controllers/cube.fbx', i = True)
#cmd.select('Cube_CTRL', r = 1)
#IKctrl = cmd.ls(sl = 1)
IKctrl = cmd.circle(n = str(labels[0]) + '_IK_CTRL' , r = 8, nr = (normals), d = 1, s = 4)
cmd.delete(ch = 1)
print('IKctrl = ' + str(IKctrl))

#cmd.setAttr(IKctrl[0] + '.scaleX', cmd.getAttr(baseIK + '.radius') * 0.25)
#cmd.setAttr(IKctrl[0] + '.scaleY', cmd.getAttr(baseIK + '.radius') * 0.25)
#cmd.setAttr(IKctrl[0] + '.scaleZ', cmd.getAttr(baseIK + '.radius') * 0.25)
#cmd.makeIdentity(apply=True, t=1, r=1, s=1, n=2)

#IKctrl = cmd.rename(IKctrl, str(labels[0]) + '_IK_CTRL')
#IKctrl = cmd.rename(IKctrl, str(labels[0])[0:2] + IKlabel + '_IK_CTRL')

IKorig = cmd.group(n = str(IKctrl[0]) + '_Orig')

cmd.pointConstraint(endIK, IKorig, mo = 0)
cmd.orientConstraint(endIK, IKorig, mo = 0)

cmd.delete(IKorig, cn = 1)


#parent only the ikHandle under IK ctrl and hide it
cmd.parent(ikHand[0], IKctrl[0]) 
cmd.setAttr(ikHand[0] + '.v', 0)


#color the ctrls
for item in PVctrl[0], IKctrl[0]:
    cmd.setAttr(item + '.overrideEnabled', 1)
    cmd.setAttr(item + '.overrideColor', 13)


#end of IK part.


#duplicate FK
cmd.select(baseJnt, midJnt, endJnt, r = 1)

FKchain = cmd.duplicate(po = 1, rc = 1) #children are duplicated too

print('FKchain (old) = ' + str(FKchain))


#rename the FKchain and update the list
#if having trouble with getting indexes of lists from item names in loops...
#please check this https://www.dataquest.io/blog/tutorial-advanced-for-loops-python-pandas/
for item in FKchain:
    newItem = cmd.rename(item, labels[FKchain.index(item)] + '_FK' + '_jnt')
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
    ctrl = cmd.circle(n = str(labels[FKchain.index(item)]) + '_FK_CTRL' , r = 7, nr = (switchNormals))
    cmd.delete(ch = 1)
    orig = cmd.group(n = ctrl[0] + '_Orig')
    
    cmd.setAttr(ctrl[0] + '.overrideEnabled', 1)
    cmd.setAttr(ctrl[0] + '.overrideColor', 6)
    
    print('ctrl = ' + str(ctrl))
    
    cmd.pointConstraint(item, orig, mo = 0)
    cmd.orientConstraint(item, orig, mo = 0)
    
    cmd.delete(orig, cn = 1)
    
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
            parentCtrl = str(labels[FKchain.index(item) - 1]) + '_FK_CTRL'
            print('parentCtrl = ' + parentCtrl)
            
            cmd.parent(childOrig, parentCtrl)

#end of FK part.


#create IKFK switch
switchCtrl = cmd.circle(n = labels[0] + '_Switch_CTRL' , r = 3, nr = (orientVector))

cmd.setAttr(switchCtrl[0] + '.overrideEnabled', 1)
cmd.setAttr(switchCtrl[0] + '.overrideColor', 14)
cmd.setAttr(switchCtrl[0] + '.scaleX', 0.8)
cmd.setAttr(switchCtrl[0] + '.scaleY', 0.8)
cmd.setAttr(switchCtrl[0] + '.scaleZ', 0.8)
cmd.select(switchCtrl[0], r = 1)
cmd.makeIdentity(apply=True, t=1, r=1, s=1, n=2)
cmd.delete(ch = 1)

switchOrig = cmd.group(n = switchCtrl[0] + '_Orig')
print('switchCtrl = ' + str(switchCtrl))


#constrain it to endJnt
cmd.parentConstraint(endJnt, switchOrig, mo = 0, sr = 'none', st = 'none')


#select switchCtrl control vertices and translate along Z axis
cmd.select(switchCtrl[0] + '.cv[:]', r = 1)
cmd.move(switchTranslate, x = switchNormals[0], y = switchNormals[1], z = switchNormals[2], r = 1, os = 1, wd = 1)


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


#create the parent constraints for the joints (target1, target2, object, maintainOffset = ...)
baseConstraint = cmd.parentConstraint(baseIK, baseFK, baseJnt, mo = 0)
midConstraint = cmd.parentConstraint(midIK, midFK, midJnt, mo = 0)
endConstraint = cmd.parentConstraint(endIK, endFK, endJnt, mo = 0)

allConstraints = baseConstraint + midConstraint + endConstraint
print('allConstraints = ' + str(allConstraints))


#create the reverse node, if it doesn't exists
if cmd.objExists(str(labels[0]) + '_reverse'):
    reverseNode = str(labels[0]) + '_reverse'
    
else:
    reverseNode = cmd.shadingNode('reverse', asUtility = 1, n = str(labels[0]) + '_reverse')

print('reverseNode = ' + str(reverseNode))


#connect attributes
#switch into FK constraints
for item in allConstraints:
    output = switchCtrl[0] + '.SwitchIKFK'
    input = item + '.' + FKchain[allConstraints.index(item)] + 'W1'
    
    print(output + ' connected to ' + input)
    
    cmd.connectAttr(output, input, f = 1)


#switch into reverse
cmd.connectAttr(switchCtrl[0] + '.SwitchIKFK', reverseNode + '.inputX', f = 1)


#reverse into IK constraints
for item in allConstraints:
    output = reverseNode + '.outputX'
    input = item + '.' + IKchain[allConstraints.index(item)] + 'W0'
    
    print(output + ' connected to ' + input)
    
    cmd.connectAttr(output, input, f = 1)


#set the visibility of ctrls according to switch
FKvis = str(labels[0]) + '_FK_CTRL_Orig', baseFK
print('FKvis = ' + str(FKvis))

IKvis = PVorig, IKorig, baseIK
print('IKvis = ' + str(IKvis))


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