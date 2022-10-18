import bpy

class NFFloatPanel(bpy.types.Panel):
    bl_label = "Float Inputs"
    bl_idname = "_PT_nodefactory_floats"
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
        
        for i in nf.floatProps:                            
            col.label(text=i.name)         
            col.prop(i, "randomize")
            col.prop(i, "min")
            col.prop(i, "max")
        
def register():
    bpy.utils.register_class(NFFloatPanel)


def unregister():
    bpy.utils.unregister_class(NFFloatPanel)


#if __name__ == "__main__":
#    register()
