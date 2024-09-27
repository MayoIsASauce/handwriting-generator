from PIL import Image
from random import randint

from definitions.Color_e import Color_e as Color
import analysis

def __change_color(image: Image.Image, color) -> Image.Image:
    pixels = image.load()

    threshold = 100

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]

            intensity = (r + g + b) / 3

            # For lighter pixels, keep the brightness but tint them red
            # Calculate brightness level (relative to max intensity)
            brightness = intensity / 255

            if color == Color.RED:
                pixels[x, y] = (int(255 * (brightness + 1)), g, b)
            elif color == Color.BLUE:
                pixels[x, y] = (r, g, int(255 * (brightness + 0.7)))
            elif color == Color.GREEN:
                pixels[x, y] = (r, int(255 * (brightness + 0.4)), b)

    return image

def generate_text_image(input_s:str, size=(500,250), baseline=False, offset_max=5, color: Color = Color.BLACK) -> Image.Image:
    """
    Takes a string and creates an image with the text in provided handwriting

    * `input_s` the string to use when creating the image
    * `size` the size of the image, also controls the scaling of the font and alignment
    * `baseline` Should the letters be perfectly lined up?
    * `offset_max` The maximum amount of letter vertical offset in either direction
    * `color` The desired color of text
    """
        
    def rand_select(arr: list):
        return arr[randint(0,len(arr)-1)]

    __symbol_guide = {
        '-': "-.png",
        ',': ",.png",
        '!': "!.png",
        '(': "(.png",
        ')': ").png",
        '[': "[.png",
        ']': "].png",
        '{': "{.png",
        '}': "}.png",
        '#': "#.png",
        '%': "%.png",
        '+': "+.png",
        '=': "=.png",
        '~': "~.png",
        '$': "$.png",
        '¢': "cent.png",
        '.': "dec.png",
        '/': "div.png",
        '>': "greater.png",
        '∩': "intersection.png",
        '<': "less.png",
        '*': "mult.png",
        '|': "pipe.png",
        '?': "ques.png",
        '∪': "union.png"
    }

    if input_s == "":
        raise ValueError("Passed tokenizer an empty input_s")

    chars: list[str] = list(input_s)
    chars.reverse()

    selected_ids = {}
    selected_fonts = {}

    def switch_ids():
        selected_ids = {
            'll': rand_select(list(analysis.fonts['ll'].keys())),
            'lu': rand_select(list(analysis.fonts['lu'].keys())),
            'nums': rand_select(list(analysis.fonts['nums'].keys()))
        }

        return selected_ids
    
    def switch_fonts():
        selected_fonts = {
            "ll": f"static/samples/letters/lower/{selected_ids['ll']}",
            "lu": f"static/samples/letters/upper/{selected_ids['lu']}",
            "nums": f"static/samples/numbers/{selected_ids['nums']}"
        }

        return selected_fonts

    selected_ids = switch_ids()
    selected_fonts = switch_fonts()

    descenders = set("ypqgj")

    images = []
    width = 0
    height = 0
    curr:str = ''
    while len(chars) != 0:
        lock = False
        curr:str = chars.pop()
        id = ''
        if curr.islower():
            id = 'll'
        elif curr.isupper():
            id = 'lu'
        elif curr.isdigit():
            id = 'nums'
        elif curr == ' ':
            blank_img = Image.new('RGB', (30, 30), color=(255, 255, 255))  # White blank image
            images.append((curr, blank_img))
            width += blank_img.width
            height = max(height, blank_img.height)
            continue
        elif curr in list(__symbol_guide.keys()):
            img = Image.open("static/samples/symbols/" + __symbol_guide[curr])
            lock = True        

        if not lock:
            img = Image.open(selected_fonts[id]+'/'+selected_ids[id]+f"_{curr}.png")

        max_size = 40
        if img.width > max_size or img.height > max_size:
            # Calculate the scaling factor to maintain aspect ratio
            scaling_factor = min(max_size / img.width, max_size / img.height)
            
            # Calculate the new width and height
            new_width = int(img.width * scaling_factor)
            new_height = int(img.height * scaling_factor)
            
            # Resize the image to fit within the max_size
            img = img.resize((new_width, new_height), Image.ADAPTIVE)


        images.append((curr, img))
        width += img.width
        height = max(height, img.height)

        selected_ids = switch_ids()
        selected_fonts = switch_fonts()

    combined_image = Image.new('RGB', (width, height+5), color=(255, 255, 255))

    x_off = 0
    y_off = 0
    for curr, img in images:
        if baseline == True:
            y_off = height - img.height - 3
        else:
            y_off = height - img.height - randint(-offset_max, offset_max)

        if curr in descenders:
            y_off += 8

        combined_image.paste(img, (x_off, y_off)) 
        x_off += img.width
    
    if color != Color.BLACK:
        combined_image = __change_color(combined_image, color)
    
    return combined_image