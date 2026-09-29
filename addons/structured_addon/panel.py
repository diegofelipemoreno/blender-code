import bpy
from . import img_loader
from . import operators

class OBJECT_PT_structured(bpy.types.Panel):
    """Creates a Panel in the object context"""
    bl_label = "A Modular Panel"
    bl_idname = "MODULAR_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'
    #max_objects = 3  # limit displayed list to 3 objects

    def render_delete_cta(self, context):
        layout = self.layout
        num_selected = len(context.selected_objects)

        if num_selected > 0:
            op_txt = f"Delete {num_selected} object"
            if num_selected > 1:
                op_txt += "s"  # add plural 's'
            layout.operator(operators.OBJECT_OT_delete_location.bl_idname, text=op_txt)
        else:
            to_disable = layout.column()
            to_disable.enabled = False
            layout.operator(operators.OBJECT_OT_delete_location.bl_idname)

    def render_objects(self, context):
        layout = self.layout
        icons = img_loader.get_icons_collection()
        row = layout.row(align=True)
        row.label(text="Scene Objects",
                  icon_value=icons['pack_64'].icon_id)
        row.label(text="Carita Felizs",
                  icon_value=icons["smile_64"].icon_id)
        grid = layout.grid_flow(columns=2,
                                row_major=True)
        print('__package__', __package__) # = __package__ structured_addon
        add_on = context.preferences.addons[__package__]
        preferences = add_on.preferences
        for i, ob in enumerate(context.scene.objects):
            if i >= preferences.max_objects:
                grid.label(text="...")
                break
            # display object name and type icon
            item_layout = grid.column()

            item_layout.label(text=ob.name, icon=f'OUTLINER_OB_{ob.type}')
            item_layout.enabled = ob.select_get() 
            item_layout.alert = ob == context.object # Setting the alert it means the trick to show the objet selected. The object is been selected.


    def draw(self, context):
        layout = self.layout

        self.render_objects(context)
        # displays or render the random button into the panel
        layout.operator(operators.TRANSFORM_OT_random_location.bl_idname)
        # displays or render the delete button into the panel
        #layout.operator(bpy.ops.object.delete.idname())
        self.render_delete_cta(context)

def register_classes():
    bpy.utils.register_class(OBJECT_PT_structured)

def unregister_classes():
    bpy.utils.unregister_class(OBJECT_PT_structured)
