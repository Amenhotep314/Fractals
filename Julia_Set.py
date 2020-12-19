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

    print("ICH BIN ICH!")


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