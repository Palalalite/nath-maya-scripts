import maya.cmds as cmd

#user settings
blendScales = 1


selection = cmd.ls(sl = 1)

switch = selection.pop(0)
IK = selection.pop(0)
FK = selection.pop(0)
child = selection.pop(0)

blender = switch + ".SwitchIKFK"

joints = [IK, FK]
      
pairBlendNode = cmd.createNode("pairBlend", n = '_'.join(child.split('_')[0:3]) + "_PBL")
cmd.setAttr(pairBlendNode + ".rotInterpolation", 1)

cmd.connectAttr(blender, pairBlendNode + ".weight")

scaleBlendNode = cmd.createNode("pairBlend", n = '_'.join(child.split('_')[0:3]) + "_PBS")

for (item, i) in zip(joints, range(1,3)):
    cmd.connectAttr(item + ".translate", pairBlendNode + ".inTranslate" + str(i), f = 1)
    cmd.connectAttr(item + ".rotate", pairBlendNode + ".inRotate" + str(i), f = 1)
    
    cmd.connectAttr(item + ".scale", scaleBlendNode + ".inTranslate" + str(i), f = 1)
    
cmd.connectAttr(pairBlendNode + ".outTranslate", child + ".translate" , f = 1)
cmd.connectAttr(pairBlendNode + ".outRotate", child + ".rotate" , f = 1)
cmd.connectAttr(scaleBlendNode + ".outTranslate", child + ".scale" , f = 1)