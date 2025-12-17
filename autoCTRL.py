import maya.cmds as cmd


# Variables
ctrl_radius = 2.0
normals = (1.0, 0.0, 0.0)
ctrl_suffix = '_ctrl'
orig_suffix = '_offset'
constraint = 1
keep_hierarchy = 1
color = 13

# Functions
def make_joints_dictionnary(selection):
    joints = {}
    [joints.update({item : {}}) for item in selection if cmd.objectType(item, isType = 'joint') or cmd.objectType(item, isType = 'cluster')]
    return joints


def get_label(dict):
    for item in list(dict):
        dict[item].update({"label" : item})
        print(dict)
    return dict


def get_parent(dict):
    for item in list(dict):
        parent = cmd.listRelatives(item, parent = 1)
        if parent and cmd.objectType(parent, isType = 'joint'):
            dict[item].update({"parent" : parent})
    return dict


def get_position(dict):
    for item in list(dict):
        position = {"translates" : cmd.xform(item, q = 1, ws = 1, t = 1), "rotates" : cmd.xform(item, q = 1, ws = 1, ro = 1)}
        dict[item].update({"position" : position})
    return dict


def make_controller(dict):
    for item in list(dict):
        label = dict[item]['label']

        ctrl = cmd.circle(n = label + ctrl_suffix , radius = ctrl_radius, nr = normals)
        orig = cmd.group(n = label+ ctrl_suffix + orig_suffix)

        dict[item].update({"ctrl" : ctrl[0]})
        dict[item].update({"orig" : orig})
    return dict


def set_position(dict):
    for item in list(dict):
        orig = dict[item]['orig']
        translates = dict[item]['position']['translates']
        rotates = dict[item]['position']['rotates']

        cmd.xform(orig, ws = 1, t = translates)
        cmd.xform(orig, ws = 1, ro = rotates)


def set_parent(dict):
    for item in list(dict):
        if 'parent' in dict[item].keys():
            parent_joint = dict[item]['parent'][0]
            if parent_joint in list(dict):
                orig = dict[item]['orig']
                parent = dict[parent_joint]['ctrl']
                cmd.parent(orig, parent)


def set_constraints(dict):
    for item in list(dict):
        joint = item
        ctrl = dict[item]['ctrl']

        cmd.parentConstraint(ctrl, joint, mo = 0)


def set_color(item):
    shape = cmd.listRelatives(item, s = 1, ni = 1)[0]
    if shape:
        print(shape)
        cmd.setAttr(shape + '.overrideEnabled', 1)
        cmd.setAttr(shape + '.overrideColor', color)


# Script
selection = cmd.ls(sl = 1)
joints = make_joints_dictionnary(selection)

get_label(joints)
get_parent(joints)
get_position(joints)
make_controller(joints)
set_position(joints)

if constraint : set_constraints(joints)

if keep_hierarchy : set_parent(joints)

for item in joints:
    ctrl = joints[item]['ctrl']
    print(ctrl)
    set_color(ctrl)