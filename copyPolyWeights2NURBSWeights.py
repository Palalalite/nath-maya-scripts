import maya.cmds as cmd

# Select TARGETS first, and SOURCE last.

# Functions
def get_skinCluster(geometry):
    shape = cmd.listRelatives(geometry, c = 1, s = 1, ni = 1)[0]
    print(shape)
    skin = cmd.listConnections(shape, type = 'skinCluster')
    return skin


def get_bound_joints(geometry):
    skin = get_skinCluster(geometry)
    joints = cmd.listConnections(skin, type = 'joint')
    joints = list(dict.fromkeys(joints)) # Remove duplicate joints
    print(joints)
    return joints


def get_vertices(geometry):
    vertices = cmd.ls(geometry + ".vtx[:]", fl = 1)
    return vertices


def get_control_vertices(surface):
    control_vertices = cmd.ls(surface + ".cv[:][:]", fl = 1)
    return control_vertices


def get_weights(geometry):
    weights = []
    skin = get_skinCluster(geometry)[0]
    vertices = get_vertices(geometry)
    
    for vertex in vertices:
        vertex_weights = cmd.skinPercent(skin, vertex, q = 1, v = 1)
        weights.append(vertex_weights)
    
    print(weights)
    return weights


def set_weights(source_weights, target_bound_joints, target_skin, target_vertices):
    for vertex, weight in zip(target_vertices, source_weights):
        print(vertex)
        
        joint_weight_pair = [(joint, influence) for joint, influence in zip(target_bound_joints, weight)]
        print(joint_weight_pair)
        
        cmd.skinPercent(target_skin, vertex, transformValue = joint_weight_pair)
            

# Script
selection = cmd.ls(sl = 1)
source = selection.pop(-1)
target = selection[0]
print(source)
print(target)


# Get Source Vertices
source_vertices = get_vertices(source)
print(source_vertices)


# Get Source Vertex Weights
source_weights = get_weights(source)


# Get Source Skinned Joints
source_joints = get_bound_joints(source)


# Bind Source Joints to Target
if get_skinCluster(target):
    target_skin = get_skinCluster(target)[0]

else:
    target_skin = cmd.skinCluster(target, source_joints, toSelectedBones = 1, bindMethod = 0, skinMethod = 0, normalizeWeights = 1, weightDistribution = 0, maximumInfluences = 5, obeyMaxInfluences = 1, removeUnusedInfluence = 0)[0]
    
# Get Target Vertices
target_vertices = get_control_vertices(target)


# Get Target Skinned Joints
target_bound_joints = get_bound_joints(target)


# Set Target Vertices Weights
set_weights(source_weights, target_bound_joints, target_skin, target_vertices)