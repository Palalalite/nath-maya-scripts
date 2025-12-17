import maya.cmds as cmd


# Variables
selection = cmd.ls(sl = 1)
vent = selection.pop(0)
driven_key = selection.pop(0)
mult_double_linear = selection.pop(0)
offsets = selection.copy()


# Functions


# Script
new_driven_key = cmd.duplicate(driven_key)[0]
new_mult_double_linear = cmd.duplicate(mult_double_linear)[0]

cmd.connectAttr(vent + '.cycle', new_driven_key + '.input', f = 1)
cmd.connectAttr(vent + '.weight', new_mult_double_linear + '.input1', f = 1)
cmd.connectAttr(new_driven_key + '.output', new_mult_double_linear + '.input2', f = 1)

cmd.connectAttr(new_mult_double_linear + '.output', offsets[0] + '.rotateY', f = 1)

unit_conversion = cmd.listConnections(new_mult_double_linear + '.output')[0]

for offset in offsets[1:]:
    cmd.connectAttr(unit_conversion + '.output', offset + '.rotateY', f = 1)

cmd.select(vent, driven_key, mult_double_linear, r = 1)