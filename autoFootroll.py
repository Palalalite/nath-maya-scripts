# Just create footroll attributes and nodes

import maya.cmds as cmd

# Dictionnaries

footroll_attributes = {
    "footControls": {
        "name": "________",
        "type": "enum",
        "en": "Foot"
    },
    
    "footRoll": {
        "name": "footRoll",
        "type": "float",
        "minimum": -15,
        "maximum": 20,
        "defVal": 0
    },
    
    "bank": {
        "name": "bank",
        "type": "float",
        "defVal": 0
    },
    
    "orteil": {
        "name": "orteil",
        "type": "float",
        "defVal": 0,
    },
    
    "pli": {
        "name": "pli",
        "type": "float",
        "defVal": 0,
    },

    '''
    "cigare": {
        "name": "cigare",
        "type": "float",
        "defVal": 0,
    },
    '''

    "talon": {
        "name": "talon",
        "type": "float",
        "defVal": 0,
    },
    
    "talonBalayage": {
        "name": "talonBalayage",
        "type": "float",
        "defVal": 0,
    },
    
    "pointe": {
        "name": "pointe",
        "type": "float",
        "defVal": 0,
    },
    
    "pointeBalayage": {
        "name": "pointeBalayage",
        "type": "float",
        "defVal": 0,
    },
    
    "ecart": {
        "name": "ecart",
        "type": "float",
        "defVal": 0,
    },
    
    "options": {
        "name": "_______",
        "type": "enum",
        "en": "Roll Options"
    },
    
    "footrollTalon": {
        "name": "angleTalon",
        "type": "float",
        "defVal": -45
    },
    """ 
    "footrollCigare": {
        "name": "angleCigare",
        "type": "float",
        "defVal": 0
    },
     """
    "footrollPointe": {
        "name": "anglePointe",
        "type": "float",
        "defVal": 60
    },
    
    "footrollPli": {
        "name": "anglePli",
        "type": "float",
        "defVal": 30
    },
    
    "footrollSpread": {
        "name": "angleEcart",
        "type": "float",
        "defVal": -16
    }
}


nodes_data = {
    "_Roll_Talon_rmv": {
        "node_type": 'remapValue',
        "inputMin": 0,
        "inputMax": -15,
        "outputMin": 0,
        "outputMax": -45
    },
    
    "_Roll_Pli_01_rmv": {
        "node_type": 'remapValue',
        "inputMin": 0,
        "inputMax": 12.5,
        "outputMin": 0,
        "outputMax": 99
    },
    
    "_Roll_Pli_02_rmv": {
        "node_type": 'remapValue',
        "inputMin": 12.5,
        "inputMax": 20,
        "outputMin": 99,
        "outputMax": 0
    },
    
    "_Roll_Pointe_rmv": {
        "node_type": 'remapValue',
        "inputMin": 12.5,
        "inputMax": 20,
        "outputMin": 0,
        "outputMax": 99
    },
    
    "_Bank_clamp": {
        "node_type": 'clamp',
        "minR": -360.0,
        "maxG": 360.0
    },
    
    "_Pli_Orteils_rmv": {
        "node_type": 'remapValue',
        "outputMax": 6

    },
    
    "_Spread_Orteils_rmv": {
        "node_type": 'remapValue',
        "outputMax": 16
    },
    
    "_Footroll_Offset_pma": {
        "node_type": 'plusMinusAverage'
    },
    
    "_Pli_Offset_pma": {
        "node_type": 'plusMinusAverage'
    },
    
    "_orteils_pli_adl": {
        "node_type": 'addDoubleLinear'
    }
}


# Functions
def get_side(item):
    side = item[0][0]
    return side


def add_attributes(ik_foot_ctrl):
    target_controller = ik_foot_ctrl[0]

    for attribute in footroll_attributes:

        # NOTE : value = bigDictionnary[smolDictionnary].get("fieldName", value if fieldName is inexistant)
        name = footroll_attributes[attribute].get("name", "blank")
        type = footroll_attributes[attribute].get("type", "float")
        minimum = footroll_attributes[attribute].get("minimum", )
        maximum = footroll_attributes[attribute].get("maximum", )
        defVal = footroll_attributes[attribute].get("defVal", 0)
        output = footroll_attributes[attribute].get("output", )
        en = footroll_attributes[attribute].get("en", )

        if minimum and maximum:
            cmd.addAttr(longName = name, attributeType = type, min = minimum, max = maximum, dv = defVal, keyable = 1)

        elif en:
            cmd.addAttr(longName = name, keyable = 1, at = 'enum', en = en)
            cmd.setAttr(target_controller + "." + name, lock = 1)
        
        else:
            cmd.addAttr(longName = name, attributeType = type, dv = defVal, keyable = 1)
        
        if output:
            cmd.connectAttr(target_controller + "." + name, output)


def create_remap_nodes(prefix):
    nodes = []
    for item in nodes_data:
        name = prefix + item
        print(name)
        node_type = nodes_data[item].get("node_type", )
        inputMin = nodes_data[item].get("inputMin", 0)
        inputMax = nodes_data[item].get("inputMax", 0)
        outputMin = nodes_data[item].get("outputMin", 0)
        outputMax = nodes_data[item].get("outputMax", 0)
        
        node = cmd.createNode(node_type, n = name)

        """ 
        attributes_set = [inputMin, inputMax, outputMin, outputMax]
        
        for attribute in attributes_set:
            if attribute:
                cmd.setAttr(name + "." attribute, attribute)
        """

        if inputMin:
            cmd.setAttr(name + ".inputMin", inputMin)
            
        if inputMax:
            cmd.setAttr(name + ".inputMax", inputMax)
            
        if outputMin:
            cmd.setAttr(name + ".outputMin", outputMin)
            
        if outputMax:
            cmd.setAttr(name + ".outputMax", outputMax)
       
        nodes.append(node)

    return nodes


def make_into_set(name, suffix, items):
    print(name)
    print(items)
    cmd.select(items)
    set = cmd.sets(n = name + suffix)
    return set 


# Script
selection = cmd.ls(sl = 1)
add_attributes(selection)
prefix = 'D_Metatarse'
remap_nodes = create_remap_nodes(prefix)
make_into_set(prefix + '_footroll', '_nodes', remap_nodes)

# Pli 01 rmv into Pli 02 rmv
cmd.connectAttr(remap_nodes[1] + '.outValue', remap_nodes[2] + '.outputMin')

# Pli 02, Pointe, Talon rmv into Footroll Offset pma
cmd.connectAttr(remap_nodes[2] + '.outValue', remap_nodes[7] + '.input3D[0].input3Dx')
cmd.connectAttr(remap_nodes[3] + '.outValue', remap_nodes[7] + '.input3D[0].input3Dy')
cmd.connectAttr(remap_nodes[0] + '.outValue', remap_nodes[7] + '.input3D[0].input3Dz')

# Pli Orteils rmv into Orteils Pli adl
cmd.connectAttr(remap_nodes[5] + '.outValue', remap_nodes[9] + '.input1')

# Orteils Pli adl into Pli Offset pma
cmd.connectAttr(remap_nodes[9] + '.output', remap_nodes[8] + '.input3D[1].input3Dx')