import pymel.core as pm

# Select TARGETS first, and SOURCE last.
source = pm.selected()[-1]
targets = pm.selected()[0:-1]

for target in targets:
    shapeType = pm.nodeType(target.getShape())
    if shapeType in ["nurbsSurface", "nurbsCurve"]:
        pm.copySkinWeights(source, target.cv, noMirror=True, surfaceAssociation='closestPoint', ia=['oneToOne','name'])
    else:
        pm.copySkinWeights(source, target, noMirror=True, surfaceAssociation='closestPoint', ia=['oneToOne','name'])