
bl_info = {
    "name": "Color Proportional Scaler",
    "author": "Diego Moreno",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "3D Viewport > N-Panel > Item / Right Click Menu",
    "description": "Scale objects proportionally based on their material color brightness without removing black objects",
    "category": "Object",
}

import bpy

def get_object_luminance(obj):
    """Calcula la luminancia relativa (0.0 a 1.0) basada en el color del material del objeto."""
    if not obj.data or not hasattr(obj.data, "materials") or not obj.data.materials:
        return 0.0  # Sin material = tratado como negro/0.0

    mat = obj.data.materials[0]
    if not mat or not mat.use_nodes:
        return 0.0

    nodes = mat.node_tree.nodes
    principled = nodes.get("Principled BSDF")

    if not principled:
        return 0.0

    color = principled.inputs["Base Color"].default_value
    r, g, b = color[0], color[1], color[2]

    # Fórmula Estándar ITU-R BT.709 para calcular la luminancia percibida
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return min(max(luminance, 0.0), 1.0)


class OBJECT_OT_color_scale(bpy.types.Operator):
    """Escala los objetos según la luminancia de su color de material"""

    bl_idname = "object.color_proportional_scale"
    bl_label = "Scale by Color Brightness"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(
        name="Eje de Escala",
        description="Eje en el cual aplicar el escalado proporcional",
        items=[
            ("ALL", "Todos los Ejes (XYZ)", "Escalar uniformemente"),
            ("X", "Eje X", "Escalar solo en X"),
            ("Y", "Eje Y", "Escalar solo en Y (Profundidad)"),
            ("Z", "Eje Z", "Escalar solo en Z (Altura)"),
        ],
        default="Y",
    )

    min_scale: bpy.props.FloatProperty(
        name="Escala Mínima (Negro)",
        description="Factor de escala base para objetos negros (Luminancia = 0.0)",
        default=1.0,  # Conserva el tamaño base de 1.0 para el negro
        min=0.01,     # Evita que se reduzca a 0
        soft_max=5.0,
    )

    max_scale: bpy.props.FloatProperty(
        name="Escala Máxima (Blanco)",
        description="Factor de escala para objetos blancos (Luminancia = 1.0)",
        default=2.5,
        min=0.1,
        soft_max=10.0,
    )

    progression_type: bpy.props.EnumProperty(
        name="Progresión",
        description="Modo de interpolación de la escala",
        items=[
            ("LINEAR", "Lineal", "Aumento directamente proporcional"),
            ("EXPONENTIAL", "Exponencial", "Los colores claros crecen de forma más pronunciada"),
            ("STEPPED", "Escalonada", "Redondea los colores a niveles discretos"),
        ],
        default="LINEAR",
    )

    only_selected: bpy.props.BoolProperty(
        name="Solo Seleccionados",
        description="Aplicar solo a objetos seleccionados o a toda la escena",
        default=True,
    )

    def execute(self, context):
        objects = context.selected_objects if self.only_selected else context.scene.objects

        processed_count = 0
        for obj in objects:
            if obj.type != "MESH":
                continue

            lum = get_object_luminance(obj)

            # Cálculo de la escala según la progresión
            if self.progression_type == "LINEAR":
                factor = self.min_scale + (self.max_scale - self.min_scale) * lum
            elif self.progression_type == "EXPONENTIAL":
                factor = self.min_scale + (self.max_scale - self.min_scale) * (lum ** 2)
            elif self.progression_type == "STEPPED":
                stepped_lum = round(lum * 4) / 4.0
                factor = self.min_scale + (self.max_scale - self.min_scale) * stepped_lum

            # Aplicar la escala garantizando que no se elimine ningún objeto
            if self.axis == "ALL":
                obj.scale = (factor, factor, factor)
            elif self.axis == "X":
                obj.scale.x = factor
            elif self.axis == "Y":
                obj.scale.y = factor
            elif self.axis == "Z":
                obj.scale.z = factor

            processed_count += 1

        self.report({"INFO"}, "Escalados {0} objetos respetando tamaño mínimo.".format(processed_count))
        return {"FINISHED"}


# Panel UI
class OBJECT_PT_color_scale_panel(bpy.types.Panel):
    bl_label = "Color Proportional Scale"
    bl_idname = "OBJECT_PT_color_scale_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(OBJECT_OT_color_scale.bl_idname, text="Escalar por Color")


def right_click_menu_func(self, context):
    self.layout.separator()
    self.layout.operator(OBJECT_OT_color_scale.bl_idname, text="Scale by Color Brightness")


classes = (
    OBJECT_OT_color_scale,
    OBJECT_PT_color_scale_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.append(right_click_menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(right_click_menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()