import maya.cmds as cmd

# Variables
label = ''
ctrl_suffix = '_CTRL'
orig_suffix = '_orig'

# Functions
def create_ctrl(follicle):
    ctrl = cmd.circle(n = follicle + ctrl_suffix)
    orig = cmd.group(n = follicle + orig_suffix)
    return ctrl, orig

def create_joint(follicle):
    joint = cmd.joint(n = follicle + '_skn', r = 0, p = [0, 0, 0])
    return joint


def ctrl_under_follicle(follicle):
    ctrl_orig = create_ctrl(follicle)
    cmd.select(ctrl_orig[0], r = 1)
    joint = create_joint(follicle)
    cmd.parent(ctrl_orig[1], follicle, r = 1)
    
# Script
selection = cmd.ls(sl = 1)

for follicle in selection:
    ctrl_under_follicle(follicle)