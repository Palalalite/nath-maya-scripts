import maya.cmds as cmd


# Variables
winID = 'Colorizer'
column_width_1 = 50
row_height = 24


# Functions
def item_force_string(item):
    if type(item) is str : item = item
    if type(item) is list : item = item[0]
    return item


def get_objects_to_color():
    selection = cmd.ls(sl = 1)
    targets = []
    
    shape = cmd.checkBox('shape', v = 1, q = 1)
    children = cmd.checkBox('children', v = 1, q = 1)

    # print(selection)

    for item in selection:
        if shape:
            allShapes = cmd.listRelatives(item, c = 1, s = 1)
            if allShapes :
                for i in allShapes:
                    if cmd.objectType(i, isType = 'nurbsCurve'):
                        targets.append(i)
                        # print(i)
            else : targets.append(item)
        else : targets.append(item)
    

    return targets


def change_color():
    targets = get_objects_to_color()
    color = cmd.colorIndexSliderGrp('color', q = 1, value = 1) - 1
    
    print(color)

    for target in targets:
        item_force_string(target)
        
        print(target)
        cmd.setAttr(target + ".overrideEnabled", 1)
        cmd.setAttr(target + ".overrideColor", color)


def item_force_string(item):
    if type(item) is str : item = item
    if type(item) is list : item = item[0]
    return item


# Initializing
if cmd.window(winID, exists = 1): 
    cmd.deleteUI(winID)
cmd.window(winID, rtf = 1, s = 0, tlb = 1)


# Window
cmd.columnLayout()

# Couleur
cmd.rowLayout(nc = 1, h = row_height)
cmd.colorIndexSliderGrp('color', label = 'Couleur', min = 1, max = 32, value = 18, columnWidth3 = (column_width_1, 40, 190))
cmd.setParent('..')


# Shape et enfants
cmd.rowLayout(nc = 2, h = row_height)
cmd.checkBox('shape', label = 'Shape', w = 145)
cmd.checkBox('children', label = 'Enfants (WIP)', w = 145)
cmd.setParent('..')


# Bouton
cmd.rowLayout(nc = 1, h = row_height)
cmd.button(label = 'Set!', command = 'change_color()', w = column_width_1 + 240)
cmd.setParent('..')

# Draw Window
cmd.showWindow()