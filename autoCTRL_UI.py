import maya.cmds as cmd

class autoCTRL_UI():
    selection = cmd.ls(sl = 1)

    def __init__(self):
        self.winID = 'AutoCTRL'
        self.column_width_1 = 60
        self.row_height = 26
        self.ctrl_suffix = '_ctrl'
        self.orig_suffix = '_offset'
        self.folder = 'shapes_folder'
        self.fbx_files = cmd.getFileList(folder = self.folder, filespec = '*.fbx')
        # self.ma_files = cmd.getFileList(folder = self.folder, filespec = '*.ma')

        self.build_ui()


    # Functions
    def update_selection(self):
        autoCTRL_UI.selection = cmd.ls(sl = 1)


    def get_shapes_list(self):
        controllers = {}
        
        print(self.fbx_files)
        
        # for item in self.fbx_files:
        #     file = item
        #     name = file.replace('.fbx', '').capitalize()
        #     controllers[name] = file    # dictionary_name[key] = value
        
        return controllers


    def shapes_into_menu(self):
        controllers = self.get_shapes_list()
        for controller in controllers:
            name = controller.replace('_', ' ') # get entry name
            cmd.menuItem(label = name)


    def update_shape(self):
        shape_choice = cmd.optionMenu('ctrl_shape', q = 1, value = 1)
        print(shape_choice)
        return shape_choice


    def import_shape(self):
        controllers = self.get_shapes_list()
        choice = self.update_shape()
        file = controllers[choice]
        full_path = self.folder + "\\" + file
        
        #file -import -type "FBX"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "cube" -options "fbx"  -pr  -importTimeRange "combine" "C:/Lazul/SCRIPTS/controllers/cube.fbx"
        cmd.file(full_path, i = 1, type = "FBX", iv = 1, ra = 1, mnc = 0, op = 'fbx', pr = 1)
        #print(full_path)


    def update_name(self):
        name = cmd.textFieldGrp('ctrl_label', q = 1, text = 1)
        name = name.replace(' ', '_')
        return name


    def update_color(self):
        color = cmd.colorIndexSliderGrp('ctrl_color', q = 1, value = 1)
        color = color - 1
        return color


    def update_scale(self):
        scale = cmd.floatSliderGrp('ctrl_scale', q = 1, value = 1)
        return scale


    def update_constraint(self):
        constraint_translate = cmd.checkBoxGrp('ctrl_constraints', q = 1, value1 = 1)
        constraint_orient = cmd.checkBoxGrp('ctrl_constraints', q = 1, value2 = 1)
        return [constraint_translate, constraint_orient]


    def name_exists(self):
        name = self.update_name()
        if name: 
            return 1
        else: 
            print('Please input a name')
            return 0


    def create_controller(self):
        name = ''
        selection = self.get_selection()
    
        if self.name_exists():
            name = self.update_name()
        
        elif selection:
            name = selection
        
        print('name = ' + str(name))
        ctrl = self.import_shape()
        orig = cmd.group(n = name + self.orig_suffix)
        
        return orig, ctrl


    def print_data(self):
        selection = self.get_selection()
        name = self.update_name()
        shape = self.update_shape()
        color = self.update_color()
        scale = self.update_scale()
        constraint = self.update_constraint()
        
        print('\nPrinting...')
        print(selection)
        print(name)
        print(shape)
        print(color)
        print(scale)
        print(constraint)


    def button_action(self):
        self.print_data()
        self.create_controller()


    # Initializing
    def build_ui(self):
        if cmd.window(self.winID, exists = 1): 
            cmd.deleteUI(self.winID)

        cmd.window(self.winID, s = 0, rtf = 1)

        # Window
        cmd.rowLayout(nc = 2)

        # Les paramètres
        cmd.columnLayout()

        # Nom
        cmd.rowLayout(nc = 1, h = self.row_height)
        cmd.textFieldGrp('ctrl_label', label = 'Nom', columnWidth2 = (self.column_width_1, 235), text = "")
        cmd.setParent('..')

        # Forme (+ wip: BOUTON POUR METTRE SEULEMENT LA SHAPE)
        cmd.rowLayout(nc = 2, h = self.row_height)
        cmd.text(label = 'Forme', align = 'right', w = self.column_width_1)
        cmd.optionMenu('ctrl_shape')
        self.shapes_into_menu()
        cmd.setParent('..')

        # Couleur
        cmd.rowLayout(nc = 1, h = self.row_height)
        cmd.colorIndexSliderGrp('ctrl_color', label = 'Couleur', min = 1, max = 32, value = 14, columnWidth3 = (self.column_width_1, 72, 160))
        cmd.setParent('..')

        # Scale
        cmd.rowLayout(nc = 1, h = self.row_height)
        cmd.floatSliderGrp('ctrl_scale', l = 'Scale', columnWidth3 = (self.column_width_1, 50, 183), field = 1, value = 10, min = 1, max = 99)
        cmd.setParent('..')

        # Contraintes
        cmd.rowLayout(nc = 1)
        cmd.checkBoxGrp('ctrl_constraints', numberOfCheckBoxes = 2, l = 'Contrainte', labelArray2 = ['Translate', 'Orient'], value1 = 1, value2 = 1, columnWidth3 = (self.column_width_1, 110, 150))
        cmd.setParent('..')

        # Créer les contrôleurs
        cmd.rowLayout(nc = 1)
        cmd.button(label = 'Create controller', h = 32, w = 303, command = lambda x : self.button_action)
        cmd.setParent('..')

        # Draw window
        cmd.showWindow()


autoCTRL_UI()