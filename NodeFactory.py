import bpy
import os
from bpy.props import PointerProperty
from collections import defaultdict

# on selecting new node tree
def update(self, context):
    node = self.Node
    print("Inputs")
    
    self.floatProps.clear()
    self.intProps.clear()
    self.boolProps.clear()
    
    for i in node.inputs:
        
        print(i.identifier)
        
        if type(i) == bpy.types.NodeSocketInterfaceFloat:
            new_item = self.floatProps.add()            
            new_item.name = i.name
            new_item.min = i.min_value
            new_item.max = i.max_value
            continue
        
        if type(i) == bpy.types.NodeSocketInterfaceInt:
            new_item = self.intProps.add()
            new_item.name = i.name
            new_item.min = i.min_value
            new_item.max = i.max_value
            continue
            
        if type(i) == bpy.types.NodeSocketInterfaceBool:
            new_item = self.boolProps.add()
            new_item.name = i.name
            continue
            

class NFFloatProp(bpy.types.PropertyGroup):
    name = ''
    randomize : bpy.props.BoolProperty(name="Randomize?", default=False)
    min : bpy.props.FloatProperty(name="Minimum Value", default=0)
    max : bpy.props.FloatProperty(name="Maximum Value", default=1)     

class NFIntProp(bpy.types.PropertyGroup):
    name = ''
    randomize : bpy.props.BoolProperty(name="Randomize?", default=False)
    min : bpy.props.IntProperty(name="Minimum Value", default=0)
    max : bpy.props.IntProperty(name="Maximum Value", default=1)     

class NFBoolProp(bpy.types.PropertyGroup):
    name = ''
    randomize : bpy.props.BoolProperty(name="Randomize bool?", default=False)
    

# the panel
class NodeFactory(bpy.types.Panel):
    bl_label = "Node Factory"
    bl_idname = "_PT_nodefactory"
    bl_context_mode = 'OBJECT'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Node Factory'
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        nf = scene.NodeFactoryP
        
        col = layout.column()
        
        col.label(text='Export Settings')
        col.prop(nf, "count")
        col.prop(nf, "outName")
        
        if not os.path.exists(nf.exportDir):
            col.label(text='This path does not exist!')
        
        col.prop(nf, "exportDir")
        col.prop(nf, "exportFormat")
        
        col.prop_search(nf,"Node", bpy.data, "node_groups")
        col.label(text='Source Object')
        col.prop_search(nf, "ModifierSource", context.scene, "objects") 
        
        col.prop(nf, "applyModifiers")
        
        if nf.applyModifiers:
            col.prop(nf, "exportTextures")
            
            if nf.exportTextures:
                col.prop(nf, "texSize")
                col.prop(nf, "diffuse")
                col.prop(nf, "ao")
                col.prop(nf, "roughness")
                col.prop(nf, "normal")
                col.prop(nf, "emission")
            
        if nf.ModifierSource is None:
            col.label(text='Select source object')
            col.label(text='to export')
        else:
            col.operator("nf.begin_export")
        
        #col.clear()
           


# addon config
class NodeFactoryProperties(bpy.types.PropertyGroup):
    count : bpy.props.IntProperty(name="Amount to Generate", default=10)
    outName : bpy.props.StringProperty(name="Name of Output", default="nfOut")
    exportDir : bpy.props.StringProperty(name="Export Destination", default="C:\\")
    
    exportFormat : bpy.props.EnumProperty(
        name= "Export Format",
        description = "What filetype should this be exported as",
        items = [('blend', ".blend", "save as .blend"),
                 ('obj', ".obj", "save as .obj"),
                 ('fbx', ".fbx", "save as .fbx")]
        )
    
    applyModifiers : bpy.props.BoolProperty(name="Apply Modifiers", default=True)
    exportTextures : bpy.props.BoolProperty(name="Export Textures")
    
    diffuse : bpy.props.BoolProperty(name="Diffuse")
    ao : bpy.props.BoolProperty(name="Ambient Occlusion")
    roughness : bpy.props.BoolProperty(name="Roughness")
    normal : bpy.props.BoolProperty(name="Normal")
    emission : bpy.props.BoolProperty(name="Emission")
    texSize : bpy.props.IntProperty(name="Texture Size", default=1024)
    
    Node : PointerProperty(type=bpy.types.GeometryNodeTree, update=update)
    ModifierSource : PointerProperty(type=bpy.types.Object)
    floatProps : bpy.props.CollectionProperty(type=NFFloatProp)
    intProps : bpy.props.CollectionProperty(type=NFIntProp)
    boolProps : bpy.props.CollectionProperty(type=NFBoolProp)
    
def register():
    bpy.utils.register_class(NFFloatProp)
    bpy.utils.register_class(NFIntProp)
    bpy.utils.register_class(NFBoolProp)
    bpy.utils.register_class(NodeFactory)
    bpy.utils.register_class(NodeFactoryProperties)
    bpy.types.Scene.NodeFactoryP = bpy.props.PointerProperty(type=NodeFactoryProperties)
    
def unregister():
    bpy.utils.unregister_class(NodeFactory)
    bpy.utils.unregister_class(NFFloatProp)
    bpy.utils.unregister_class(NFIntProp)
    bpy.utils.unregister_class(NFBoolProp)
    bpy.utils.unregister_class(NodeFactoryProperties)
    del bpy.types.Scene.NodeFactoryP
    

#if __name__ == "__main__":
#    register()
