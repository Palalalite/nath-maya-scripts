import maya.cmds as cmd

# Functions
def turn_into_surface(geometry):
    print(geometry)
    
    # Select loop's starting edges
    cross_edges = cmd.polySelect(geometry, er = 3)
    print (cross_edges)
    
    # Select each border loop
    curves = []
    for edge in cross_edges:
        border_edges = cmd.polySelect(geometry, elb = edge)
        curve = cmd.polyToCurve()
        curves.append(curve[0])

    surface = cmd.loft(curves, n = geometry[0] + '_proxy', ch = 1, u = 1, c = 0, ar = 0, d = 3, ss = 1, rn = 0, po = 0, rsn = 1)
    cmd.makeIdentity(surface)
    [cmd.delete(curve) for curve in curves]
    
    return surface
    

def turn_into_geometry(surface):
    surface = surface[0]
    geometry_2 = cmd.nurbsToPoly(surface, n = surface + '_skin', f = 3)
    cmd.makeIdentity(geometry_2)
    return geometry_2


# Select Target THEN Source
selection = cmd.ls(sl = 1)
geometry = selection

surface = turn_into_surface(geometry)

geometry_2 = turn_into_geometry(surface)

cmd.hide(geometry)