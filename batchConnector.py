import maya.cmds as cmd

# Select output node then input node

selection = cmd.ls(sl = 1)
output = selection.pop(0)

outAttr = 'outputX'
inAttr = ['v']

print(output)
print(selection)

for item in selection:
    for attr in inAttr:
        cmd.connectAttr(output + '.' + outAttr, item + '.' + attr, f = 1)