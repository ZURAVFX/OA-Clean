from pathlib import Path
from io import BytesIO

import pymupdf
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
OUT = ASSETS / "social-card.png"
FONT_REGULAR = Path(r"C:\Users\ElliotMcKenzie\AppData\Local\Microsoft\Windows\Fonts\DMSans_18pt-Regular.ttf")
FONT_MEDIUM = Path(r"C:\Users\ElliotMcKenzie\AppData\Local\Microsoft\Windows\Fonts\DMSans_18pt-Medium.ttf")


def raster_svg(path: Path, width: int) -> Image.Image:
    doc = pymupdf.open(path)
    page = doc[0]
    zoom = width / page.rect.width
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=True)
    rendered = Image.open(BytesIO(pix.tobytes("png"))).convert("RGBA")
    if "white" in path.stem:
        white = Image.new("RGBA", rendered.size, (255, 255, 255, 0))
        white.putalpha(rendered.getchannel("A"))
        return white
    return rendered


canvas = Image.new("RGB", (1200, 630), "#000000")
draw = ImageDraw.Draw(canvas)

for x in range(0, 760, 80):
    draw.line((x, 0, x, 630), fill=(24, 24, 24), width=1)
for y in range(0, 631, 80):
    draw.line((0, y, 760, y), fill=(24, 24, 24), width=1)

draw.rectangle((760, 0, 1200, 630), fill="#AFFF41")
draw.rounded_rectangle((790, 30, 1170, 600), radius=10, outline=(0, 0, 0), width=1)

logo_source = raster_svg(ASSETS / "oa-full-black.svg", 145)
logo = Image.new("RGBA", logo_source.size, (255, 255, 255, 0))
logo.putalpha(logo_source.getchannel("A"))
canvas.paste(logo, (54, 48), logo)

font_large = ImageFont.truetype(str(FONT_MEDIUM), 102)
font_small = ImageFont.truetype(str(FONT_REGULAR), 24)
font_label = ImageFont.truetype(str(FONT_MEDIUM), 18)

draw.text((54, 205), "Clean files.", font=font_large, fill="#EAEAEA", spacing=-8)
draw.text((54, 305), "Keep the work.", font=font_large, fill="#AFFF41", spacing=-8)
draw.text((58, 470), "Local metadata cleaning for image and video.", font=font_small, fill="#EAEAEA")
draw.text((58, 518), "WINDOWS  /  APPLE SILICON  /  INTEL", font=font_label, fill="#AFFF41")

icon = raster_svg(ASSETS / "oa-icon-black.svg", 180)
canvas.paste(icon, (890, 230), icon)
draw.text((815, 64), "DROP. CLEAN. DONE.", font=font_label, fill="#000000")

canvas.save(OUT, optimize=True)
print(OUT)
