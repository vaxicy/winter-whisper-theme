"""Render a flat snowflake and breeze mark; only a transparent 128px export."""
from pathlib import Path
import math
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCALE = 4
im = Image.new('RGBA', (128*SCALE, 128*SCALE))
d = ImageDraw.Draw(im)

def line(points, fill, width):
    points = [(round(x*SCALE), round(y*SCALE)) for x,y in points]
    d.line(points, fill=fill, width=width*SCALE)
    r = width*SCALE/2
    for x,y in points:
        d.ellipse((x-r,y-r,x+r,y+r),fill=fill)

# Six symmetrical arms with two branching tips, solid fills and rounded ends.
cx,cy = 64,48
for i in range(6):
    angle = math.radians(-90+i*60)
    ux,uy = math.cos(angle),math.sin(angle)
    line([(cx,cy),(cx+ux*35,cy+uy*35)], '#A9A4D0', 5)
    for side in (-1,1):
        x,y = cx+ux*23,cy+uy*23
        branch_angle = angle+side*math.pi/3
        line([(x,y),(x+math.cos(branch_angle)*12,y+math.sin(branch_angle)*12)], '#A9A4D0', 4)

def breeze(x1,x2,y,amplitude):
    points = [(x1+(x2-x1)*i/60,y+amplitude*math.sin(i/60*math.pi*2)) for i in range(61)]
    line(points,'#C1C1E6',4)

breeze(17,110,97,3)
breeze(33,93,112,2)
im = im.resize((128,128),Image.Resampling.LANCZOS)
dest = ROOT/'logo/logo128.png'
dest.parent.mkdir(parents=True,exist_ok=True)
im.save(dest)
assert im.size == (128,128) and im.mode == 'RGBA'
print('Generated logo/logo128.png: 128x128 RGBA')
