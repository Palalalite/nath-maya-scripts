#get selection's world translates and rotates
selection = cmd.ls(sl = 1)

destPos = cmd.xform(selection[0], q = 1, ws = 1, rp = 1)
print(destPos)

destOri = cmd.xform(selection[0], q = 1, ws = 1, ro = 1)
print(destOri)

#create locator and constraint it
loc = cmd.spaceLocator(n = selection[0] + '_loc')
cmd.parentConstraint(selection[0], loc, mo = 0)