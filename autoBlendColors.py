import maya.cmds as cmd

attributes = ["translate", "rotate"]

selection = cmd.ls(sl = 1)

switch = selection.pop(0)
FK = selection.pop(0)
IK = selection.pop(0)
child = selection.pop(0)

blender = switch + ".SwitchIKFK"

set = [FK, IK]

for attribute in attributes:
    if attribute == "translate":
        suffix = "_BCT"
    elif attribute == "rotate":
        suffix = "_BCR"
    elif attribute == "scale":
        suffix = "_BCS"
        
    blendNode = cmd.createNode("blendColors", n = '_'.join(child.split('_')[0:3]) + suffix)
    
    cmd.connectAttr(blender, blendNode + ".blender")
    
    for item in set:
        cmd.connectAttr(item + "." + attribute, blendNode + ".color" + str(set.index(item) + 1))

    cmd.connectAttr(blendNode + ".output", child + "." + attribute)