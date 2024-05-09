import os
from sys import argv
from pathlib import Path
from PIL import Image

alpha = int(argv[1])
glob = argv[2]
files = Path(os.getcwd()).glob(glob)
for f in files:
    print(f)
    img = Image.open(f, 'r').convert('RGBA')
    new_img = Image.new('RGBA', img.size)
    for x in range(new_img.width):
        for y in range(new_img.height):
            old_color = img.getpixel((x, y))
            if old_color == (0,0,0,0): continue
            new_color = tuple([
                old_color[0],
                old_color[1],
                old_color[2],
                alpha
            ])
            new_img.putpixel((x,y), new_color)
    new_img.save(f)