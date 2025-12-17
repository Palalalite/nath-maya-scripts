import maya.cmds as cmd

selection = cmd.ls(sl = 1)

for item in selection:
    cmd.select(item + ".cv[:]", r = 1)
    cmd.scale(-1, -1, -1, os = 1, xyz = 1)