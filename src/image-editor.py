from PIL import Image, ImageDraw, ImageFont
import textwrap
import templates
import json
from pathlib import Path

def add_single_text(
    image_path: str,
    font_path: str,
    font_size: int,
    text: str,
    text_xy: tuple[float, float],
    text_align: str,
    text_anchor: str,
    text_width: int,
    text_fill_color: tuple[int, int, int],
    text_stroke: bool,
    text_stroke_size: int,
    text_stroke_color: tuple[int, int, int]
    ):
    """
    Adds multitext to a given image.
    
    """
    image = Image.open(image_path).convert("RGB")
    font = ImageFont.truetype(font_path, font_size)
    textwidth = text_width/font.getlength("m")
    wrapped_text = textwrap.fill(text, width=textwidth, replace_whitespace=False)
    draw = ImageDraw.Draw(image)
    draw.text(
        xy=text_xy, 
        text=wrapped_text,
        fill=text_fill_color,
        align=text_align,
        anchor=text_anchor,
        font=font,
        stroke_width=text_stroke_size if text_stroke else 0,
        stroke_fill=text_stroke_color if text_stroke else None
    )
    return image

if __name__ == "__main__":
    template = "necesito"
    text = "HACER UN SCRIPT DE PYTHON QUE GENERE MEMES"
    if (file_path := templates.available[template]) == None:
        print(f"Error: template {template} not found.")
        exit(1)
    with open(Path(file_path), 'r') as file:
        print(f"File {file_path} opened.")
        configs = json.load(fp=file)
        print(f"Json loaded.")

        if (prefix := configs["text"]["prefix"]) != None:
            text = prefix + " " + text
        if (suffix := configs["text"]["suffix"]) != None:
            text = text + " " + suffix
        
        add_single_text(
            image_path=configs["image_path"],
            font_path=configs["font_path"],
            font_size=configs["text"]["size"],
            text=text,
            text_xy=(configs["text"]["x"], configs["text"]["y"]),
            text_anchor=configs["text"]["anchor"],
            text_align=configs["text"]["align"],
            text_width=configs["text"]["max_width"],
            text_fill_color=(configs["text"]["color"]["r"], configs["text"]["color"]["g"], configs["text"]["color"]["b"]),
            text_stroke=configs["text"]["stroke"]["active"],
            text_stroke_size=configs["text"]["stroke"]["size"],
            text_stroke_color=(configs["text"]["stroke"]["color"]["r"], configs["text"]["stroke"]["color"]["g"], configs["text"]["stroke"]["color"]["b"])
        ).show()
        print("Execution complete.")
