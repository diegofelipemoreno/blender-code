import json
import os
import sys
import bpy


def create_pixel_art_from_json(json_path):
    # 1. Verificar si el archivo JSON existe
    if not os.path.exists(json_path):
        print("Error: No se encontro el archivo JSON en: {0}".format(json_path))
        return

    # 2. Leer los datos del JSON
    with open(json_path, "r") as f:
        data = json.load(f)

    # 3. Crear una nueva colección en Blender para organizar los cubos
    collection_name = "PixelArt_Import"
    if collection_name in bpy.data.collections:
        pixel_collection = bpy.data.collections[collection_name]
    else:
        pixel_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(pixel_collection)

    # Cache para reutilizar materiales con el mismo color y evitar duplicados
    materials_cache = {}

    print("Generando {0} cubos...".format(len(data)))

    # 4. Iterar sobre cada elemento del JSON
    for item in data:
        col = item["grid_position"]["col"]
        row = item["grid_position"]["row"]
        rgba = item["color"]["rgba"]

        # Convertir color de 0-255 (sRGB) a 0.0-1.0 para Blender
        r = rgba[0] / 255.0
        g = rgba[1] / 255.0
        b = rgba[2] / 255.0
        a = rgba[3] / 255.0
        hex_color = item["color"]["hex"]

        # Posición 3D: Invertimos row (-row) para que la imagen no quede al revés en el eje Z/Y
        # Colocamos X = col, Y = 0, Z = -row (plano frontal XZ)
        location = (col, 0, -row)

        # Crear el cubo básico
        bpy.ops.mesh.primitive_cube_add(size=0.95, location=location)
        cube = bpy.context.active_object
        cube.name = "Pixel_{0}_{1}".format(col, row)

        # Mover el cubo a nuestra colección organizada
        for coll in cube.users_collection:
            coll.objects.unlink(cube)
        pixel_collection.objects.link(cube)

        # Creación / Asignación de Material con Color
        if hex_color in materials_cache:
            mat = materials_cache[hex_color]
        else:
            mat = bpy.data.materials.new(name="Mat_{0}".format(hex_color))
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            principled = nodes.get("Principled BSDF")

            if principled:
                principled.inputs["Base Color"].default_value = (r, g, b, a)

            materials_cache[hex_color] = mat

        cube.data.materials.append(mat)

    print("¡Mosaico 3D generado con exito!")


# --- MODOS DE EJECUCIÓN ---

# A) Ejecución dentro de la interfaz de Blender (Text Editor)
# Reemplaza la ruta por la ubicación real de tu archivo pixel_data.json
json_file_path = "/Users/diego/Documents/workspace-web/blender-code/pixel_data.json"

# B) Para pasar el argumento desde terminal ejecutando Blender de fondo:
# blender --background --python script.py -- /ruta/a/pixel_data.json
if "--" in sys.argv:
    args = sys.argv[sys.argv.index("--") + 1 :]
    if args:
        json_file_path = args[0]

create_pixel_art_from_json(json_file_path)