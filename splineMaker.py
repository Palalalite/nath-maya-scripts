import maya.cmds as cmd

#user variables
chainSize = 8

#get selection
selection = cmd.ls(sl = 1)

upperJnt = selection[0]
lowerJnt = selection[1]

print(selection)

#get labels
label = []

for item in selection:
    newLabel = item.split('_') #ex : from G_bras_jnt, get [G, bras, jnt]
    item = '_'.join(newLabel[0:2]) #ex : keep 'G_Bras'
    print(item)
    label.append(item)

print(label)


#create joints in-between https://stackoverflow.com/questions/60539638/maya-python-create-equidistant-joint-chain-between-locators
steps = 1.0 / (chainSize - 1)  # Will use count to calculate how much it should increase percentage by each iteration. Need to do -1 so the joints reach both start and end points.
perc = 0  # This will always go between a range of 0.0 - 1.0, and we'll use this in the constraint's weights.

splineJnts = []

for item in range(chainSize):
    spJnt = cmd.createNode('joint', n = label[1] + '_jnt_spline_00')
    
    constraint = cmd.parentConstraint(upperJnt, spJnt, weight=1.0 - perc, st = 'none', sr = 'none')[0]  # Apply 1st constraint, with inverse of current percentage.
    cmd.parentConstraint(lowerJnt, spJnt, weight=perc, sr = ['x', 'y', 'z'])  # Apply 2nd constraint, with current percentage as-is.
    cmd.delete(constraint)  # Don't need this anymore.

    perc += steps  # Increase percentage for next iteration.
    if splineJnts:
        cmd.parent(spJnt, splineJnts[-1])
    splineJnts.append(spJnt)

print(splineJnts)


#create ikSpline
ikSpline = cmd.ikHandle(sj = splineJnts[0], ee = splineJnts[-1], sol = 'ikSplineSolver', n = label[1] + '_ikSpline', roc = 1, pcv = 1, ccv = 1, scv = 1, ns = 1, tws = 'linear')
cmd.rename(ikSpline[1], label[1] + '_effector')
spCurve = cmd.rename(ikSpline[2], label[1] + '_spCurve')


#get create curveInfo
if cmd.objExists(label[1] + '_curveInfo'):
    curveInfoNode = label[1] + '_curveInfo'
    
else:
    curveInfoNode = cmd.arclen(spCurve, ch = 1)
    cmd.rename(curveInfoNode, label[1] + '_curveInfo')

print(curveInfoNode)


#create clusters
cmd.select(spCurve + '.cv[0]', r = 1)
clustUp = cmd.cluster(n = label[1] + '_cluster0')

cmd.select(spCurve + '.cv[1:2]', r = 1)
clustMid = cmd.cluster(n = label[1] + '_cluster1')

cmd.select(spCurve + '.cv[3]', r = 1)
clustLow = cmd.cluster(n = label[1] + '_cluster2')

spClusters = [clustUp, clustMid, clustLow]


#create controllers for each
spCtrl = []
for item in spClusters:
    cmd.select(cl = 1)
    ctrl = cmd.circle(n = label[1] + '_bendy_ctrl_0', r = 5, nr = (1, 0, 0))
    cmd.setAttr(ctrl[0] + '.overrideEnabled', 1)
    cmd.setAttr(ctrl[0] + '.overrideColor', 17)
    spCtrl.append(ctrl)
print(spCtrl)


#create locators and parent them under CTRLs, for twist stuff
locUp = cmd.spaceLocator(n = label[1] + '_locUp')
cmd.parent(locUp, spCtrl[0])
locLo = cmd.spaceLocator(n = label[1] + '_locLo')
cmd.parent(locLo, spCtrl[2])


#create orig for each ctrl
spOrig = []
for item in spCtrl:
    cmd.select(item, r = 1)
    orig = cmd.group(n = item[0] + '_orig')
    spOrig.append(orig)
print(spOrig)


#place the orig at the clusters and orient them according to joints
for item in spOrig:
    cmd.pointConstraint(spClusters[spOrig.index(item)], item, mo = 0)
    cmd.orientConstraint(upperJnt, item, mo = 0)
    cmd.delete(item, cn = 1)
    cmd.parent(spClusters[spOrig.index(item)], spCtrl[spOrig.index(item)][0])


#set ikSpline attributes
cmd.setAttr(ikSpline[0] + '.dTwistControlEnable', 1)
cmd.setAttr(ikSpline[0] + '.dWorldUpType', 4)

#get base distance between upper and lower joints.
defDistBase = cmd.getAttr(label[1] + '_curveInfo' + '.arcLength')
print(defDistBase)

#multiply node stuff
