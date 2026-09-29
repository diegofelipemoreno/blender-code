
bl_info = {
    "name": "Collector",
    "author": "Diego Moreno",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "description": "Create collections for object types",
    "category": "Object",
}


import bpy

# OT means Operator Types the inherance class.
# OBJECT_OT means the action to do something in blender
class OBJECT_OT_collector_types(bpy.types.Operator):
    """Create collections based on objects types"""
    bl_idname = "object.pckt_type_collector"
    bl_label = "Create Type Collections"
    bl_options = {'REGISTER', 'UNDO'}  # Enables Ctrl+Z undo

    @classmethod
    def poll(cls, context):
        return len(context.scene.objects) > 0

    def execute(self, context):
        # 1. Create or get existing collections or is for Avoiding duplicate collections
        mesh_cl = bpy.data.collections.get("Mesh") or bpy.data.collections.new("Mesh")
        light_cl = bpy.data.collections.get("Light") or bpy.data.collections.new("Light")
        cam_cl = bpy.data.collections.get("Camera") or bpy.data.collections.new("Camera")

        # 2. Link collections to current scene root if not already linked
        for cl in (mesh_cl, light_cl, cam_cl):
            if cl.name not in context.scene.collection.children:
                # link Lo que hace: Toma esa carpeta creada en la memoria y la conecta físicamente al árbol de tu escena actual (la Colección Escena principal / Outliner).
                context.scene.collection.children.link(cl)

        # 3. Move objects safely
        for ob in list(context.scene.objects):
            target_cl = None
            if ob.type == 'MESH':
                target_cl = mesh_cl
            elif ob.type == 'LIGHT':
                target_cl = light_cl
            elif ob.type == 'CAMERA':
                target_cl = cam_cl

            if target_cl:
                # Unlink from all current collections first
                for col in ob.users_collection:
                    col.objects.unlink(ob) # Elimina el vínculo previo
                # Link to the target collection
                target_cl.objects.link(ob) # Asigna el nuevo vínculo

        return {'FINISHED'}


# Panel defined to draw inside the "Item" tab
# OBJECT_PT means Panel. The visual interface container
class OBJECT_PT_collector_item_panel(bpy.types.Panel):
    bl_label = "Type Collector"
    bl_idname = "OBJECT_PT_collector_item_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'  # Places it in the Item tab of the N sidebar

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_collector_types.bl_idname, icon='OUTLINER_COLLECTION')

classes = (
    OBJECT_OT_collector_types,
    OBJECT_PT_collector_item_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()