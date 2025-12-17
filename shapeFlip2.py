import maya.cmds as cmd

#user values
axis = [0, 0, 1]

selection = cmd.ls(sl = 1)

for item in selection:
    shape = cmd.listRelatives(item, s = 1)[0]
    print(shape)
    
    if axis == [1, 0, 0]:
        x = '180deg'
        y = 0
        z = 0
    elif axis == [0, 1, 0]:
        x = 0
        y = '180deg'
        z = 0
    elif axis == [0, 0, 1]:
        x = 0
        y = 0
        z = '180deg'
        
    cmd.select(shape + ".cv[:]", r = 1)
    cmd.rotate(x, y, z, r = 1)