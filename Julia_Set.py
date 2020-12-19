from tkinter import Tk, Canvas
from random import randint

import Util
import Text_Wrapper


def main():

    while True:
    print("Welcome to Julia Set Generator/Renderer")
    choice = Util.get_choice(["Generate a set", "Render a set", "Help!"], "What would you like to do?")

    if choice == 0:
        generate_set()
    elif choice == 1:
        render_set()
    else:
        help()


def generate_set():

    width = Util.get_number("Width of set in pixels", bound=1920)
    height = Util.get_number("Height of set in pixels", bound=1080)
    res = Util.get_number("Resolution (0 checks one pixel at a time, 1 checks 4, 2 checks 9, ...)", bound=1079)
    c = Util.get_number("C value", require_positive=False, use_float=True)
    filename = Util.get_string("File to save set to")
    java = bool(Util.get_choice(["No", "Yes"], "Generate using Java?"))
    target = Text_Wrapper.Text_Wrapper_Writer(filename, width, height, res, c)
    print(target.escape)

    x = 0
    while x <= width:
        y = 0
        while y <= height:
            imaginary_num = to_complex(x, y, target)
            in_set = is_in_set(imaginary_num, 0, target)
            if in_set:
                target.write_pixel(x, y, in_set)

            y += (1 + target.res)
        x += (1 + target.res)


def to_complex(x, y, target):
    
    real = (((2 * target.escape) / target.width) * x) - target.escape
    imaginary = (((2 * target.escape) / target.height) * y) - target.escape
    return complex(real, imaginary)


def is_in_set(imaginary_num, depth, target):
    
    # https://en.wikipedia.org/wiki/Julia_set#Pseudocode_for_normal_Julia_sets
    result = imaginary_num ** 2 + target.c
    if (result.real + result.imag <= target.escape) and depth < 1000:
        return(is_in_set(result, depth + 1, target))
    else:
        if depth < 1000:
            return depth
        else:
            return False


def render_set():

    data = Text_Wrapper.Text_Wrapper_Reader(Text_Wrapper.get_file('set'))
    window = Tk()
    canvas = Canvas(window, width=data.width, height=data.height)
    canvas.pack()

    res = data.res

    for pixel in data.pixels:
        x = pixel[0]
        y = pixel[1]
        canvas.create_rectangle(x, y, x+res, y+res, fill='#FF00FF', outline='')

    window.mainloop()


def help():

    print("JULIA SETS")
    print("Information about Julia Sets goes here.\n")

    print("GENERATING SETS")
    print("Information about generating sets goes here.\n")

    print("RENDERING SETS")
    print("Information about rendering sets goes here.\n")


if __name__ == "__main__":
    main()