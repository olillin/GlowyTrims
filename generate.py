import os
from pathlib import Path
from PIL import Image
import shutil

RGBA = tuple[int, int, int, int]

# Define directories
output_dir = Path('output')

palettes_dir = Path('input/color_palettes')
item_textures_dir = Path('input/items')
model_textures_dir = Path('input/models/armor')

# Clean output directory
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)


selected_palettes: list[str] = [
    'amethyst',
    'glowworm_silk',
    'rose_quartz',
]
base_palette: str = 'trim_palette'

def create_dir(path: Path):
    if (path.exists()):
        return
    if (not path.parent.exists()):
        create_dir(path.parent)
    path.mkdir()

base_palette_path = palettes_dir.joinpath(base_palette + '.png')
base_palette_img: Image.Image = Image.open(base_palette_path).convert('RGBA')
for palette in selected_palettes:
    # Create color map
    palette_path = palettes_dir.joinpath(palette + '.png')
    palette_img: Image.Image = Image.open(palette_path).convert('RGBA')

    color_map: dict[RGBA, RGBA] = {}
    for x in range(base_palette_img.width):
        old_pixel: RGBA = RGBA(base_palette_img.getpixel((x, 0)))
        new_pixel: RGBA = RGBA(palette_img.getpixel((x, 0)))
        color_map[old_pixel] = new_pixel

    # Generate textures
    def generate_textures(in_dir: Path, out_dir: Path):
        for in_texture_name in os.listdir(in_dir):
            in_texture_path = in_dir.joinpath(in_texture_name)
            in_texture_img = Image.open(in_texture_path).convert('RGBA')
            out_texture_img = Image.new('RGBA', in_texture_img.size)

            for x in range(in_texture_img.width):
                for y in range(in_texture_img.height):
                    in_pixel: RGBA = RGBA(in_texture_img.getpixel((x, y)))
                    if in_pixel == (0, 0, 0, 0): continue
                    out_pixel: RGBA = RGBA(color_map[in_pixel])
                    out_texture_img.putpixel((x, y), out_pixel)

            out_texture_path = Path(out_dir).joinpath(f'{in_texture_path.stem}_{palette}_e.png')
            create_dir(out_texture_path.parent)
            out_texture_img.save(out_texture_path)
            print(out_texture_path)

    generate_textures(item_textures_dir, output_dir.joinpath('assets/minecraft/textures/trims/items'))
    generate_textures(model_textures_dir, output_dir.joinpath('assets/minecraft/textures/trims/models/armor'))
    # Copy palette texture
    out_palettes_dir = output_dir.joinpath('assets/minecraft/textures/trims/color_palettes')
    create_dir(out_palettes_dir)
    palette_img.save(out_palettes_dir.joinpath(palette_path.name))