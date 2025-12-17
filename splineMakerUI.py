import maya.cmds as cmd

class SplineMaker:
    selection = cmd.ls(sl = 1)
    start_joint = ''
    end_joint = ''


    def __init__(self):
        self.winID = "SplineMaker"
        self.row_height = 24

        self.build_ui()
    

    def update_selection(self):
        SplineMaker.selection = cmd.ls(sl = 1)


    def update_targets(self):
        self.update_selection()

        if len(SplineMaker.selection) > 0:
            SplineMaker.start_joint = SplineMaker.selection[0]
        else:
            SplineMaker.start_joint = 'None'

        if len(SplineMaker.selection) > 1:
            SplineMaker.end_joint = SplineMaker.selection[1]
        else:
            SplineMaker.end_joint = 'None'
        
        cmd.text('start_joint', e = 1, label = 'From... ' + SplineMaker.start_joint, h = self.row_height)
        cmd.text('end_joint', e = 1, label = 'To... ' + SplineMaker.end_joint, h = self.row_height)


    def create_spline(self):
        selection = SplineMaker.selection
        upperJnt = SplineMaker.start_joint
        lowerJnt = SplineMaker.end_joint
        chainSize = cmd.intSliderGrp('joint_quantity', q = 1, field = 1, value = 1)

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

        for i in range(chainSize):
            spJnt = cmd.createNode('joint', n = label[1] + '_spline_' + f'{i + 1:02}')
            
            if i == 0:
                cmd.parentConstraint(upperJnt, spJnt, weight = 1.0 - perc, st = 'none', sr = 'none', mo = 0)[0]  # Apply 1st constraint, with inverse of current percentage.
                
            elif i > 0:
                cmd.pointConstraint(upperJnt, spJnt, weight = 1.0 - perc, mo = 0)[0]  # Apply 1st constraint, with inverse of current percentage.
                cmd.pointConstraint(lowerJnt, spJnt, weight = perc, mo = 0) 
                cmd.orientConstraint(upperJnt, spJnt, weight = 1.0, mo = 0) # Apply 2nd constraint, with current percentage as-is.
            
            cmd.delete(spJnt, cn = 1)  # Don't need this anymore.

            perc += steps  # Increase percentage for next iteration.
            if splineJnts:
                cmd.parent(spJnt, splineJnts[-1])
            splineJnts.append(spJnt)
        
        cmd.makeIdentity(splineJnts[0], apply = 1, t = 1, r = 1, s = 1, n = 0, pn = 1)
        print(splineJnts)

        #create ikSpline
        ikSpline = cmd.ikHandle(sj = splineJnts[0], ee = splineJnts[-1], sol = 'ikSplineSolver', n = label[1] + '_ikSpline', roc = 1, pcv = 1, ccv = 1, scv = 1, ns = 1, tws = 'linear')
        cmd.rename(ikSpline[1], label[1] + '_effector')
        spCurve = cmd.rename(ikSpline[2], label[1] + '_spCurve')

        #get create curveInfo
        if cmd.objExists(label[1] + '_curveInfo'):
            curveInfoNode = label[1] + '_curveInfo'
            
        else:
            curveInfoNode = cmd.arclen(spCurve, ch = 1, nds = 1)
            curveInfoNode = cmd.rename(curveInfoNode, label[1] + '_curveInfo')

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
        for item, i in zip(spClusters, range(len(spClusters))):
            cmd.select(cl = 1)
            ctrl = cmd.circle(n = label[1] + '_bendy_' + str(i + 1) + '_ctrl', r = 5, nr = (1, 0, 0))
            cmd.setAttr(ctrl[0] + '.overrideEnabled', 1)
            cmd.setAttr(ctrl[0] + '.overrideColor', 18)
            spCtrl.append(ctrl)
        print(spCtrl)

        # #create locators and parent them under CTRLs, for twist stuff
        # locUp = cmd.spaceLocator(n = label[1] + '_locUp')
        # cmd.parent(locUp, spCtrl[0])
        # locLo = cmd.spaceLocator(n = label[1] + '_locLo')
        # cmd.parent(locLo, spCtrl[2])

        #create orig for each ctrl
        spOrig = []
        for item in spCtrl:
            cmd.select(item, r = 1)
            orig = cmd.group(n = item[0] + '_offset')
            spOrig.append(orig)
        print(spOrig)

        #place the orig at the clusters and orient them according to joints
        for item in spOrig:
            cmd.pointConstraint(spClusters[spOrig.index(item)], item, mo = 0)
            cmd.orientConstraint(upperJnt, item, mo = 0)
            cmd.delete(item, cn = 1)
            cmd.parent(spClusters[spOrig.index(item)], spCtrl[spOrig.index(item)][0])

        #get base distance between upper and lower joints.
        defDistBase = cmd.getAttr(curveInfoNode + '.arcLength')
        print(defDistBase)

        #multiply node stuff
        spline_div = cmd.createNode('multiplyDivide', n = label[1] + '_spline_md')
        cmd.setAttr(spline_div + '.operation', 2)
        cmd.setAttr(spline_div + '.input2X', defDistBase)
        cmd.connectAttr(curveInfoNode + '.arcLength', spline_div + '.input1X', f = 1)

        for joint in splineJnts:
            cmd.connectAttr(spline_div + '.outputX', joint + '.scaleX')

        # spline_pow = cmd.createNode('multiplyDivide', n = label[1] + '_spline_pow')
        # cmd.setattr(spline_pow + '.input1Y', defDistBase)

        # Twist setup
        cmd.setAttr(ikSpline[0] + '.dTwistControlEnable', 1)
        cmd.setAttr(ikSpline[0] + '.dWorldUpType', 4)
        cmd.connectAttr(spCtrl[0][0] + '.worldMatrix[0]', ikSpline[0] + '.dWorldUpMatrix')
        cmd.connectAttr(spCtrl[2][0] + '.worldMatrix[0]', ikSpline[0] + '.dWorldUpMatrixEnd')

        # # Constraints
        # cmd.parentConstraint(upperJnt, spOrig[0], mo = 0)
        # cmd.pointConstraint(lowerJnt, spOrig[2], mo = 0)
        # cmd.pointConstraint(spCtrl[0], spCtrl[2], spOrig[1], mo = 0)

        

    def build_ui(self):
        if cmd.window(self.winID, exists = 1):
            cmd.deleteUI(self.winID)
        cmd.window(self.winID, s = 0, rtf = 1)

        #Fenêtre
        cmd.columnLayout()
        cmd.rowLayout(nc = 2, cw2 = (175, 175), h = 64)
        cmd.text('start_joint', label = 'From... ', h = self.row_height)
        cmd.text('end_joint', label = 'To... ', h = self.row_height)
        cmd.setParent('..')

        # Nombre joints
        cmd.intSliderGrp('joint_quantity', l = 'Joints', columnWidth3 = (50, 50, 225), field = 1, value = 8, min = 3, max = 20)

        # Copy Shapes button
        cmd.button(label = 'Create spline', h = 32, w = 350, c = lambda x : self.create_spline())
        cmd.setParent('..')

        # Draw window
        cmd.showWindow()

        # ScriptJobs
        cmd.scriptJob(e = ['SelectionChanged', self.update_targets], p = self.winID)


SplineMaker()