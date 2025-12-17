# WIP
import maya.cmds as cmd

print('imported BatchConnectorUI')

class BatchConnectorUI:
    selection = cmd.ls(sl = 1)

    def __init__(self):
        self.winID = 'BatchConnector'
        self.row_height = 24
        self.list_height = 100

        self.build_ui()


    def update_selection(self):
        BatchConnectorUI.selection = cmd.ls(sl = 1)


    def add_items(self, ui_items):
        existing_items = cmd.textScrollList(ui_items, q = True, allItems = True)

        if BatchConnectorUI.selection:
            items = BatchConnectorUI.selection
            if existing_items : 
                items = [item for item in items if item not in existing_items]
            else: pass
            cmd.textScrollList(ui_items, e = True, enable = True, append = items)


    def remove_items(self, ui_items):
        selected_items = cmd.textScrollList(ui_items, q = True, selectItem = True)
        if selected_items:
            cmd.textScrollList(ui_items, e = True, removeItem = selected_items)
        else: pass


    def clear_items(self, ui_items):
        cmd.textScrollList(ui_items, e = True, removeAll = True)


    def update_attr(self, ui_items, ui_output):
        selected_items = cmd.textScrollList(ui_items, q = True, selectItem = True)
        attributes = []

        if selected_items:
            for item in selected_items:
                item_attributes = cmd.listAttr(item, c = 1)
                attributes = item_attributes
            
            cmd.textScrollList(ui_output, e = True, ra = True)
            cmd.textScrollList(ui_output, e = True, enable = True, append = attributes)

        else: 
            cmd.textScrollList(ui_output, e = True, ra = True)

        # cmd.textScrollList(self.list_output_attr, e = True, removeAll = True)

        # attributes = cmd.listAttr(source, c = 1)

        # if attributes:
        #     cmd.textScrollList(self.list_output_attr, e = True, enable = True, append = attributes)


    def connect_attributes(self, _):
        out_item = cmd.textScrollList(self.list_source, q = True, selectItem = True)
        out_attr = cmd.textScrollList(self.list_output_attr, q = True, selectItem = True)

        in_items = cmd.textScrollList(self.list_targets, q = True, selectItem = True)
        in_attr = cmd.textScrollList(self.list_input_attr, q = True, selectIndexedItem = True)

        for item in in_items:
            print(item)
            for attr in in_attr:
                print(attr)
                attribute = cmd.listAttr(item, c = 1)[attr-1]
                print(attribute)
                cmd.connectAttr(out_item[0] + '.' + out_attr[0], item + '.' + attribute, f = 1)


    def disconnect_attributes(self, _):
        out_item = cmd.textScrollList(self.list_source, q = True, selectItem = True)
        out_attr = cmd.textScrollList(self.list_output_attr, q = True, selectItem = True)

        in_items = cmd.textScrollList(self.list_targets, q = True, selectItem = True)
        in_attr = cmd.textScrollList(self.list_input_attr, q = True, selectItem = True)
        
        for item in in_items:
            for attr in in_attr:
                cmd.disconnectAttr(out_item[0] + '.' + out_attr[0], item + '.' + attr)


    def build_ui(self):
        if cmd.window(self.winID, exists = 1):
            cmd.deleteUI(self.winID)
        cmd.window(self.winID, s = 0, rtf = 1)

        #Fenêtre
        cmd.columnLayout()
        cmd.rowLayout(nc = 2)

        # Source
        cmd.columnLayout()
        cmd.text(label = 'Objects', h = self.row_height)
        cmd.rowLayout(nc = 3)
        cmd.button(label = 'Add', w = 100, c = lambda x: self.add_items(self.list_source)) # lambda x: fonction pour pouvoir mettre des arguments
        cmd.button(label = 'Remove', w = 100, c = lambda x: self.remove_items(self.list_source))
        cmd.button(label = 'Clear', c = lambda x: self.clear_items(self.list_source))
        cmd.setParent('..')
        cmd.separator()
        self.list_source = cmd.textScrollList(h = self.list_height, allowMultiSelection = False, enable = False, sc = lambda : self.update_attr(self.list_source, self.list_output_attr))
        cmd.separator()
        cmd.text(label = 'Outputs', h = self.row_height)
        self.list_output_attr = cmd.textScrollList(h = self.list_height + 100, allowMultiSelection = False, enable = False)
        # print(source)
        cmd.setParent('..')

        # Target
        cmd.columnLayout()
        cmd.text('targets_label', label = 'Target CTRLs', h = self.row_height)
        cmd.rowLayout(nc = 3)
        cmd.button(label = 'Add', w = 100, c = lambda x: self.add_items(self.list_targets))
        cmd.button(label = 'Remove', w = 100, c = lambda x: self.remove_items(self.list_targets))
        cmd.button(label = 'Clear', c = lambda x: self.clear_items(self.list_targets))
        cmd.setParent('..')
        cmd.separator()
        self.list_targets = cmd.textScrollList(h = self.list_height, allowMultiSelection = True , enable = False, sc = lambda : self.update_attr(self.list_targets, self.list_input_attr))
        cmd.separator()
        cmd.text(label = 'Inputs', h = self.row_height)
        self.list_input_attr = cmd.textScrollList(h = self.list_height + 100, allowMultiSelection = True , enable = False)
        # print(targets)
        cmd.setParent('..')
        cmd.setParent('..')

        # Copy Shapes button
        cmd.columnLayout()
        cmd.button(label = 'Connect!', h = 32, w = 518, c = self.connect_attributes)
        cmd.separator()
        cmd.button(label = 'Disconnect!', h = 24, w = 518, c = self.disconnect_attributes)
        cmd.setParent('..')

        # Draw window
        cmd.showWindow()

        # ScriptJobs
        cmd.scriptJob(e = ['SelectionChanged', self.update_selection], p = self.winID)


BatchConnectorUI()