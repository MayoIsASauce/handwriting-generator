import PIL.Image
import sys
import generator as gen

if __name__ == "__main__":
    # 1. fetch text
    string_input: str = "USD $1,000,000"

    # 2. for each letter in the text fetch an image
    collage = gen.generate_text_image(string_input, size=(300, 300), offset_max=2, color=gen.Color.BLACK)
    collage.show()
