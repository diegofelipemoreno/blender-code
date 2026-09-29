
bl_info = {
    "name": "Elevator",
    "author": "Diego Moreno",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Move objects up to a minimum height",
    "category": "Object",
}


import bpy
from bpy.props import FloatProperty

# FUNCIÓN PARA EL MENÚ CONTEXTUAL (Clic derecho sobre el objeto)
def draw_elevator_menu(self, context):
    self.layout.operator(OBJECT_OT_elevator.bl_idname, icon='OUTLINER_COLLECTION')

class OBJECT_OT_elevator(bpy.types.Operator):
    """Move Objects up to a given height"""
    bl_idname = "object.pckt_floor_transform"
    bl_label = "Elevate Objects"
    bl_options = {'REGISTER', 'UNDO'}  # Enables Ctrl+Z undo
    floor: FloatProperty(name="Floor", default=0)

    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects) > 0


    def execute(self, context):
        for ob in context.selected_objects:
            if ob.location.z > self.floor:
                continue
            ob.location.z = self.floor
            
        return {'FINISHED'}

# Panel defined to draw inside the "Item" tab
class OBJECT_PT_draw_elevator_item(bpy.types.Panel):
    bl_label = "Elevate Objects"
    bl_idname = "OBJECT_PT_draw_elevator_item"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'  # Places it in the Item tab of the N sidebar

    # El panel (PT) usa la función draw() para colocar un botón en pantalla que, al presionarse, llama al operador (OT) para ejecutar la acción.
    # El método para dibujar paneles SIEMPRE debe llamarse "draw"
    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_elevator.bl_idname, icon='OUTLINER_COLLECTION')

def register():
    # add operator and menu item
    bpy.utils.register_class(OBJECT_OT_elevator)
    object_menu = bpy.types.VIEW3D_MT_object_context_menu
    object_menu.append(draw_elevator_menu)

def unregister():
    # remove operator and menu item
    bpy.utils.unregister_class(OBJECT_OT_elevator)
    object_menu = bpy.types.VIEW3D_MT_object_context_menu
    object_menu.remove(draw_elevator_menu)

if __name__ == "__main__":
    register()