import maya.cmds as cmd
from importlib import reload

# Creates joint chain along a curve

class AutoJointChainAfterCurveUI:
    selection = cmd.ls(sl = 1)
    curve = 'None'

    def __init__(self):
        self.winID = 'Please_select_a_curve'
        self.default_quantity = 5
        self.row_height = 24
        self.column_width_1 = 60
        self.list_height = 100
        self.uv_values1 = [0.93, 0.806, 0.642, 0.472, 0.322, 0.195, 0.092]
        self.uv_values2 = [0.93, 0.672, 0.432, 0.2, 0.092]
        self.uv_values3 = [0.07, 0.328, 0.568, 0.8, 0.908]
        self.build_ui()


    def update_selection(self):
        AutoJointChainAfterCurveUI.selection = cmd.ls(sl = 1)


    def update_targets(self):
        self.update_selection()

        if len(AutoJointChainAfterCurveUI.selection) > 0:
            if cmd.listRelatives(AutoJointChainAfterCurveUI.selection[0]):
                if cmd.objectType(cmd.listRelatives(AutoJointChainAfterCurveUI.selection[0])) == 'nurbsCurve':
                    AutoJointChainAfterCurveUI.curve = AutoJointChainAfterCurveUI.selection[0]
                else : AutoJointChainAfterCurveUI.curve = 'Not a curve'
        else:
            AutoJointChainAfterCurveUI.curve = 'None'
        
        cmd.text('curve_label', e = 1, label = 'Curve : ' + AutoJointChainAfterCurveUI.curve)


    def naming_joints(self):
        
        joint_names = []
        
        if self.name:
            i = 0
            while i < self.quantity:
                i = i + 1
                
                id = f'{i:02}'
                
                name_parts = [self.side, self.name, id]
                
                if self.suffix:
                    name_parts.append(self.suffix)
                
                joint_name = '_'.join(name_parts)
                
                joint_names.append(joint_name)
        
        return joint_names


    def get_uv_values(self, quantity):
        uv_values = []
        
        def maths(x, a = 0.7, h = 1, k = 0.1):
            result = a * (pow(x - h, 2)) + k
            return result
        
        steps = 1.0 / (quantity - 1)
        perc = 0
        
        print(steps)

        for i in range(quantity):
            print(i + 1, maths(perc), perc)
            uv_values.append(maths(perc))
            perc += steps
        
        return(uv_values)

    def deleteConnection(self, plug):
        if cmd.connectionInfo(plug, isDestination=True):
            plug = cmd.connectionInfo(plug, getExactDestination=True)
            readOnly = cmd.ls(plug, ro=True)
            #delete -icn doesn't work if destination attr is readOnly 
            if readOnly:
                source = cmd.connectionInfo(plug, sourceFromDestination=True)
                cmd.disconnectAttr(source, plug)
            else:
                cmd.delete(plug, icn=True)


    def create_joints_on_curve(self, curve):
        quantity = cmd.intSliderGrp('joint_quantity', q = 1, field = 1, value = 1)
        uv_values = self.uv_values3

        joints = []

        for i in range(quantity):
            # print('_'.join(AutoJointChainAfterCurveUI.curve.split('_')[:-1]) + '_' + str(i))
            
            cmd.select(cl = 1)
            joint = cmd.joint(n = '_'.join(curve.split('_')[:-1]) + '_' + str(i + 1), r = 0)
            joints.append(joint)
        
        for joint, uv_value in zip(joints, uv_values):
            print(joint, uv_value)
            motion_path = cmd.pathAnimation(joint, curve, fm = 1)
            cmd.cutKey(motion_path, cl = 1, at = "u")
            cmd.setAttr(motion_path + '.uValue', uv_value)

            for i in (".tx", ".ty", ".tz"):
                self.deleteConnection(joint + i)

            cmd.delete(motion_path)

            if joints.index(joint) == 0 : print('start joint')
            else : cmd.parent(joint, joints[joints.index(joint) - 1])

            cmd.setAttr(joint + ".displayLocalAxis", 1)
        
        cmd.select(joints[0], r = 1)
        cmd.joint(e = 1, oj = "xzy", secondaryAxisOrient = "ydown", ch = 1, zso = 1)

        last_joint_attributes = ["rx", "ry", "rz", "jointOrientX", "jointOrientY", "jointOrientZ"]
        for attribute in last_joint_attributes:
            if(cmd.getAttr(joints[-1] + "." + attribute, se = 1)):
                cmd.setAttr(joints[-1] + "." + attribute, 0)
        
        cmd.select(joints, r = 1)

        if cmd.checkBoxGrp('auto_ctrl', q = 1, value1 = 1):
            import autoCTRL_Leandre
            reload(autoCTRL_Leandre)
            


    def build_ui(self):
        if cmd.window(self.winID, exists = 1):
            cmd.deleteUI(self.winID)
        cmd.window(self.winID, s = 0, rtf = 1)

        #Fenêtre
        cmd.columnLayout()
        cmd.rowLayout(nc = 1, h = self.row_height)
        cmd.text('curve_label', l = 'Curve :', h = self.row_height)
        cmd.setParent('..')
        
        # Quantité
        cmd.rowLayout(nc = 1, h = self.row_height)
        cmd.intSliderGrp('joint_quantity', l = 'Quantité', columnWidth3 = (self.column_width_1, 50, 183), field = 1, value = self.default_quantity, min = 1, max = 99)
        cmd.setParent('..')

        # Faire les controlleurs?
        cmd.rowLayout(nc = 1, h = self.row_height)
        cmd.checkBoxGrp('auto_ctrl', numberOfCheckBoxes = 1, l = 'CTRLS', value1 = 1, columnWidth2 = (self.column_width_1, 150))
        cmd.setParent('..')

        # Button
        cmd.button(label = 'Create joints on curve!', h = 32, w = self.column_width_1 + 50 + 183, c = lambda x : self.create_joints_on_curve(AutoJointChainAfterCurveUI.curve))
        cmd.setParent('..')

        # Draw window
        cmd.showWindow()

        # ScriptJobs
        cmd.scriptJob(e = ['SelectionChanged', self.update_targets], p = self.winID)


AutoJointChainAfterCurveUI()