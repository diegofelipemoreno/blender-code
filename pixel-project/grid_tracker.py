import argparse
import json
import os
from PIL import Image


def process_pixel_art(image_path, block_size=38, output_json=None):
    # Generar el nombre dinámico si no se proporcionó uno personalizado
    if not output_json:
        filename = os.path.splitext(os.path.basename(image_path))[0]
        output_json = "pixel_{0}_data.json".format(filename)

    try:
        # Cargar la imagen y asegurar canal alfa (RGBA)
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print("Error al abrir la imagen '{0}': {1}".format(image_path, e))
        return

    width, height = img.size
    pixels_data = []

    cols = width // block_size
    rows = height // block_size

    for row in range(rows):
        for col in range(cols):
            left = col * block_size
            top = row * block_size
            right = left + block_size
            bottom = top + block_size

            block = img.crop((left, top, right, bottom))

            # Muestreo en el centro del bloque
            center_x = block_size // 2
            center_y = block_size // 2
            r, g, b, a = block.getpixel((center_x, center_y))

            # FILTRO: Ignorar bloques completamente transparentes (a == 0)
            if a == 0:
                continue

            hex_color = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

            block_info = {
                "grid_position": {"col": col, "row": row},
                "pixel_position": {"x": left, "y": top},
                "color": {"hex": hex_color, "rgba": [r, g, b, a]},
            }

            pixels_data.append(block_info)

    with open(output_json, "w") as f:
        json.dump(pixels_data, f, indent=4)

    print(
        "Proceso completado. Se registraron {0} bloques utiles en '{1}'.".format(
            len(pixels_data), output_json
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analiza una imagen por bloques de pixeles y exporta sus posiciones/colores a JSON."
    )

    parser.add_argument(
        "image_path",
        type=str,
        help="Ruta a la imagen de entrada (ej: contra.png)",
    )

    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=38,
        help="Tamano de la cuadrícula en pixeles (por defecto: 38)",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Nombre personalizado del archivo JSON (opcional, por defecto genera 'pixel_<nombre>_data.json')",
    )

    args = parser.parse_args()

    process_pixel_art(
        image_path=args.image_path,
        block_size=args.size,
        output_json=args.output,
    )