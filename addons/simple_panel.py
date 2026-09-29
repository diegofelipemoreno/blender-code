bl_info = {
    "name": "A Very Simple Panel",
    "author": "Diego Moreno",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "description": "Just show up a panel in the UI",
    "category": "Learning",
}

import bpy
from bpy.utils import previews
import os
import random

# global variable for icon storage
custom_icons = None

def add_random_location(objects, amount=1, do_axis=(True, True, True)):
    """Add units to the locations of given objects"""
    for ob in objects:
        for i in range(3):
            if do_axis[i]:
                loc = ob.location
                loc[i] += random.randint(-amount, amount)

def load_custom_icons():
    """Load icon from the add-on folder"""
    global custom_icons

    # Get directory of current file
    addon_path = os.path.dirname(__file__)
    img_file = os.path.join(addon_path, "icon_smile_64.png")

    pcoll = previews.new()
    
    # Intenta obtener la ruta del script actual
    try:
        addon_path = os.path.dirname(__file__)
    except NameError:
        # Si estás ejecutando en el Text Editor sin guardar el archivo en disco
        addon_path = bpy.path.abspath("//")

    img_file = os.path.join(addon_path, "icon_smile_64.png")

    pcoll = previews.new()

    if os.path.exists(img_file):
        # Load icon into preview collection
        pcoll.load("smile_face", img_file, 'IMAGE')
    else:
        print(f"[Warning] Image file not found: {img_file}")

    custom_icons = pcoll

def remove_custom_icons():
    """Clear Icons loaded from file"""
    global custom_icons

    if custom_icons:
        previews.remove(custom_icons)
        custom_icons = None

class OBJECT_PT_very_simple(bpy.types.Panel):
    """Creates a Panel in the object context of the
    properties editor"""
    bl_label = "A Very Simple Panel"
    bl_idname = "VERYSIMPLE_PT_layout"
    bl_space_type = 'PROPERTIES' # To change this panel to a different section for example axis just change to 'VIEW_3D'
    bl_region_type = 'WINDOW' # To change this panel to a different section for example axis just change to 'UI'
    bl_context = 'object'

    def draw(self, context):
        '''
        layout = self.layout    
        layout.label(text="A Very Simple Label", icon='INFO')
        layout.label(text="Isn't it great?", icon='QUESTION')

        # Accessing custom icons safely
        global custom_icons
        if custom_icons and "smile_face" in custom_icons:
            icon_id = custom_icons["smile_face"].icon_id
            layout.label(text="Smile", icon_value=icon_id)
        else:
            layout.label(text="Smile (Loading/Missing)", icon='ERROR')
        '''
        # using columns
        col = self.layout.column()
        col.label(text="A Very Simple Label", icon='INFO')

        # using row
        row = col.row()
        row.label(text="Isn't it great?", icon='QUESTION')
        row.label(text="Smile",icon='ERROR')

        # using box
        box = col.box()
        split = box.split(factor=0.3)
        left_col = split.column()
        right_col = split.column()
        for k, v in bl_info.items():
            if not v:
                # ignore empty entries
                continue
            left_col.label(text=k)
            right_col.label(text=str(v))

        # using grid
        col.label(text="Scene Objects:")
        grid = col.grid_flow(columns=2)
        for ob in context.scene.objects:
            #grid.label(text=ob.name, icon=f'OUTLINER_OB_{ob.type}')
            # layout item to set entry color
            item_layout = grid.column()
            item_layout.label(text=ob.name, icon=f'OUTLINER_OB_{ob.type}')
            item_layout.enabled = ob.select_get() 
            item_layout.alert = ob == context.object # Setting the alert it means the trick to show the objet selected. The object is been selected.

        # Using buttons in this case delete
        # Deletes the object that is selected
        # It is equivalent to invoking Object | Delete from the menu
        # col.operator(bpy.ops.object.delete.idname())
        num_selected = len(context.selected_objects)

        if num_selected > 0:
            op_txt = f"Delete {num_selected} object"
            if num_selected > 1:
                op_txt += "s"  # add plural 's'
            col.operator(bpy.ops.object.delete.idname(), text=op_txt)
        else:
            to_disable = col.column()
            to_disable.enabled = False
            to_disable.operator(bpy.ops.object.delete.idname(), text="Delete Selected")
        
        # This adds the button Add random Location (operator method)
        col.operator(TRANSFORM_OT_random_location.bl_idname)

class TRANSFORM_OT_random_location(bpy.types.Operator):
    """Add units to the locations of selected objects"""
    bl_idname = "transform.add_random_location"
    bl_label = "Add random Location"

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

def register():
    load_custom_icons()
    bpy.utils.register_class(OBJECT_PT_very_simple)
    bpy.utils.register_class(TRANSFORM_OT_random_location)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_very_simple)
    bpy.utils.unregister_class(TRANSFORM_OT_random_location)
    remove_custom_icons()

if __name__ == "__main__":
    register()