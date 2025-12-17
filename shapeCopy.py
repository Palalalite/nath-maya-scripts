import maya.cmds as cmd

# Variables
defaultColor = 17

selection = cmd.ls(sl = 1)

baseTransform = selection.pop(-1)
targets = selection.copy()

print(baseTransform)
print(targets)

baseDuplicates = [cmd.duplicate(baseTransform, n = target + "_duplicata", rc = 1)[0] for target in targets]

print(baseDuplicates)

for (duplicata, target) in zip(baseDuplicates, targets):
    newShape = cmd.listRelatives(duplicata, s = 1)[0]
    print(newShape)
    
    cmd.setAttr(newShape + '.overrideEnabled', 1)
    
        
    oldShape = cmd.listRelatives(target, s = 1)[0]
    print(oldShape)
    
    colored = cmd.getAttr(oldShape + '.overrideEnabled')
    print(colored)
    
    if colored:
        targetColor = cmd.getAttr(oldShape + '.overrideColor')
    else:
        targetColor = defaultColor
    
    print(targetColor)
    cmd.setAttr(newShape + '.overrideColor', targetColor)
    
    cmd.parent(newShape, target, r = 1, s = 1)

    
    cmd.delete(oldShape, s = 1)
    
    cmd.delete(duplicata)
    
    