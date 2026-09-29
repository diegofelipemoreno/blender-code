import bpy
import random

def add_random_location(objects, amount=1, do_axis=(True, True, True)):
    """Add units to the locations of given objects"""
    for ob in objects:
        for i in range(3):
            if do_axis[i]:
                loc = ob.location
                loc[i] += random.randint(-amount, amount)

class TRANSFORM_OT_random_location(bpy.types.Operator):
    """Add units to the locations of selected objects"""
    bl_idname = "transform.add_random_location"
    bl_label = "Add random Location"
    bl_options = {'REGISTER', 'UNDO'}  # Enables Ctrl+Z undo support

    amount: bpy.props.IntProperty(name="Amount",
                                  min=0,  # prevent negative values to avoid errors in add_random_location()
                                  default=1)
    axis: bpy.props.BoolVectorProperty(
                                name="Displace Axis",
                                default=(True, True, True),
                                subtype='XYZ'
                                )

    @classmethod
    def poll(cls, context):
        return context.selected_objects 
        # comprueba si hay al menos un objeto seleccionado en la escena.
        # Si hay objetos seleccionados: El botón en el panel estará activo y cliqueable.
        # Si la lista está vacía ([] se evalúa como False): El botón aparecerá en gris (desactivado) en la interfaz para evitar errores.

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        # Es el método que se activa inmediatamente cuando el usuario hace clic en el botón. Su función es preparar la interfaz o solicitar confirmación antes de aplicar la lógica pesada.
        # Usually, we don’t need to define it, but in this case, we use it to tell Blender we want to display and edit the operator properties

    def execute(self, context):
        add_random_location(context.selected_objects,
                            self.amount,
                            self.axis)
        return {'FINISHED'}

class OBJECT_OT_delete_location(bpy.types.Operator):
    """Deletes the selected objects safely with confirmation"""
    bl_idname = "object.elevator_delete_selected"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects)
        # comprueba si hay al menos un objeto seleccionado en la escena.
        # Si hay objetos seleccionados: El botón en el panel estará activo y cliqueable.
        # Si la lista está vacía ([] se evalúa como False): El botón aparecerá en gris (desactivado) en la interfaz para evitar errores.

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
        # Es el método que se activa inmediatamente cuando el usuario hace clic en el botón. Su función es preparar la interfaz o solicitar confirmación antes de aplicar la lógica pesada.
        # Usually, we don’t need to define it, but in this case, we use it to tell Blender we want to display and edit the operator properties

    def execute(self, context):
        bpy.ops.object.delete()  # Actually delete the selected objects
        return {'FINISHED'}

def register_classes():
    bpy.utils.register_class(TRANSFORM_OT_random_location)
    bpy.utils.register_class(OBJECT_OT_delete_location)

def unregister_classes():
    bpy.utils.unregister_class(TRANSFORM_OT_random_location)
    bpy.utils.unregister_class(OBJECT_OT_delete_location)

if __name__ == "__main__":
    register_classes()