import sys
import PIL.Image

import generator as gen

if __name__ == "__main__":
    # 1. fetch text
    string_input: str = sys.argv[1]

    # 2. for each letter in the text fetch an image
    collage: PIL.Image.Image = gen.generate_text_image(string_input, size=(300, 300))
    collage.show()
