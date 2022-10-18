import bpy

class NFBoolPanel(bpy.types.Panel):
    bl_label = "Bool Inputs"
    bl_idname = "_PT_nodefactory_bools"
    bl_context_mode = 'OBJECT'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Node Factory'
    bl_parent_id = '_PT_nodefactory'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        nf = context.scene.NodeFactoryP
        
        col = layout.column()
        
        for i in nf.boolProps:                            
            col.label(text=i.name)         
            col.prop(i, "randomize")        
            
def register():
    bpy.utils.register_class(NFBoolPanel)


def unregister():
    bpy.utils.unregister_class(NFBoolPanel)


#if __name__ == "__main__":
#    register()
