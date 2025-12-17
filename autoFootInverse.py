import maya.cmds as cmd

# Avoir crée au préalable, les joints Orteils et joints Inverse, les ikHandles Pointe Inv et Pli Inv, et les avoir freeze
# /!\ Nomenclature-rigide /!\ 

# User values
forward = "X"
swipe = "Z"
bank = "Y"

selection = cmd.ls(sl = 1)

ikFootCtrl = selection[0]
print(ikFootCtrl)

side = ikFootCtrl[0]


# Dictionnary of attributes to add to ikFootCtrl
attributes = {
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
        #"output": side + "_Orteils_03_GRP.rotate" + forward
    },
    
    "pli": {
        "name": "pli",
        "type": "float",
        "defVal": 0,
        #"output": side + "_INVPli_01_jnt.rotateAxis" + forward
    },
    
    "cigare": {
        "name": "cigare",
        "type": "float",
        "defVal": 0,
        #"output": side + "_INVTalon_01_jnt.rotateAxis" + forward
    },
    
    "talon": {
        "name": "talon",
        "type": "float",
        "defVal": 0,
        #"output": side + "_INVTalon_01_jnt.rotateAxis" + forward
    },
    
    "talonBalayage": {
        "name": "talonBalayage",
        "type": "float",
        "defVal": 0,
        #"output": side + "_INVTalon_01_jnt.rotateAxis" + swipe
    },
    
    "pointe": {
        "name": "pointe",
        "type": "float",
        "defVal": 0,
        #"output": side + "_INVPointe_01_jnt.rotateAxis" + forward
    },
    
    "pointeBalayage": {
        "name": "pointeBalayage",
        "type": "float",
        "defVal": 0,
        #"output": side + "_INVPointe_01_jnt.rotateAxis" + swipe
    },
    
    "ecart": {
        "name": "ecart",
        "type": "float",
        "defVal": 0,
        #"output": side + "_INVPointe_01_jnt.rotateAxis" + swipe
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
    
    "footrollCigare": {
        "name": "angleCigare",
        "type": "float",
        "defVal": 0
    },
    
    "footrollPointe": {
        "name": "anglePointe",
        "type": "float",
        "defVal": 60
    },
    
    "footrollPli": {
        "name": "anglePli",
        "type": "float",
        "defVal": 30
    }
}


for attribute in attributes:
    #value = bigDictionnary[smolDictionnary].get("fieldName", value if fieldName is blank)
    name = attributes[attribute].get("name", "blank")
    type = attributes[attribute].get("type", "float")
    minimum = attributes[attribute].get("minimum", )
    maximum = attributes[attribute].get("maximum", )
    defVal = attributes[attribute].get("defVal", 0)
    output = attributes[attribute].get("output", )
    en = attributes[attribute].get("en", )

    cmd.select(ikFootCtrl, r = 1)
    
    if minimum and maximum:
        cmd.addAttr(longName = name, attributeType = type, min = minimum, max = maximum, dv = defVal, keyable = 1)

    elif en:
        cmd.addAttr(longName = name, keyable = 1, at = 'enum', en = en)
        cmd.setAttr(ikFootCtrl + "." + name, lock = 1)
        
    else:
        cmd.addAttr(longName = name, attributeType = type, dv = defVal, keyable = 1)
    
    if output:
        cmd.connectAttr(ikFootCtrl + "." + name, output)


#footRoll Remap Setup
remapValues = {
    side + "_INVTalon_rmv": {
        "inputMin": 0,
        "inputMax": -15,
        "outputMin": 0,
        "outputMax": -45
    },
    
    side + "_INVPli_01_rmv": {
        "inputMin": 0,
        "inputMax": 12.5,
        "outputMin": 0
    },
    
    side + "_INVPli_02_rmv": {
        "inputMin": 12.5,
        "inputMax": 20,
        "outputMax": 0
    },
    
    side + "_INVPointe_rmv": {
        "inputMin": 12.5,
        "inputMax": 20,
        "outputMin": 0
    }
}


remapNodes = []

for item in remapValues:
    name = item
    inputMin = remapValues[item].get("inputMin", )
    inputMax = remapValues[item].get("inputMax", )
    outputMin = remapValues[item].get("outputMin", )
    outputMax = remapValues[item].get("outputMax", )
    
    node = cmd.createNode("remapValue", n = name)
    
    cmd.setAttr(name + ".inputMin", inputMin)
    cmd.setAttr(name + ".inputMax", inputMax)
    
    if outputMin:
        cmd.setAttr(name + ".outputMin", outputMin)
        
    elif outputMax:
        cmd.setAttr(name + ".outputMax", outputMax)
    
    remapNodes.append(node)
    
print(remapNodes)

#footRoll Talon
cmd.connectAttr(ikFootCtrl + ".angleTalon", remapNodes[0] + ".outputMax")
cmd.connectAttr(ikFootCtrl + ".footRoll", remapNodes[0] + ".inputValue")

cmd.connectAttr(remapNodes[0] + ".outValue", side + "_INVTalon_01_jnt.rotate" + forward)

#footRoll Pli
cmd.connectAttr(ikFootCtrl + ".anglePli", remapNodes[1] + ".outputMax")
cmd.connectAttr(ikFootCtrl + ".footRoll", remapNodes[1] + ".inputValue")

cmd.connectAttr(remapNodes[1] + ".outValue", remapNodes[2] + ".outputMin")
cmd.connectAttr(ikFootCtrl + ".footRoll", remapNodes[2] + ".inputValue")

cmd.connectAttr(remapNodes[2] + ".outValue", side + "_INVPli_01_jnt.rotate" + forward)

#footRoll Pointe
cmd.connectAttr(ikFootCtrl + ".anglePointe", remapNodes[3] + ".outputMax")
cmd.connectAttr(ikFootCtrl + ".footRoll", remapNodes[3] + ".inputValue")

cmd.connectAttr(remapNodes[3] + ".outValue", side + "_INVPointe_01_jnt.rotate" + forward)


#foot Bank
bankClamp = cmd.createNode("clamp", n = side + "_INVBank_01_CLM")
cmd.setAttr(bankClamp + ".minR", 0.0)
cmd.setAttr(bankClamp + ".minG", -360.0)
cmd.setAttr(bankClamp + ".maxR", 360.0)
cmd.setAttr(bankClamp + ".maxG", 0.0)
cmd.connectAttr(ikFootCtrl + ".bank", bankClamp + ".inputR")
cmd.connectAttr(ikFootCtrl + ".bank", bankClamp + ".inputG")
cmd.connectAttr(bankClamp + ".outputR", side + "_INVBank_02_jnt.rotate" + bank)
cmd.connectAttr(bankClamp + ".outputG", side + "_INVBank_01_jnt.rotate" + bank)


#ikHandles Pli et Pointe
chevilleJnt = side + "_Cheville_01_jnt"
pliJnt = side + "_Pli_01_jnt"
pointeJnt = side + "_Pointe_01_jnt"

ikPli = cmd.ikHandle(sj = chevilleJnt, ee = pliJnt, n = side + '_Pli_ikH', sol = 'ikSCsolver', ap = 0, eh = 1, see = 1, s = 0, p = 1, w = 1, pw = 1)
ikPointe = cmd.ikHandle(sj = pliJnt, ee = pointeJnt, n = side + '_Pointe_ikH', sol = 'ikSCsolver', ap = 0, eh = 1, see = 1, s = 0, p = 1, w = 1, pw = 1)

cmd.parent(ikPli[0], side + "_INVPli_01_jnt")
cmd.parent(ikPointe[0], side + "_INVPointe_01_jnt")


#Orteils follow
cmd.parentConstraint(side + "_Pli_01_jnt", side + "_Orteils_02_GRP", mo = 0)


#Switch into ikBlend
pliInterpolation = cmd.createNode("remapValue", n = side + "_PliInterpolation_01_rmv")
pointeInterpolation = cmd.createNode("remapValue", n = side + "_PointeInterpolation_01_rmv")

curvePoints = {
    "0": {
        "position": 0,
        "floatValue": 0
    },
    
    "1": {
        "position": 0.668,
        "floatValue": 0.045
    },
    
    "2": {
        "position": 0.916,
        "floatValue": 0.192
    },
    
    "3": {
        "position": 0.972,
        "floatValue": 0.556
    },
    
    "4": {
        "position": 1.0,
        "floatValue": 1.0
    }
}

for point in curvePoints:
    id = point
    position = curvePoints[point].get("position", 0)
    floatValue = curvePoints[point].get("floatValue", 0)
    
    cmd.setAttr(pliInterpolation + ".value[" + point + "].value_Position", position)
    cmd.setAttr(pliInterpolation + ".value[" + point + "].value_FloatValue", floatValue)
    cmd.setAttr(pliInterpolation + ".value[" + point + "].value_Interp", 1)
    
    cmd.setAttr(pointeInterpolation + ".value[" + point + "].value_Position", position)
    cmd.setAttr(pointeInterpolation + ".value[" + point + "].value_FloatValue", floatValue)
    cmd.setAttr(pointeInterpolation + ".value[" + point + "].value_Interp", 1)

cmd.connectAttr(side + "_Jambe_reverse.outputX", pliInterpolation + ".inputValue")
cmd.connectAttr(side + "_Jambe_reverse.outputX", pointeInterpolation + ".inputValue")

cmd.connectAttr(pliInterpolation + ".outValue", ikPli[0] + ".ikBlend")
cmd.connectAttr(pointeInterpolation + ".outValue", ikPointe[0] + ".ikBlend")


#AnimBlend Rotation Node for resetting the joint Pli's rotates when FK
animBlendRotate = cmd.createNode("animBlendNodeAdditiveRotation", n = side + "_JambeSwitch_ABNAR")

cmd.connectAttr(side + "_JambeSwitch_01_CTRL.SwitchIKFK", animBlendRotate + ".weightA")
cmd.connectAttr(side + "_Jambe_reverse.outputX", animBlendRotate + ".weightB")

cmd.connectAttr(animBlendRotate + ".output", pliJnt + ".rotate")


#ikHandles visibility off
cmd.setAttr(ikPli[0] + ".v", 0)
cmd.setAttr(ikPointe[0] + ".v", 0)