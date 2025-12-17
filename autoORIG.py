import maya.cmds as cmd
import random
import string

# Variables
parenting = 1
id_length = 3
orig_suffix = 'offset'

# Functions
def get_position(item):
    translates = cmd.xform(item, q = 1, ws = 1, t = 1)
    rotates = cmd.xform(item, q = 1, ws = 1, ro = 1)
    position = {"translates": translates, "rotates": rotates}
    return position


def get_parent(item):
    parent = cmd.listRelatives(item, p = 1)
    return parent[0]


def get_label(item):
    random_id = ''.join(random.choice(string.digits) for i in range(id_length))
    name = '_'.join([item, orig_suffix, random_id])
    return name


def create_group(item):
    parent = get_parent(item)
    name = get_label(item)
    position = get_position(item)
    orig = cmd.group(n = name, w = 1, em = 1)
    cmd.xform(orig, ws = 1, t = position['translates'])
    cmd.xform(orig, ws = 1, ro = position['rotates'])
    if parent : cmd.parent(orig, parent)
    cmd.parent(item, orig)
    return orig


# Script
selection = cmd.ls(sl = 1)
for item in selection:
    create_group(item)