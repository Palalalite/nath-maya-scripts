# -*- coding: utf-8 -*-
# Joint maker v0.1 WIP
import maya.cmds as cmd

# faire fonctinon rotate la chaine de joint forward et front
# changer la logique des fonctions

class JointChainMaker:
    def __init__(self):
        self.winID = 'JointMaker'
        self.column_width_1 = 60
        self.row_height = 26
        self.side_labels = {'aucun' : '',
                            'Centre' : 'C',
                            'Gauche' : 'G',
                            'Droite' : 'D',
                            'center' : 'c',
                            'left' : 'l',
                            'right' : 'r'}
        self.axes = ['X +', 'X -', 'Y +', 'Y -', 'Z +', 'Z -']
        self.default_suffix = "jnt"
        self.default_distance = 5

        self.build_ui()


    # Functions
    def side_labels_list(self):
        for label in self.side_labels:
            cmd.menuItem(label = label)


    def update_side(self):
        side = cmd.optionMenu('joint_side', q = 1, value = 1)
        print(self.side_labels[side])
        return self.side_labels[side]


    def axes_list(self):
        for axis in self.axes:
            cmd.menuItem(label = axis)


    def update_direction(self):
        direction_choice = cmd.radioButtonGrp('joint_direction', q = 1, sl = 1)
        direction = [0, 0, 0]
        
        if direction_choice == 1:
            direction[0] = 1
        
        elif direction_choice == 2:
            direction[1] = 1
            
        elif direction_choice == 3:
            direction[2] = 1
        
        return direction


    def update_distance(self):
        distance = cmd.floatFieldGrp('joint_translate', q = 1, value1 = 1)
        return distance


    def naming_joints(self):
        side = self.update_side()
        name = cmd.textFieldGrp('joint_label', q = 1, text = 1)
        quantity = cmd.intSliderGrp('joint_quantity', q = 1, field = 1, value = 1)
        suffix = cmd.textFieldGrp('joint_suffix', q = 1, text = 1)
        
        joint_names = []
        
        if name:
            i = 0
            while i < quantity:
                i = i + 1
                
                id = f'{i:02}'
                
                name_parts = [name, id]
                
                if side:
                    name_parts.insert(0, side)
                
                if suffix:
                    name_parts.append(suffix)
                
                joint_name = '_'.join(name_parts)
                
                joint_names.append(joint_name)
        
        return joint_names


    def create_joints(self):
        joints = self.naming_joints()

        radius = cmd.floatFieldGrp('joint_radius', q = 1, value1 = 1)
        print(joints)
        direction = self.update_direction()
        distance = self.update_distance()
        
        position_values = [i * distance for i in direction]
        
        cmd.select(cl = 1)
        
        for joint in joints:
            #print("je crée le joint " + joint)
            cmd.joint(n = joint, relative = 1, radius = radius, position = [0, 0, 0] if joints.index(joint) == 0 else position_values)
            
        if not joints:
            print('Please provide a name')

        # cmd.rotate(joints[0], ws = 1, xyz = direction)


    def build_ui(self):
        # Initializing
        if cmd.window (self.winID, q = 1, exists = 1):
            cmd.deleteUI (self.winID, window = 1)

        cmd.window (self.winID, title = self.winID, s = 0, rtf = 0, tlb = 0)

        # Window
        cmd.columnLayout()

        # Côté
        cmd.rowLayout(nc = 2, h = self.row_height)
        cmd.text(label = 'Side', align = 'right', w = self.column_width_1)
        cmd.optionMenu('joint_side')
        self.side_labels_list()
        cmd.setParent('..')

        # Nom
        cmd.rowLayout(nc = 1, h = self.row_height)
        cmd.textFieldGrp('joint_label', label = 'Name', columnWidth2 = (self.column_width_1, 235), text = "")
        cmd.setParent('..')

        # Quantité
        cmd.rowLayout(nc = 1, h = self.row_height)
        cmd.intSliderGrp('joint_quantity', l = 'Quantity', columnWidth3 = (self.column_width_1, 50, 183), field = 1, value = 1, min = 1, max = 99)
        cmd.setParent('..')

        # Suffixe et radius
        cmd.rowLayout(nc = 2, h = self.row_height)
        cmd.textFieldGrp('joint_suffix', label = 'Suffix', columnWidth2 = (self.column_width_1, 83), text = self.default_suffix)
        cmd.floatFieldGrp('joint_radius', label = 'Radius', columnWidth2 = (self.column_width_1, 82), value1 = .5)
        cmd.setParent('..')

        # Direction

        cmd.rowLayout(nc = 4)
        cmd.text(label = 'Up', align = 'right', w = self.column_width_1)
        cmd.optionMenu('world_up')
        self.axes_list()
        cmd.optionMenu('world_up', e = 1, sl = 1)
        cmd.text(label = 'Front', align = 'right', w = self.column_width_1)
        cmd.optionMenu('world_front')
        self.axes_list()
        cmd.optionMenu('world_front', e = 1, sl = 6)
        cmd.setParent('..')

        
        # Distance et tranaslate
        cmd.rowLayout(nc = 2)

        cmd.floatFieldGrp('joint_translate', l = 'Translate', columnWidth2 = (self.column_width_1, 50), value1 = self.default_distance)
        cmd.radioButtonGrp('joint_direction', columnWidth3 = [65, 65, 65], sl = 1, labelArray3 = ['X', 'Y', 'Z'], nrb = 3)
        cmd.setParent('..')

        # Créer les joints
        cmd.rowLayout(nc = 1)
        cmd.button(label = 'Create joints', h = 32, w = 303, command = lambda x : self.create_joints())
        # cmd.button(label = 'Créer joints', h = 32, w = 303, command = lambda x : self.update_side())
        cmd.setParent('..')

        # Draw the window
        cmd.showWindow()

JointChainMaker()