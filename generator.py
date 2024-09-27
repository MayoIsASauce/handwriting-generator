from PIL import Image
from random import randint

from definitions.Color_e import Color_e as Color
from definitions.SymbolGuide_d import SymbolGuide_d as __symbol_guide
import analysis

def __change_color(image: Image.Image, color) -> Image.Image:
    pixels = image.load()

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]

            intensity = (r + g + b) / 3
            brightness = intensity / 255

            if color == Color.RED:
                pixels[x, y] = (int(255 * (brightness + 1)), g, b)
            elif color == Color.BLUE:
                pixels[x, y] = (r, g, int(255 * (brightness + 0.7)))
            elif color == Color.GREEN:
                pixels[x, y] = (r, int(255 * (brightness + 0.4)), b)

    return image

def generate_text_image(input_s: str, size=(500, 250), baseline=False, offset_max=5, color: Color = Color.BLACK) -> Image.Image:
    """
    Main function that takes a string and creates an image with the text in provided handwriting.
    """

    if not input_s:
        raise ValueError("Passed tokenizer an empty input_s")

    chars = list(input_s)
    chars.reverse()

    selected_ids = switch_ids()
    selected_fonts = switch_fonts(selected_ids)

    images, total_width, total_height = process_characters(chars, selected_fonts, selected_ids, size, offset_max)
    
    combined_image = combine_images(images, total_width, total_height, baseline, offset_max)

    if color != Color.BLACK:
        combined_image = __change_color(combined_image, color)
    

    return combined_image


def rand_select(arr: list) -> str:
    """Randomly selects an element from a list."""
    return arr[randint(0, len(arr) - 1)]


def switch_ids() -> dict:
    """Switches the font IDs for lowercase, uppercase, and numbers."""
    selected_ids = {
        'll': rand_select(list(analysis.fonts['ll'].keys())),
        'lu': rand_select(list(analysis.fonts['lu'].keys())),
        'nums': rand_select(list(analysis.fonts['nums'].keys()))
    }
    return selected_ids


def switch_fonts(selected_ids: dict) -> dict:
    """Switches the font paths for lowercase, uppercase, and numbers based on selected_ids."""
    selected_fonts = {
        "ll": f"static/samples/letters/lower/{selected_ids['ll']}",
        "lu": f"static/samples/letters/upper/{selected_ids['lu']}",
        "nums": f"static/samples/numbers/{selected_ids['nums']}"
    }
    return selected_fonts


def process_characters(chars: list, selected_fonts: dict, selected_ids: dict, size: tuple, offset_max: int) -> tuple:
    """
    Processes characters in the input string, generates images for them, and calculates total width and height.
    """
    images = []
    total_width, total_height = 0, 0

    while chars:
        curr = chars.pop()
        img, img_width, img_height = get_image_for_character(curr, selected_fonts, selected_ids)
        
        # Adjust the image if needed
        max_size = 40
        img = resize_image(img, max_size)
        
        images.append((curr, img))
        total_width += img.width
        total_height = max(total_height, img.height)

        selected_ids = switch_ids()
        selected_fonts = switch_fonts(selected_ids)

    return images, total_width, total_height


def get_image_for_character(curr: str, selected_fonts: dict, selected_ids: dict) -> tuple:
    """
    Gets the image for the current character, either from the specified font or as a blank image for spaces.
    """
    if curr.islower():
        id = 'll'
    elif curr.isupper():
        id = 'lu'
    elif curr.isdigit():
        id = 'nums'
    elif curr == ' ':
        blank_img = Image.new('RGB', (30, 30), color=(255, 255, 255))
        return blank_img, blank_img.width, blank_img.height
    elif curr in list(__symbol_guide.keys()):
        img = Image.open("static/samples/symbols/" + __symbol_guide[curr])
        return img, img.width, img.height
    
    # Otherwise, select the image from the fonts
    img = Image.open(selected_fonts[id] + '/' + selected_ids[id] + f"_{curr}.png")
    return img, img.width, img.height


def resize_image(img: Image.Image, max_size: int) -> Image.Image:
    """
    Resizes an image to a maximum size while maintaining the aspect ratio.
    """
    if img.width > max_size or img.height > max_size:
        scaling_factor = min(max_size / img.width, max_size / img.height)
        new_width = int(img.width * scaling_factor)
        new_height = int(img.height * scaling_factor)
        img = img.resize((new_width, new_height), Image.ADAPTIVE)
    return img


def combine_images(images: list, total_width: int, total_height: int, baseline: bool, offset_max: int) -> Image.Image:
    """
    Combines individual images of characters into one final image, with baseline or offset handling.
    """
    combined_image = Image.new('RGB', (total_width, total_height + 5), color=(255, 255, 255))
    x_off = 0

    for curr, img in images:
        y_off = calculate_y_offset(curr, img, total_height, baseline, offset_max)
        combined_image.paste(img, (x_off, y_off))
        x_off += img.width

    return combined_image


def calculate_y_offset(curr: str, img: Image.Image, total_height: int, baseline: bool, offset_max: int) -> int:
    """
    Calculates the vertical offset for each character image depending on the baseline or offset options.
    """
    descenders = set("ypqgj")
    if baseline:
        y_off = total_height - img.height - 3
    else:
        y_off = total_height - img.height - randint(-offset_max, offset_max)

    if curr in descenders:
        y_off += 8

    return y_off