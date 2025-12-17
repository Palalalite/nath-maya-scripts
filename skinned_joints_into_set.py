import maya.cmds as cmd


# Functions
def get_skinCluster(geometry):
    shape = cmd.listRelatives(geometry, c = 1, s = 1, ni = 1)[0]
    skin = cmd.listConnections(shape, type = 'skinCluster')
    return skin


def get_bound_joints(geometry):
    skin = get_skinCluster(geometry)
    joints = cmd.listConnections(skin, type = 'joint')
    joints = list(dict.fromkeys(joints)) # Remove duplicate joints
    return joints


def make_into_set(name, items):
    print(name)
    print(items)
    cmd.select(items)
    set = cmd.sets(n = name + '_skin_joints')
    return set 


# Script
selection = cmd.ls(sl = 1)


# Get bound joints
skin_clusters = []

for item in selection:
    geometry_name = item
    skin_cluster = get_bound_joints(item)
    
    ensemble = (geometry_name, skin_cluster)
    
    skin_clusters.append(ensemble)

print(skin_clusters)


# Create sets
for ensemble in skin_clusters:
    make_into_set(ensemble[0], ensemble[1])