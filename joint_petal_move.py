import maya.cmds as cmd

# Dupliquer une chaine de joint et attacher les duplicatas à chaque pétale
# D'abord sélectionner le joint base, puis ensuite les modés

# Variables
anchor_vertex = 166
offset = [-135.0, 0.0, 0.0]

# Functions
def get_joint_chain(joint):
    joint_chain = cmd.listRelatives(joint, ad = 1, ni = 1)
    joint_chain.append(joint)
    joint_chain.reverse()
    return joint_chain


def get_chain_suffixes(chain):
    suffixes = []
    for joint in chain:
        joint_name = joint.split('_')
        suffix = '_'.join(joint_name[-2:])
        suffixes.append(suffix)
    return suffixes


def duplicate_base_joint(joint, petals):
    duplicate_chains = []

    for petal in petals:
        duplicate_joint = cmd.duplicate(joint, rc = 1)
        
        duplicate_chains.append(duplicate_joint)
    
    return duplicate_chains


def rename_joints(duplicates, suffixes, petals):
    new_base_joints = []

    for (petal, chain) in zip(petals, duplicates):
        print(chain)
        mesh_name = petal.capitalize()
        print(mesh_name)

        new_chain = []

        for (joint, suffix) in zip(chain, suffixes):
            prefix = joint.split('_')[0]
            new_name = '_'.join([prefix, mesh_name, suffix])

            print(joint + ' -> ' + new_name)

            new_name = cmd.rename(joint, new_name)

            new_chain.append(new_name)
        
        print(new_chain)

        new_base_joints.append(new_chain[0])

    return new_base_joints


def get_vertex_coordinates(petals, vertex): # pour ne pas dépendre du pointOnPolyconstraint
    coordinates = []
    test = []
    for petal in petals:
        anchor = petal + '.vtx[' + str(vertex) + ']'
        vertex_position = cmd.xform(anchor, t = 1, q = 1, ws = 1)
        vertex_normals = cmd.polyNormalPerVertex(anchor, q = 1, x = 1)

        # target_rotation = [vertex_normals[0], vertex_normals[1], vertex_normals[2]]
        coordinates.append([vertex_position, vertex_normals])
        test.append(vertex_normals)
    print('test = ' + str(test))

    return coordinates


def fais_des_locators(petals):
    locators = []
    for petal in petals:
        petal_id = petal[-2:]
        locator = cmd.spaceLocator(n = 'petale' + str(petal_id) + '_loc')
        locators.append(locator)
    return locators



def vertex_constraint_to_petal(joints, petals): # Diantre ce pointOnPolyConstraint ne marche absolument pas
    for (joint, petal) in zip(joints, petals):
        locator = cmd.spaceLocator()
        anchor = petal + '.vtx[' + str(anchor_vertex) + ']'
        print(anchor)
        constraint = cmd.pointOnPolyConstraint(anchor, locator, mo = 0, w = 1)
        # cmd.setAttr(constraint[0] + '.offsetRotateX', -135.0)


# Script
selection = cmd.ls(sl = 1)
base_joint = selection.pop(0)
petals = selection.copy()

chain = get_joint_chain(base_joint)
print(chain)

suffixes = get_chain_suffixes(chain)
print(suffixes)

duplicate_chains = duplicate_base_joint(base_joint, petals)
print(duplicate_chains)

new_joints = rename_joints(duplicate_chains, suffixes, petals)
print(new_joints)

locators = fais_des_locators(petals)
print(locators)

# print(str(new_joints)[1:-1])
# print(str(locators))
# jnt_group = cmd.group(str(new_joints)[1:-1], n = 'jnts')
# loc_group = cmd.group(str(locators)[1:-1], n = 'locs')

# vertex_coordinates = get_vertex_coordinates(petals, anchor_vertex)
# print(vertex_coordinates)

# vertex_constraint_to_petal(new_joints, petals)
# petals_anchor = vertex_constraint_to_petal(new_joints, petals)