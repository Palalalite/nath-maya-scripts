import maya.cmds as cmd
import maya.OpenMaya as om
import random
import string

#user variables
planeEdges = 7
ribbonWidth = 9
userLabel = "test"
customColor = 17
tweaks = 1

#get the two joints
selection = cmd.ls(sl = 1)
jntA = selection[0]
jntB = selection[1]
print (selection)

joints = [jntA, jntB]

#get labels
label = selection[0].split("_") #ex : from G_bras_jnt, get [G, bras, jnt]
label = "_".join(label[0:2]) #ex : keep "G_Bras"

print("label = " + str(label))


#get jointB"s translates for custom plane orienting
translatesRaw = cmd.getAttr(jntB + ".translateX"), cmd.getAttr(jntB + ".translateY"), cmd.getAttr(jntB + ".translateZ") #that gets us a TUPLE, NOT LIST. https://www.w3schools.com/python/python_tuples.asp
print (translatesRaw)


translatesAbs = [abs(translate) for translate in translatesRaw]

print (translatesAbs)

#some variables
normals = [0, 0, 0]
direction = [0, 0, 0]

#if the max value is at index n, then make the corresponding variable true
if translatesAbs.index(max(translatesAbs)) == 0:
    normals[0] = 1
    if translatesRaw[translatesAbs.index(max(translatesAbs))] < 0:
        direction[0] = -1
    else :
        direction[0] = 1

if translatesAbs.index(max(translatesAbs)) == 1:
    normals[1] = 1
    if translatesRaw[translatesAbs.index(max(translatesAbs))] < 0:
        direction[1] = -1
    else :
        direction[1] = 1

if translatesAbs.index(max(translatesAbs)) == 2:
    normals[2] = 1
    if translatesRaw[translatesAbs.index(max(translatesAbs))] < 0:
        direction[2] = -1
    else :
        direction[2] = 1
        
print("normals = " + str(normals))
print("direction = " + str(direction))

#create two locators
locators = []

#new label
newLabel = "_".join(jntA.split("_")[0:3])

#determine color of the ctrls
if "G" in newLabel[0]:
    ctlColor = 6

elif "D" in newLabel[0]:
    ctlColor = 13

else:
    ctlColor = customColor
            
for jnt in joints:
    words = jnt.split("_")
    print(words)
    
    prefix = "_".join(words[0:2])
    print(prefix)
    
    id = int(words[2])
    print(id)
    
    letters = string.ascii_letters
    loc = cmd.spaceLocator (n = ''.join(random.choice(letters) for i in range(10)))
    
    cmd.matchTransform(loc, jnt)
    
    newName = str(prefix) + "_0" + str(id) + "_loc"
    
    
    while cmd.objExists(newName) == 1: #while this name exists...
        id = id + 1 #increment id
        newName = str(prefix) + "_0" + str(id) + "_loc"
        
        if cmd.objExists(newName) == 0: #when name doesn't exists...
            break
    
    cmd.rename(loc, newName)
    
    loc = newName
    
    print(loc)
    
    locators.append(loc)
    

locA = locators[0]
locB = locators[1]

cmd.aimConstraint(locA, locB, aimVector = (1, 0, 0), upVector = (0, -1, 0), worldUpType = "objectrotation", worldUpVector = (0, -1, 0), worldUpObject = jntA)
cmd.aimConstraint(locB, locA, aimVector = (-1, 0, 0), upVector = (0, -1, 0), worldUpType = "objectrotation", worldUpVector = (0, -1, 0), worldUpObject = jntA)

#get distance between the two locators
posLocA = cmd.xform(locA, q = 1, ws = 1, t = 1)
posLocB = cmd.xform(locB, q = 1, ws = 1, t = 1)
vecLocA = om.MVector(posLocA[0], posLocA[1], posLocA[2])
vecLocB = om.MVector(posLocB[0], posLocB[1], posLocB[2])

distance = (vecLocB - vecLocA).length()

print(distance)
#distance = cmd.distanceDimension(locA, locB)


#create the plane with determined dimensions
width = distance
height = ribbonWidth
planeBase = cmd.polyPlane(n = label + "_planeTemp", h = height, w = width, sh = 1, sw = planeEdges)

#constraint the plane to the joints, according to determined joint direction
cmd.select(jntA, r = 1)
cmd.select(jntB, add = 1)
cmd.select(planeBase, add = 1)
cmd.pointConstraint(mo = 0)
cmd.select(jntB, d = 1)

if normals[0]:
    cmd.orientConstraint(o = (-90, 0, 0))
if normals[1]:
    cmd.orientConstraint(o = (-90, 0, -90))
if normals[2]:
    cmd.orientConstraint(o = (-90, 90, 0))

#select the plane"s crossing edges
crossEdges = cmd.polySelect(planeBase, er = 3)
print (crossEdges)

#select border edges starting from first cross edge
borderEdges = cmd.polySelect(planeBase, elb = crossEdges[0])
print (borderEdges)

#get the long edges, by substracting border edges by cross edges
longEdges = [edge for edge in borderEdges if edge not in crossEdges]
print (longEdges)

#get middle of the array"s ID
middleID = int(len(longEdges) / 2)
print (middleID)

#split the long edges list in two new lists
firstEdge = longEdges[:middleID]
secondEdge = longEdges[middleID:]

print (firstEdge)
print (secondEdge)

#reverse the second edge
secondEdge.reverse()
print(secondEdge)

#we have the first and the second edge

#select plane, then first edge, then deselect plane
cmd.select(planeBase, r = 1)
cmd.polySelect(ebp = (firstEdge[0],firstEdge[-1]), r = 1)
cmd.select(planeBase, d = 1)

#make the first curve
curveA = cmd.polyToCurve(n = jntA + "_curveA")

#select plane, then second edge, then deselect plane
cmd.select(planeBase, r = 1)
cmd.polySelect(ebp = (secondEdge[0],secondEdge[-1]), r = 1)
cmd.select(planeBase, d = 1)

#make the second curve
curveB = cmd.polyToCurve(n = label + "_curveB")

#make the ribbon
ribbon = cmd.loft(curveA, curveB, n = jntA[:-4] + "_loft", ch = 1, u = 1, c = 0, ar = 0, d = 3, ss = 1, rn = 0, po = 0, rsn = 1)
cmd.hide(planeBase[0])

#create hairSystem on the ribbon
#set the follicles quantity variable and select the ribbon
hairQty = len(crossEdges)

cmd.select(ribbon, r = 1)

#create a group for the follicles
follicleGrp = cmd.group(n = label + "Follicles_01_GRP", em = 1)

#for each follicle...
#reference https://stackoverflow.com/a/63878115
for i in range(hairQty):
    #create the follicle
    cmd.createNode("follicle")
    cmd.pickWalk(d = "up") #get the follicle shape node
    
    #rename ans parent under folli grp
    follicle = cmd.rename(label + "Follicle_0" + str(i) + "_fol")
    cmd.parent(follicle, follicleGrp)
    
    #what makes the follicle attach to the nurbsSurface
    cmd.setAttr(follicle + ".simulationMethod", 0)
    cmd.makeIdentity(ribbon, apply = True, t = 1, r = 1, s = 1, n = 0)
    
    cmd.connectAttr(follicle + ".outRotate", follicle + ".rotate", f = True)
    cmd.connectAttr(follicle + ".outTranslate", follicle + ".translate")
    cmd.connectAttr(ribbon[0] + ".worldMatrix", follicle + ".inputWorldMatrix")
    cmd.connectAttr(ribbon[0] + ".local", follicle + ".inputSurface")
    
    cmd.setAttr(follicle + ".parameterV", 0.5)
    cmd.setAttr(follicle + ".parameterU", float(i) / (hairQty - 1))
    
    if tweaks:
        tweak = cmd.circle(n = label + "Tweak_0" + str(i) + "_CTRL", r = 2.6, s = 4, nr = (1,0,0), degree = 1)
        cmd.parent(tweak, follicle, r = 1)
    
    #create joint under follicle
    cmd.joint(n = label + "Follicle_0" + str(i) + "_jnt", r = 0.8)

#delete junk and select ribbon
cmd.delete(planeBase, curveA, curveB)

#cmd.select(ribbon[0], r = 1)

#for bendies, create three joints
bendyJnt = []

for item in range(3):
    cmd.select(cl = 1)
    item = cmd.joint(n = label + "Bendy_0" + str(item + 1) + "_jnt")
    cmd.setAttr(item + ".radius", 4)
    print("item = " + str(item))
    bendyJnt.append(item)
    
print("bendyJnt = " + str(bendyJnt))


#then create their controllers
bendyCtrl = []
for item in bendyJnt:
    ctrl = cmd.circle(n = label + "Bendy_0" + str(bendyJnt.index(item) + 1) + "_CTRL", r = 6, nr = (1,0,0))
    cmd.setAttr(ctrl[0] + ".overrideEnabled", 1)
    cmd.setAttr(ctrl[0] + ".overrideColor", 17)
    cmd.delete(ctrl, ch = 1)
    cmd.parent(item, ctrl[0])
    bendyCtrl.append(ctrl[0])
    
print("bendyCtrl = " + str(bendyCtrl))


#create two offsets for each ctrl
offset1 = []
offset2 = []

for (item, i) in zip(bendyCtrl, range(4,7)):
    cmd.select(item, r = 1)
    orig2 = cmd.group(n = label + "Bendy_0" + str(i) + "_GRP")
    
    offset2.append(orig2)
    
for (item, i) in zip(offset2, range(1,4)):
    cmd.select(item, r = 1)
    orig1 = cmd.group(n = label + "Bendy_0" + str(i) + "_GRP")
    
    offset1.append(orig1)

print("offset1 = " + str(offset1))    
print("offset2 = " + str(offset2))


#place the bendies at the ribbon
cmd.parentConstraint(locA, offset1[0], mo = 0)
cmd.parentConstraint(locB, offset1[2], mo = 0)
cmd.pointConstraint(bendyCtrl[0], bendyCtrl[2], offset1[1], mo = 0)
cmd.aimConstraint(bendyCtrl[0], offset1[1], aimVector = (1, 0, 0), upVector = (0, -1, 0), worldUpType = "objectrotation", worldUpVector = (0, -1, 0), worldUpObject = bendyCtrl[0])



#skin the ribbon to the bendys
cmd.select(bendyJnt, ribbon[0], r = 1)
bendySkin = cmd.skinCluster(mi = 2)
print(bendySkin)

