from tkinter import Tk, Canvas
from random import randint

import Util
import Text_Wrapper


def main():

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
    xscale = Util.get_number("Distance from origin to x-extremes")
    yscale = Util.get_number("Distance from origin to y-extremes")
    res = Util.get_number("Resolution (0 checks one pixel at a time, 1 checks 4, 2 checks 9, ...)", bound=1079)
    filename = Util.get_string("File to save set to")
    java = bool(Util.get_choice(["No", "Yes"], "Generate using Java?"))
    target = Text_Wrapper.Text_Wrapper_Writer(filename, width, height, xscale, yscale, res)

    x = 0
    while x <= width:
        y = 0
        while y <= height:
            to_complex(x, y, target)


def to_complex(x, y, target):

    real = (((2 * target.xscale) / target.width) * x) - target.xscale
    imaginary = (((2 * target.yscale) / target.height) * y) - target.yscale
    return complex(real, imaginary)



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