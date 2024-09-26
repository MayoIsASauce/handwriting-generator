from PIL import Image
from definitions.Color_e import Color_e as Color

import analysis

def __tokenize(string: str) -> list[tuple[int, str]]:
    """
    Takes an input string and analyzes the string to determine which files to use
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



def generate_text_image(input_s:str, size=(500,250), baseline=-1, color: Color = Color.BLACK):
    __tokenize(input_s)
    return Image.open("static/samples/letters/lower/001/001_A.png")