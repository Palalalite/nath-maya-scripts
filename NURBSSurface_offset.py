# offset your NURBS ribbon, if there's ever an use case for it
import maya.cmds as cmd
import re

class SurfaceOffseter:
    selection = cmd.ls(sl = 1)
    surface = ''

    def __init__(self):
        self.winID = 'SurfaceOffseter'
        self.row_height = 24
        self.list_height = 100

        self.build_ui()


    # def start_targets(self):
    #     SurfaceOffseter.selection = cmd.ls(sl = 1)
    #     print('something selected')


    def update_selection(self):
        SurfaceOffseter.selection = cmd.ls(sl = 1)


    def update_targets(self):
        self.update_selection()
        if len(SurfaceOffseter.selection) > 0:
            if cmd.listRelatives(SurfaceOffseter.selection[0]):
                if cmd.objectType(cmd.listRelatives(SurfaceOffseter.selection[0])) == 'nurbsSurface':
                    SurfaceOffseter.surface = SurfaceOffseter.selection[0]
                else : SurfaceOffseter.surface = 'Not a surface'
        else:
            SurfaceOffseter.surface = 'None'
        
        cmd.text('surface_label', e = 1, label = 'Surface : ' + SurfaceOffseter.surface)


    def get_vertices(self, surface):
        vertices_flat = cmd.ls(surface + ".cv[:]", fl = 1)
        vertices = {}

        vertex_pattern = re.compile(r"\w+\.cv\[(\d*)\]\[(\d*)\]")
        u_max = int(vertex_pattern.search(vertices_flat[-1])[1])
        v_max = int(vertex_pattern.search(vertices_flat[-1])[2])

        for u in range(u_max+1):
            vertices[u] = {}
            for v in range(v_max+1):
                surf_vertex = surface + '.cv['+str(u)+']'+'['+str(v)+']'
                # print(surf_vertex)
                vertices[u][v] = cmd.xform(surf_vertex, q = 1, ws = 1, t = 1)
        #         print(vertices[u][v])
        # print(vertices)
        return vertices


    def offset_vertices(self, forward):
        vertices = self.get_vertices(self.surface)
        new_vertices = vertices.copy()

        if forward:
            print('FORWARD ' * 3)
            new_vertices[0] = vertices[len(vertices)-1]
            for u in vertices:
                # print('before : ' + str(vertices[u]))
                if u > 0:
                    new_vertices[u] = vertices[u-1]
                # print('after  : ' + str(new_vertices[u]))
                # print('*'*15)
        
        elif not forward:
            print('BACKWARD ' * 3)
            new_vertices[len(vertices)-1] = vertices[0]
            for u in vertices:
                # print('before : ' + str(vertices[u]))
                if u != len(vertices)-1:
                    new_vertices[u] = vertices[u+1]
                # print('after  : ' + str(new_vertices[u]))
                # print('*'*15)
        return new_vertices
    
    def apply_vertex_positions(self, forward):
        new_vertices = self.offset_vertices(forward)

        for u in new_vertices:
            for v in new_vertices[u]:
                surface_vtx = self.surface + '.cv['+str(u)+']['+str(v)+']'
                print(new_vertices[u][v])
                print(surface_vtx)
                cmd.xform(surface_vtx, ws = 1, t = new_vertices[u][v])



        # for key in new_vertices:
        #     print(key)

        # cmd.xform(orig, ws = 1, t = translates)


    # def get_skinCluster(geometry):
    #     shape = cmd.listRelatives(geometry, c = 1, s = 1, ni = 1)[0]
    #     print(shape)
    #     skin = cmd.listConnections(shape, type = 'skinCluster')
    #     return skin


    # def get_bound_joints(geometry):
    #     skin = get_skinCluster(geometry)
    #     joints = cmd.listConnections(skin, type = 'joint')
    #     joints = list(dict.fromkeys(joints)) # Remove duplicate joints
    #     print(joints)
    #     return joints


    # def get_vertices(geometry):
    #     vertices = cmd.ls(geometry + ".vtx[:]", fl = 1)
    #     return vertices


    # def get_control_vertices(surface):
    #     control_vertices = cmd.ls(surface + ".cv[:][:]", fl = 1)
    #     return control_vertices


    # def get_weights(geometry):
    #     weights = []
    #     skin = get_skinCluster(geometry)[0]
    #     vertices = get_vertices(geometry)
        
    #     for vertex in vertices:
    #         vertex_weights = cmd.skinPercent(skin, vertex, q = 1, v = 1)
    #         weights.append(vertex_weights)
        
    #     print(weights)
    #     return weights


    # def set_weights(source_weights, target_bound_joints, target_skin, target_vertices):
    #     for vertex, weight in zip(target_vertices, source_weights):
    #         print(vertex)
            
    #         joint_weight_pair = [(joint, influence) for joint, influence in zip(target_bound_joints, weight)]
    #         print(joint_weight_pair)
            
    #         cmd.skinPercent(target_skin, vertex, transformValue = joint_weight_pair)
    
    def build_ui(self):
        if cmd.window(self.winID, exists = 1): 
            cmd.deleteUI(self.winID)

        cmd.window(self.winID, s = 0, rtf = 1)

        # Window
        cmd.columnLayout()
        cmd.text('surface_label', l = 'Surface :', h = 32)
        cmd.separator()
        cmd.rowLayout(nc = 2)
        cmd.button(label = 'Forward', h = 32, w = 200, c = lambda x : self.apply_vertex_positions(forward=True))
        cmd.button(label = 'Backward', h = 32, w = 200, c = lambda x : self.apply_vertex_positions(forward=False))
        cmd.setParent('..')
        cmd.setParent('..')

        # Show window
        cmd.showWindow()
        
        # ScriptJobs
        # cmd.scriptJob(ct = ['SomethingSelected', self.start_targets], p = self.winID)
        cmd.scriptJob(e = ['SelectionChanged', self.update_targets], p = self.winID)


SurfaceOffseter()