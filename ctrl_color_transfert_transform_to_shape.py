import maya.cmds as cmd

selection = cmd.ls(sl = 1)

# Functions
def get_selection_data(ctrl_transform):
    ctrl_data = {}
    for item in ctrl_transform:
        color = cmd.getAttr(item + '.overrideColor')
        shapes = cmd.listRelatives(item, s = 1, ni = 1)

        ctrl_data[item] = {'color': color, 'shapes': shapes}
    # print(ctrl_data)
    return ctrl_data

def create_shapes_new_name(ctrl_dict):
    for item in ctrl_dict:
        shapes = ctrl_dict[item]['shapes']

        shape_new_name_list = []

        i = 0

        while i < len(shapes):
            i = i + 1
            id = f'{i:02}'
            
            new_name = item + 'Shape' + id

            shape_new_name_list.append(new_name)

            ctrl_dict[item]['shapes_new_name'] = shape_new_name_list
    return ctrl_dict

def rename_shapes(ctrl_dict):
    for item in ctrl_dict:
        old_names = ctrl_dict[item]['shapes']
        new_names = ctrl_dict[item]['shapes_new_name']
        print(old_names, new_names)

        for (old_name, new_name) in zip (old_names, new_names):
            cmd.rename(item + '|' + old_name, new_name)
        
        print(cmd.listRelatives(item, s = 1, ni = 1))


def apply_color_to_shapes(ctrl_dict):
    print(ctrl_dict)
    for item in ctrl_dict:
        shapes = ctrl_dict[item]['shapes_new_name']
        color = ctrl_dict[item]['color']

        for shape in shapes:
            print(shape)
            cmd.setAttr(shape + '.overrideEnabled', 1)
            cmd.setAttr(shape + '.overrideColor', color)
        
        # cmd.setAttr(ctrl + '.overrideEnabled', 0)

# Script
ctrl_dict = get_selection_data(selection)
ctrl_dict = create_shapes_new_name(ctrl_dict)
rename_shapes(ctrl_dict)
apply_color_to_shapes(ctrl_dict)