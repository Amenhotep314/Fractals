from tkinter import Tk, Canvas
from random import randint

import Util
import Text_Wrapper


def main():

    print("\nWelcome to Fractal Set Generator/Renderer")

    while True:
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
        c = Util.get_complex("C value")
    exponent = Util.get_number("Exponent", use_float=True)
    filename = Util.get_string("File to save set to")
    target = Text_Wrapper.TextWrapperWriter(filename, width, height, xmin, xmax, ymin, ymax, res)

    if set_type == 0:
        x = 0
        while x <= width:
            y = 0
            while y <= height:
                c = to_complex(x, y, target)
                in_set = is_in_mandelbrot_set(0, exponent, c, 0)
                if in_set:
                    target.write_pixel(x, y, in_set)
                print(str(int((x / (width + 1)) * 100)) + "%", end='\r')

                y += (1 + target.res)
            x += (1 + target.res)

    elif set_type == 1:
        x = 0
        while x <= width:
            y = 0
            while y <= height:
                z = to_complex(x, y, target)
                in_set = is_in_julia_set(z, exponent, c, 0)
                if in_set:
                    target.write_pixel(x, y, in_set)
                print(str(int((x / (width + 1)) * 100)) + "%", end='\r')

                y += (1 + target.res)
            x += (1 + target.res)


def to_complex(x, y, target):
    
    real = (((target.xmax - target.xmin) / target.width) * x) + target.xmin
    imaginary = (((target.ymin - target.ymax) / target.height) * y) + target.ymax
    return complex(real, imaginary)


def is_in_julia_set(z, exponent, c, depth):
    
    # https://en.wikipedia.org/wiki/Julia_set#Pseudocode_for_normal_Julia_sets
    result = z ** exponent + c
    if (result.real ** 2 + result.imag ** 2 <= 4) and depth < 900:
        return(is_in_julia_set(result, exponent, c, depth + 1))
    else:
        if depth < 900:
            return depth
        else:
            return False


def is_in_mandelbrot_set(z, exponent, c, depth):
    
    # https://en.wikipedia.org/wiki/Mandelbrot_set#Computer_drawings
    result = z ** exponent + c
    if (z.real ** 2 + z.imag ** 2 <= 4) and depth < 900:
        return(is_in_mandelbrot_set(result, exponent, c, depth + 1))
    else:
        if depth < 900:
            return depth
        else:
            return False


def render_set():

    red = Util.get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should red be rendered?")
    green = Util.get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should green be rendered?")
    blue = Util.get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should blue be rendered?")

    data = Text_Wrapper.TextWrapperReader(Text_Wrapper.get_file('set'))
    window = Tk()
    canvas = Canvas(window, bg='#000000', width=data.width, height=data.height)
    canvas.pack()

    def motion(event):
        x, y = event.x, event.y
        print(to_complex(x, y, data))

    window.bind('<Motion>', motion)

    max_depth = 0
    for pixel in data.pixels:
        if pixel[2] > max_depth:
            max_depth = pixel[2]

    res = data.res

    for i, pixel in enumerate(data.pixels):
        x = pixel[0]
        y = pixel[1]
        color = (-255 / (max_depth ** 2)) * ((pixel[2] - max_depth) ** 2) + 255

        if red == 0:
            r = format(255 - int(color), '02x')
        if red == 1:
            r = format(int(color), '02x')
        if red == 2:
            r = '80'
        if red == 3:
            r = '00'

        if green == 0:
            g = format(255 - int(color), '02x')
        if green == 1:
            g = format(int(color), '02x')
        if green == 2:
            g = '80'
        if green == 3:
            g = '00'

        if blue == 0:
            b = format(255 - int(color), '02x')
        if blue == 1:
            b = format(int(color), '02x')
        if blue == 2:
            b = '80'
        if blue == 3:
            b = '00'

        fill_color = '#' + r + g + b
        canvas.create_rectangle(x, y, x+res, y+res, fill=fill_color, width=0)
        print(str(int((i / (len(data.pixels) - 1)) * 100)) + "%", end='\r')

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