import maya.cmds as cmd

selection = cmd.ls(sl = 1)
attributes0 = ["tx", "ty", "tz", "rx", "ry", "rz"]
attributes1 = ["sx", "sy", "sz"]
optional = ["globalScale", "follows"]

for item in selection:
    for attribute in attributes0:
        if(cmd.getAttr(item + "." + attribute, se = 1)):
            cmd.setAttr(item + "." + attribute, 0)
    
    for attribute in attributes1:
        if(cmd.getAttr(item + "." + attribute, se = 1)):
            cmd.setAttr(item + "." + attribute, 1)
    
    for attribute in optional:
        if(cmd.attributeQuery(attribute, node = item, ex = 1)):
            if attribute == 'globalScale':
                cmd.setAttr(item + "." + attribute, 1)

            if attribute == 'follows':
                cmd.setAttr(item + "." + attribute, 0)