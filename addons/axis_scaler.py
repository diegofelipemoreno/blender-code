
bl_info = {
    "name": "Quick Axis Scaler",
    "author": "Diego Moreno",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Right Click Menu / N-Panel > Item",
    "description": "Scale selected objects along a specific axis by a configured factor",
    "category": "Object",
}

import bpy

class OBJECT_OT_quick_axis_scale(bpy.types.Operator):
    """Escala el objeto seleccionado en un eje específico por un factor configurable"""

    bl_idname = "object.quick_axis_scale"
    bl_label = "Quick Axis Scale"
    bl_options = {"REGISTER", "UNDO"}

    # Propiedades configurables
    axis: bpy.props.EnumProperty(
        name="Eje",
        description="Eje en el cual aplicar la escala",
        items=[
            ("X", "X Axis", "Escalar en el eje X"),
            ("Y", "Y Axis", "Escalar en el eje Y"),
            ("Z", "Z Axis", "Escalar en el eje Z"),
        ],
        default="Z",
    )

    scale_factor: bpy.props.FloatProperty(
        name="Factor de Escala",
        description="Multiplicador de escala a aplicar",
        default=2.0,
        min=0.001,
        soft_max=10.0,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def execute(self, context):
        for obj in context.selected_objects:
            if self.axis == "X":
                obj.scale.x *= self.scale_factor
            elif self.axis == "Y":
                obj.scale.y *= self.scale_factor
            elif self.axis == "Z":
                obj.scale.z *= self.scale_factor

        self.report(
            {"INFO"},
            "Objeto(s) escalado(s) en eje {} por factor {}".format(
                self.axis, self.scale_factor
            ),
        )
        return {"FINISHED"}


# Panel N (Sidebar > Item > Quick Scale)
class OBJECT_PT_quick_scale_panel(bpy.types.Panel):
    """Panel lateral en la Viewport (N-Panel)"""

    bl_label = "Quick Scale"
    bl_idname = "OBJECT_PT_quick_scale_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        # Botón para ejecutar el operador directo desde el N-Panel
        op = col.operator(
            OBJECT_OT_quick_axis_scale.bl_idname, text="Aplicar Escala"
        )


# Función para inyectar la opción en el menú del botón derecho
def right_click_menu_func(self, context):
    self.layout.separator()
    self.layout.operator(
        OBJECT_OT_quick_axis_scale.bl_idname, text="Scale Object by Axis"
    )


# Registro de clases y menus
classes = (
    OBJECT_OT_quick_axis_scale,
    OBJECT_PT_quick_scale_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Añadir al menú del Clic Derecho de Objetos
    bpy.types.VIEW3D_MT_object_context_menu.append(right_click_menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(right_click_menu_func)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()