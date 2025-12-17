import maya.cmds as cmd

print('imported shapeCopyUI')

class ShapeCopyUI:
    selection = cmd.ls(sl = 1)

    def __init__(self):
        self.winID = 'ShapeCopy'
        self.row_height = 24
        self.list_height = 100

        self.build_ui()


    def update_selection(self):
        ShapeCopyUI.selection = cmd.ls(sl = 1)


    def update_source(self, _):
        cmd.textScrollList(self.list_source, e = True, removeAll = True)

        if ShapeCopyUI.selection:
            item = ShapeCopyUI.selection[0]
            cmd.textScrollList(self.list_source, e = True, enable = True, append = item)

        else:
            cmd.textScrollList(self.list_source, e = True, enable = False, append = 'Please select a source CTRL')


    def add_targets(self, _):
        target_items = cmd.textScrollList(self.list_targets, q = True, allItems = True)

        if ShapeCopyUI.selection:
            items = ShapeCopyUI.selection
            if target_items : 
                items = [item for item in items if item not in target_items]
            else: pass
            cmd.textScrollList(self.list_targets, e = True, enable = True, append = items)
        

    def remove_targets(self, _):
        target_items = cmd.textScrollList(self.list_targets, q = True, selectItem = True)
        if target_items:
            cmd.textScrollList(self.list_targets, e = True, removeItem = target_items)
        else: pass


    def clear_targets(self, _):
        cmd.textScrollList(self.list_targets, e = True, removeAll = True)


    def copy_shape(self, _):
        source = cmd.textScrollList(self.list_source, q = True, allItems = True)
        targets = cmd.textScrollList(self.list_targets, q = True, allItems = True)
        print(source)
        print(targets)

        color = 0
        for target in targets:

            newCtrl = cmd.duplicate(source, rc = 1)
            if cmd.listRelatives(newCtrl, typ = 'transform'):
                cmd.delete(cmd.listRelatives(newCtrl, typ = 'transform'))
            
            shapes = cmd.listRelatives(newCtrl[0], s = 1)

            # delete oldTargetShapes
            for shape in cmd.listRelatives(target, s = 1):
                if cmd.getAttr(shape + '.overrideColor') > 0:
                    color = cmd.getAttr(shape + '.overrideColor')
                print(color)
                cmd.delete(shape, s = 1)

            # parent savedShapes under target
            for shape in shapes:
                cmd.parent(shape, target, r = 1, s = 1)
                if color > 0:
                    cmd.setAttr(shape + '.overrideEnabled', 1)
                    cmd.setAttr(shape + '.overrideColor', color)
            
            # delete dummyTransform
            cmd.delete(newCtrl[0])


    def flip_shape(self, _):
        targets = cmd.textScrollList(self.list_targets, q = True, allItems = True)

        for item in targets:
            cmd.select(item + ".cv[:]", r = 1)
            cmd.scale(-1, -1, -1, os = 1, xyz = 1)
            cmd.select(item, r = 1)


    def build_ui(self):
        if cmd.window(self.winID, exists = 1):
            cmd.deleteUI(self.winID)
        cmd.window(self.winID, s = 0, rtf = 1)

        #Fenêtre
        cmd.columnLayout()
        cmd.rowLayout(nc = 2)

        # Source
        cmd.columnLayout()
        cmd.text('source_label', label = 'Source Shape', h = self.row_height)
        cmd.button('update_source', label = 'Set Source', c = self.update_source)
        cmd.separator()
        self.list_source = cmd.textScrollList(h = self.list_height, enable = False)
        # print(source)
        cmd.setParent('..')

        # Target
        cmd.columnLayout()
        cmd.text('targets_label', label = 'Target CTRLs', h = self.row_height)
        cmd.rowLayout(nc = 3)
        cmd.button('add_targets', label = 'Add', w = 100, c = self.add_targets)
        cmd.button('remove_targets', label = 'Remove', w = 100, c = self.remove_targets)
        cmd.button('clear_targets', label = 'Clear', c = self.clear_targets)
        cmd.setParent('..')
        cmd.separator()
        self.list_targets = cmd.textScrollList(h = self.list_height, allowMultiSelection = True , enable = False)
        # print(targets)
        cmd.setParent('..')
        cmd.setParent('..')

        # Copy Shapes button
        cmd.rowLayout(nc = 2)
        cmd.button(label = 'Copy Shapes!', h = 32, w = 396, command = self.copy_shape)
        cmd.button(label = 'Flip copy', h = 32, w = 120, command = self.flip_shape)
        cmd.setParent('..')

        # Draw window
        cmd.showWindow()

        # ScriptJobs
        cmd.scriptJob(e = ['SelectionChanged', self.update_selection], p = self.winID)


ShapeCopyUI()