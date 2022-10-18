bl_info = {
    "name": "Node Factory",
    "author" : "autoblender",
    "version": (0, 1),
    "blender" : (3, 2, 1),
    "location" : "View3D > NodeFactory",
    "description" : "Mass randomize & export geometry nodes",
    "warning" : "Please use on a copy of your blend file, just in case.",
    "wiki_url" : "",
    "category" : "3D View",
}

import bpy
#from . import NFFLoatProp
#from . import NFIntProp
#from . import NFBoolProp
from . import NodeFactory
#from . import NodeFactoryProperties
from . import NodeFactoryOutput
from . import NFBoolPanel
from . import NFIntPanel
from . import NFFloatPanel
        
def register():
    NodeFactory.register()
    NodeFactoryOutput.register()
    NFBoolPanel.register()
    NFIntPanel.register()
    NFFloatPanel.register()
    
def unregister():
    NodeFactory.unregister()
    NodeFactoryOutput.unregister()
    NFBoolPanel.unregister()
    NFIntPanel.unregister()
    NFFloatPanel.unregister()

if __name__ == "__main__":
    register()