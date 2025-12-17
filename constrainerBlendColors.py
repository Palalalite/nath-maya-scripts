import maya.cmds as cmd

selection = cmd.ls(sl = 1)

parent1 = selection[0]
parent2 = selection[1]
child = selection[2]

blendPos = cmd.createNode("blendColors", n = child + '_BCT')
blendRot = cmd.createNode("blendColors", n = child + '_BCR')

cmd.connectAttr(parent1 + ".translate", blendPos + ".color1")
cmd.connectAttr(parent2 + ".translate", blendPos + ".color2")  
  
cmd.connectAttr(parent1 + ".rotate", blendRot + ".color1")
cmd.connectAttr(parent2 + ".rotate", blendRot + ".color2")

cmd.connectAttr(blendPos + ".output", child + ".translate")
cmd.connectAttr(blendRot + ".output", child + ".rotate")