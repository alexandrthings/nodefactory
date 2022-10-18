import bpy
import bmesh
import random
import os
import time
import threading

from bpy.app.handlers import persistent
#from bl_operators.uvcalc_smart_project import main

from bpy.types import Operator



class NodeFactoryOutput(Operator):
    
    bl_label = "Generate & Export"
    bl_idname = "nf.begin_export"
    
        # as far as im aware putting it in a thread and waiting is the only way to proc an update reliably
    def execute(self, context):
        # make object and add modifier
        # mesh = bpy.data.meshes.new('Output_Mesh')
        #output_object = bpy.data.objects.new("NFOutputObject", bpy.data.meshes.new('Output_Mesh'))
        
        #if bpy.data.objects.contains('Cube'):
            
        original_path = bpy.data.filepath
        print(original_path)
        
        # create workfile so we can make mincemeat out of it without worrying
        workfile_path = os.path.join(os.path.dirname(original_path), "workfile.blend")
        bpy.ops.wm.save_as_mainfile(filepath=workfile_path)
            
        
        if bpy.context.scene.NodeFactoryP.ModifierSource is None:
            if bpy.data.objects['Cube'] is None:
                bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0,0,0), scale=(1,1,1))
                
            object = bpy.data.objects['Cube']
            bpy.context.scene.NodeFactoryP.ModifierSource = object
        else:
            object = bpy.context.scene.NodeFactoryP.ModifierSource
            
        #if object not in bpy.context.view_layer.objects:
        #bpy.context.view_layer.objects.add(object)
            
        object.select_set(True)
            
        mats = set()
        for m in object.material_slots:
            mats.add(m.material)
            
        bpy.context.view_layer.objects.active = object
            
        bpy.ops.object.mode_set(mode='OBJECT')
        
        if "NodeFactory Nodes" not in object.modifiers:
            modifier = object.modifiers.new(name="NodeFactory Nodes", type='NODES')
            
            # whatever just move it up 100 times
            for l in range(0,100):
                bpy.ops.object.modifier_move_up(modifier="NodeFactory Nodes")
            
        else:
            modifier = object.modifiers["NodeFactory Nodes"]
            
        nf = bpy.context.scene.NodeFactoryP
        node = bpy.context.scene.NodeFactoryP.Node
        boolRandoms = bpy.context.scene.NodeFactoryP.boolProps
        floatRandoms = bpy.context.scene.NodeFactoryP.floatProps
        intRandoms = bpy.context.scene.NodeFactoryP.intProps
            
        #random_params = bpy.context.scene.NodeFactory
            
        modifier.node_group = node
            
        #idBase = "Input_"
        toExportCount = bpy.context.scene.NodeFactoryP.count
            
        # copy object
        bpy.ops.view3d.copybuffer()
            
        for exportIndex in range(1, toExportCount+1):
            
            object.select_set(True)
            bpy.context.view_layer.objects.active = object
            
            # Randomize input parameters
            for i in node.inputs:
                
                id = i.identifier
                print (id)
                    
                for f in range(0, len(floatRandoms)):
                    if (floatRandoms[f].name == i.name) and floatRandoms[f].randomize:
                        print(id)
                        modifier[id] = float(random.randrange(int(floatRandoms[f].min), int(floatRandoms[f].max)))
                        print(modifier[id])
                            
                for f in range(0, len(intRandoms)):
                    if (intRandoms[f].name == i.name) and intRandoms[f].randomize:
                        print(id)
                        modifier[id] = int(random.randrange(intRandoms[f].min, intRandoms[f].max))
                        print(modifier[id])
                     
                for b in range(0, len(boolRandoms)):
                    if (boolRandoms[b].name == i.name) and boolRandoms[b].randomize:
                        print(id)
                        modifier[id] = random.randrange(0, 1) > 0
                        print(modifier[id])
                
             # Export dir
            path = bpy.context.scene.NodeFactoryP.exportDir
            name = bpy.context.scene.NodeFactoryP.outName + str(exportIndex)
                
            thisExportPath = os.path.join(path, name)
            
            print(thisExportPath + "\\" + name)
                
            if not os.path.exists(thisExportPath):
                os.mkdir(thisExportPath)
                
            if nf.exportFormat == 'blend':
                bpy.ops.wm.save_as_mainfile(filepath=thisExportPath + "\\" + name + ".blend")
            
            Update3DViewPorts()
            
            # Apply Modifiers?
            if nf.applyModifiers:             
                bpy.ops.object.convert(target='MESH')
                #for modifier in object.modifiers:
                #    print(modifier.name)
                #    bpy.ops.object.modifier_apply(modifier=modifier.name)

                #    

                Update3DViewPorts()

                print(bpy.context.scene.statistics(bpy.context.view_layer))

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')                    
                bpy.ops.uv.smart_project()
                bpy.ops.object.mode_set(mode='OBJECT')

            Update3DViewPorts()
            
            bpy.context.object.data.materials.clear()
            
            for m in mats:
                bpy.context.object.data.materials.append(m)
            
            # Bake textures? 
            if nf.applyModifiers and nf.exportTextures:
                    
                obj = bpy.context.active_object
                           
                print(obj)
                                    
                # thanks noob cat from stackexchange

                # You can choose your texture size (This will be the de bake image)
                res = bpy.context.scene.NodeFactoryP.texSize
                
                image_name = obj.name + '_BakedTexture'
                img = bpy.data.images.new(image_name,res,res)
                bpy.context.view_layer.objects.active = obj
                
                # Due to the presence of any multiple materials, it seems necessary to iterate on all the materials, and assign them a node + the image to bake.
                matcount = 0
                for mat in obj.data.materials:
                        
                    if mat is None: # incase ther are none
                        continue

                    mat.use_nodes = True #Here it is assumed that the materials have been created with nodes, otherwise it would not be possible to assign a node for the Bake, so this step is a bit useless
                    nodes = mat.node_tree.nodes
                    texture_node =nodes.new('ShaderNodeTexImage')
                    texture_node.name = 'Bake_node'
                    texture_node.select = True
                    nodes.active = texture_node
                    texture_node.image = img #Assign the image to the node
                    matcount += 1
                    
                # if theres somehow no materials baking crashes blender
                if matcount > 0:
                    bpy.context.scene.render.engine = 'CYCLES'
                    bpy.context.scene.cycles.device = 'GPU'
                        
                    bpy.context.scene.render.bake.use_pass_direct = False
                    bpy.context.scene.render.bake.use_pass_indirect = False
                    bpy.context.scene.render.bake.use_pass_color = True
                        
                    # bake diffuse texture
                    if nf.diffuse:
                        bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')

                        dest_path = thisExportPath + "\\" + name + "_diffuse.png" 
                        img.save_render(filepath=dest_path)
                            
                    # bake roughness texture
                    if nf.roughness:
                        bpy.ops.object.bake(type='ROUGHNESS', save_mode='EXTERNAL')

                        dest_path = thisExportPath + "\\" + name + "_roughness.png" 
                        img.save_render(filepath=dest_path)
                            
                    # bake normal texture
                    if nf.normal:
                        bpy.ops.object.bake(type='NORMAL', save_mode='EXTERNAL')

                        dest_path = thisExportPath + "\\" + name + "_normal.png" 
                        img.save_render(filepath=dest_path)
                            
                    # bake emission texture
                    if nf.emission:
                        bpy.ops.object.bake(type='EMIT', save_mode='EXTERNAL')
                        dest_path = thisExportPath + "\\" + name + "_emission.png" 
                        img.save_render(filepath=dest_path)
                        
                    # bake emission texture
                    if nf.ao:
                        bpy.ops.object.bake(type='AO', save_mode='EXTERNAL')
                        dest_path = thisExportPath + "\\" + name + "_ao.png" 
                        img.save_render(filepath=dest_path)
                        
                    #In the last step, we are going to delete the nodes we created earlier
                    for mat in obj.data.materials:
                        if mat is None:
                            continue
                        
                        for n in mat.node_tree.nodes:
                            if n.name == 'Bake_node':
                                mat.node_tree.nodes.remove(n)
            
            # Export depending on selected format
            if nf.exportFormat == 'blend':
                bpy.ops.wm.save_mainfile()
            if nf.exportFormat == 'obj':
                bpy.ops.export_scene.obj(filepath=thisExportPath + "\\" + name + ".obj", use_selection = True)
            if nf.exportFormat == 'fbx':
                bpy.ops.export_scene.fbx(filepath=thisExportPath + "\\" + name + ".fbx", use_selection = True)
            #print(type(output_object))
            
            # delete applied modifiers object
            bpy.ops.object.delete(use_global=True)
            
            # paste saved object
            bpy.ops.view3d.pastebuffer()
                
            # make the pasted object the main one
            object = context.selected_objects[0]
            modifier = object.modifiers["NodeFactory Nodes"]
            nf.ModifierSource = object
                
         # delete work file
        os.remove(workfile_path)
        
        workfile_path = workfile_path + '1'
        
        os.remove(workfile_path) 
        # open original
        bpy.ops.wm.open_mainfile(filepath=original_path)
        
        return {'FINISHED'}

        
def Update3DViewPorts():
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
    bpy.ops.wm.save_mainfile()
    
def register():
    bpy.utils.register_class(NodeFactoryOutput)


def unregister():
    bpy.utils.unregister_class(NodeFactoryOutput)


#if __name__ == "__main__":
#    register()
