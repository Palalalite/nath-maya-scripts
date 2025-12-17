import maya.cmds as cmd

# Sélectionner une chaîne de joints, puis sa modé de pétale correspondante (avant freeze transform), et lancer script pour les binder ensemble

# Functions
def regroup_joint_chains(joints):
    chains = []
    for joint in joints:
        chain = [joint]

        children = cmd.listRelatives(joint, ad = 1, ni = 1)
        children.reverse()

        for item in children:
            if cmd.objectType(item, isType = 'joint') and '_skn' in item:
                chain.append(item)
        
        chains.append(chain)
        
    return chains


def assign_chains_to_petal(chains, petals):
    for (chain, petal) in zip(chains, petals):
        cmd.skinCluster(chain, petal)
    

# Script
selection = cmd.ls(sl = 1)

petals = cmd.listRelatives(selection[0], c = 1, ni = 1)
base_joints = cmd.listRelatives(selection[1], c = 1, ni = 1)

print(petals)
print(base_joints)

chains = regroup_joint_chains(base_joints)
print(chains)


assign_chains_to_petal(chains, petals)