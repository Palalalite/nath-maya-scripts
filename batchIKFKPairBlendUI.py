import maya.cmds as cmd

class BatchPairBlend():
    selection = cmd.ls(sl = 1)
    switch = 'None'
    ik_base = 'None'
    fk_base = 'None'
    skin_base = 'None'


    def __init__(self):
        self.winID = 'BatchPairBlend'
        self.column_width_1 = 60
        self.row_height = 24
    
        self.build_ui()
    
    
    def update_selection(self):
        BatchPairBlend.selection = cmd.ls(sl = 1)


    def update_targets(self):
        self.update_selection()

        if len(BatchPairBlend.selection) > 0:
            BatchPairBlend.switch = BatchPairBlend.selection[0]
            self.attr_into_menu(BatchPairBlend.switch, 'switch_attr')
        else:
            BatchPairBlend.switch = 'None'

        if len(BatchPairBlend.selection) > 1:
            BatchPairBlend.ik_base = BatchPairBlend.selection[1]
        else:
            BatchPairBlend.ik_base = 'None'

        if len(BatchPairBlend.selection) > 2:
            BatchPairBlend.fk_base = BatchPairBlend.selection[2]
        else:
            BatchPairBlend.fk_base = 'None'

        if len(BatchPairBlend.selection) > 3:
            BatchPairBlend.skin_base = BatchPairBlend.selection[3]
        else:
            BatchPairBlend.skin_base = 'None'
        

        cmd.text('switch_label', e = 1, label = 'Switch : ' + BatchPairBlend.switch)
        cmd.text('ik_label', e = 1, label = 'IK chain : ' + BatchPairBlend.ik_base)
        cmd.text('fk_label', e = 1, label = 'FK chain : ' + BatchPairBlend.fk_base)
        cmd.text('skin_label', e = 1, label = 'Skin chain : ' + BatchPairBlend.skin_base)


    def attr_into_menu(self, switch, menu):
        if switch:
            attributes = cmd.listAttr(switch, c = 1)
            for attribute in attributes:
                cmd.menuItem(label = attribute, p = menu)


    def create_pair_blends(self):
        switch = self.switch
        ik_base = self.ik_base
        fk_base = self.fk_base
        skin_base = self.skin_base

        switch_attribute = switch + '.' + cmd.optionMenu('switch_attr', q = 1, value = 1)
        print(switch_attribute)

        def get_chain(joint):
            chain = cmd.listRelatives(joint, ad = 1, type = 'joint')
            chain.append(joint)
            chain.reverse()
            return(chain[:-1])

        ik_chain = get_chain(ik_base)
        fk_chain = get_chain(fk_base)
        skin_chain = get_chain(skin_base)

        for ik_joint, fk_joint, skin_joint in zip (ik_chain, fk_chain, skin_chain):
            if cmd.checkBoxGrp('blend_select', q = 1, value1 = 1):
                pair_blend_node = cmd.createNode('pairBlend', n = skin_joint + '_position_pb')
                cmd.setAttr(pair_blend_node + '.rotInterpolation', 1)

                cmd.connectAttr(switch_attribute, pair_blend_node + '.weight')
                cmd.connectAttr(ik_joint + '.translate', pair_blend_node + '.inTranslate1')
                cmd.connectAttr(ik_joint + '.rotate', pair_blend_node + '.inRotate1')
                cmd.connectAttr(fk_joint + '.translate', pair_blend_node + '.inTranslate2')
                cmd.connectAttr(fk_joint + '.rotate', pair_blend_node + '.inRotate2')
                cmd.connectAttr(pair_blend_node + '.outTranslate', skin_joint + '.translate')
                cmd.connectAttr(pair_blend_node + '.outRotate', skin_joint + '.rotate')

            if cmd.checkBoxGrp('blend_select', q = 1, value2 = 1):
                blend_scale_node = cmd.createNode('pairBlend', n = skin_joint + '_scale_pb')

                cmd.connectAttr(switch_attribute, blend_scale_node + '.weight')
                cmd.connectAttr(ik_joint + '.scale', blend_scale_node + '.inTranslate1')
                cmd.connectAttr(fk_joint + '.scale', blend_scale_node + '.inTranslate2')
                cmd.connectAttr(blend_scale_node + '.outTranslate', skin_joint + '.scale')


    def build_ui(self):
        if cmd.window(self.winID, exists = 1): 
            cmd.deleteUI(self.winID)

        cmd.window(self.winID, s = 0, rtf = 1)

        # Window
        cmd.columnLayout()
        cmd.text('switch_label', l = 'Switch :', h = self.row_height)
        cmd.optionMenu('switch_attr', l = 'Weight attribute : ')
        cmd.separator()
        cmd.text('ik_label', label = 'IK chain : ', h = self.row_height)
        cmd.separator()
        cmd.text('fk_label', label = 'FK chain : ', h = self.row_height)
        cmd.separator()
        cmd.text('skin_label', label = 'Skin chain : ', h = self.row_height)
        cmd.separator()
        cmd.checkBoxGrp('blend_select', numberOfCheckBoxes = 2, l = 'Blend : ', labelArray2 = ['Position', 'Scale'], value1 = 1, value2 = 0, columnWidth3 = (self.column_width_1, 110, 150))
        cmd.separator()
        cmd.button(label = 'Create Pair Blends', h = 32, w = 400, c = lambda x : self.create_pair_blends())
        cmd.setParent('..')

        # Show window
        cmd.showWindow()
        
        # ScriptJobs
        cmd.scriptJob(e = ['SelectionChanged', self.update_targets], p = self.winID)


BatchPairBlend()