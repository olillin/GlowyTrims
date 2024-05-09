import os
from pathlib import Path
from PIL import Image
import shutil
from collections.abc import Iterable

output_dir: str = 'output'
# Clean output directory
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

palette_paths: list[str] = [
    "assets/biomesoplenty/textures/trims/color_palettes/glowworm_silk.png",
    "assets/biomesoplenty/textures/trims/color_palettes/rose_quartz.png",
]

base_palette_path: str = "assets/minecraft/textures/trims/color_palettes/amethyst.png"
texture_directories: list[str] = [
    "assets/minecraft/textures/trims/items",
    "assets/minecraft/textures/trims/models/armor",
]

def create_dir(path: Path):
    if (path.exists()):
        return
    if (not path.parent.exists()):
        create_dir(path.parent)
    path.mkdir()

def find_good_enough(color: tuple[int, int, int, int], colors: Iterable[tuple[int, int, int, int]], tolerance: int = 2) -> tuple[int, int, int, int] | None:
    for c in colors:
        for i in range(4):
            if abs(color[i]-c[i]) > tolerance:
                break
        else:
            return c


base_material = Path(base_palette_path).stem

for palette_path in palette_paths:
    # Create color map
    palette: Image.Image = Image.open(palette_path).convert('RGBA')
    material: str = Path(palette_path).stem

    color_map = {}
    base_palette: Image.Image = Image.open(base_palette_path)
    for x in range(base_palette.width):
        old_pixel = base_palette.getpixel((x, 0))
        new_pixel = palette.getpixel((x, 0))
        new_pixel = tuple([
            new_pixel[0],
            new_pixel[1],
            new_pixel[2],
            old_pixel[3]
            ])
        color_map[old_pixel] = new_pixel

    # Create new textures
    for texture_dir in texture_directories:
        for in_texture_name in os.listdir(texture_dir):
            if base_material not in in_texture_name: continue

            in_texture_path = Path(texture_dir).joinpath(in_texture_name)
            in_texture = Image.open(in_texture_path).convert('RGBA')
            out_texture = Image.new('RGBA', in_texture.size)

            for x in range(in_texture.width):
                for y in range(in_texture.height):
                    old_pixel = in_texture.getpixel((x, y))
                    if old_pixel == (0,0,0,0): continue
                    good_enough = find_good_enough(old_pixel, color_map.keys())
                    if good_enough == None: continue
                    new_pixel = color_map[good_enough]
                    out_texture.putpixel((x, y), new_pixel)

            out_texture_path = Path(output_dir).joinpath(str(in_texture_path).replace(base_material, material))
            create_dir(out_texture_path.parent)
            out_texture.save(out_texture_path)
            print(out_texture_path)