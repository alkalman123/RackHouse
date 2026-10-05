"""Builds img/kickstarter-share.jpg (1200x630 social card) from the
Gear Board and Crag Ring gear renders."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 630
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def main():
    bg = Image.new("RGB", (W, H), (18, 19, 21))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(30 - 12 * t), int(22 - 6 * t), int(18 - 4 * t)))
    hero = Image.open(os.path.join(ROOT, "img", "products", "gear-board-hero-dark.jpg"))
    hw, hh = hero.size
    hero = hero.crop((int(hw * 0.075), 0, int(hw * 0.925), hh)).resize((765, 630), Image.LANCZOS)
    mask = Image.linear_gradient("L").rotate(90).resize((765, 630))   # fade in from the left
    mask = mask.point(lambda v: min(255, int(v * 2.2)))
    bg.paste(hero, (W - 765, 0), mask)
    d = ImageDraw.Draw(bg)
    ember = (216, 92, 42)
    d.text((60, 70), "RACKHOUSE  ·  ON KICKSTARTER", font=ImageFont.truetype(BOLD, 22), fill=ember)
    big = ImageFont.truetype(BOLD, 54)
    d.text((60, 120), "Your whole rack.", font=big, fill=(240, 236, 230))
    d.text((60, 192), "Nothing falls off.", font=big, fill=(240, 236, 230))
    small = ImageFont.truetype(REG, 25)
    for i, line in enumerate(["3D-printed carabiner organizers", "with fully enclosed slots, for the",
                              "closet, the car, the pack and the crag."]):
        d.text((60, 292 + i * 36), line, font=small, fill=(196, 190, 182))
    d.rounded_rectangle((60, 448, 440, 510), 12, fill=ember)
    d.text((82, 463), "Early birds up to 25% off", font=ImageFont.truetype(BOLD, 24), fill=(255, 255, 255))
    d.text((60, 560), "3D render of the Gear Board", font=ImageFont.truetype(REG, 16), fill=(120, 116, 110))
    bg.save(os.path.join(ROOT, "img", "kickstarter-share.jpg"), quality=88, optimize=True)


if __name__ == "__main__":
    main()
