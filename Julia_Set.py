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

    set_type = Util.get_choice(["Mandelbrot set", "Julia set"], "Set type")
    width = Util.get_number("Width of set in pixels", bound=1920)
    height = Util.get_number("Height of set in pixels", bound=1080)
    xmin = Util.get_number("Minimum x value", use_float=True, require_positive=False)
    xmax = Util.get_number("Maximum x value", use_float=True, require_positive=False)
    ymin = Util.get_number("Minimum y value", use_float=True, require_positive=False)
    ymax = Util.get_number("Maximum y value", use_float=True, require_positive=False)
    res = Util.get_number("Resolution (0 checks one pixel at a time, 1 checks 4, 2 checks 9, ...)", bound=1079)
    if set_type:
        seed = Util.get_complex("C value")
    else:
        seed = 0
    filename = Util.get_string("File to save set to")
    target = Text_Wrapper.TextWrapperWriter(filename, width, height, xmin, xmax, ymin, ymax, res)

    if set_type:
        x = 0
        while x <= width:
            y = 0
            while y <= height:
                imaginary_num = to_complex(x, y, target)
                in_set = is_in_julia_set(imaginary_num, 0, seed)
                if in_set:
                    target.write_pixel(x, y, in_set)
                print(str(int((x / (width + 1)) * 100)) + "%", end='\r')

                y += (1 + target.res)
            x += (1 + target.res)
    
    else:
        x = 0
        while x <= width:
            y = 0
            while y <= height:
                imaginary_num = to_complex(x, y, target)
                in_set = is_in_mandelbrot_set(imaginary_num, 0, seed)
                if in_set:
                    target.write_pixel(x, y, in_set)
                print(str(int((x / (width + 1)) * 100)) + "%", end='\r')

                y += (1 + target.res)
            x += (1 + target.res) 


def to_complex(x, y, target):
    
    real = (((target.xmax - target.xmin) / target.width) * x) + target.xmin
    imaginary = (((target.ymin - target.ymax) / target.height) * y) + target.ymax
    return complex(real, imaginary)


def is_in_julia_set(imaginary_num, depth, c):
    
    # https://en.wikipedia.org/wiki/Julia_set#Pseudocode_for_normal_Julia_sets
    result = imaginary_num ** 2 + c
    if (result.real ** 2 + result.imag ** 2 <= 4) and depth < 900:
        return(is_in_julia_set(result, depth + 1, c))
    else:
        if depth < 900:
            return depth
        else:
            return False


def is_in_mandelbrot_set(imaginary_num, depth, z):
    
    # https://en.wikipedia.org/wiki/Mandelbrot_set#Computer_drawings
    result = z ** 2 + imaginary_num
    if (z.real ** 2 + z.imag ** 2 <= 4) and depth < 900:
        return(is_in_mandelbrot_set(imaginary_num, depth + 1, result))
    else:
        if depth < 900:
            return depth
        else:
            return False


def render_set():

    data = Text_Wrapper.TextWrapperReader(Text_Wrapper.get_file('set'))
    window = Tk()
    canvas = Canvas(window, bg='#000000', width=data.width, height=data.height)
    canvas.pack()

    max_depth = 0
    for pixel in data.pixels:
        if pixel[2] > max_depth:
            max_depth = pixel[2]
    grayscale = 255 / max_depth

    res = data.res

    for i, pixel in enumerate(data.pixels):
        x = pixel[0]
        y = pixel[1]
        fill_color = format(int(pixel[2] * grayscale), '02x')
        fill_color = '#' + (fill_color * 2) + '00'
        canvas.create_rectangle(x, y, x+res, y+res, fill=fill_color, outline=fill_color)
        print(str(int((i / len(data.pixels)) * 100)) + "%", end='\r')

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