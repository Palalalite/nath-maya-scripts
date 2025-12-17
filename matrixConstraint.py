import maya.cmds as cmd

translates = 1
rotates = 1
scales = 0
shears = 1


selection = cmd.ls(sl = 1)

parentObj = selection.pop(0)

print(parentObj)

childObj = selection.pop(0)

print(childObj)

multMatrx = cmd.createNode("multMatrix", n = parentObj + "_MMX")
decoMatrx = cmd.createNode("decomposeMatrix", n = parentObj + "_DCM")

cmd.connectAttr(parentObj + ".worldMatrix[0]", multMatrx + ".matrixIn[0]")

cmd.connectAttr(childObj + ".parentInverseMatrix[0]", multMatrx + ".matrixIn[1]")

cmd.connectAttr(multMatrx + ".matrixSum", decoMatrx + ".inputMatrix")

if translates:
    cmd.connectAttr(decoMatrx + ".outputTranslate", childObj + ".translate")

if rotates :
    cmd.connectAttr(decoMatrx + ".outputRotate", childObj + ".rotate")
else:
    cmd.orientConstraint(parentObj, childObj, mo = 0)
    
if scales:
    cmd.connectAttr(decoMatrx + ".outputScale", childObj + ".scale")
    
if shears:
    cmd.connectAttr(decoMatrx + ".outputShear", childObj + ".shear")