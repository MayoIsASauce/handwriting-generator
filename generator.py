from PIL import Image
from definitions.Color_e import Color_e as Color

import analysis

def __tokenize(string: str) -> list[tuple[int, str]]:
    """
    Takes an input string and analyzes the string to determine which files to use.
    """

    def peek(arr:list[str]):
        if len(arr) == 0:
            return "-1"
        else:
            return arr[-1]

    if string == "":
        raise ValueError("Passed tokenizer an empty string")

    chars: list[str] = list(string)
    chars.reverse()

    while len(chars) != 0:
        print(f"{chars.pop()} : {peek(chars)}")

    return [""]



def generate_text_image(input_s:str, size=(500,250), baseline=False, offset_max=5, color: Color = Color.BLACK):
    """
    Takes a string and creates an image with the text in provided handwriting

    * `input_s` the string to use when creating the image
    * `size` the size of the image, also controls the scaling of the font and alignment
    * `baseline` Should the letters be perfectly lined up?
    * `offset_max` The maximum amount of letter vertical offset in either direction
    * `color` The desired color of text
    """
    __tokenize(input_s)
    return Image.open("static/samples/letters/lower/001/001_A.png")