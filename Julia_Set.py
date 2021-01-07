from tkinter import Tk, Canvas
from random import randint
from PIL import Image, ImageDraw

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

    set_type = Util.get_choice(["Mandelbrot set", "Julia set", "Burning ship"], "Set type")
    width = Util.get_number("Width of set in pixels")
    height = Util.get_number("Height of set in pixels")
    xmin = Util.get_number("Minimum x value", use_float=True, require_positive=False)
    xmax = Util.get_number("Maximum x value", use_float=True, require_positive=False)
    ymin = Util.get_number("Minimum y value", use_float=True, require_positive=False)
    ymax = Util.get_number("Maximum y value", use_float=True, require_positive=False)
    res = Util.get_number("Resolution (0 checks one pixel at a time, 1 checks 4, 2 checks 9, ...)", bound=1079)
    if set_type == 1:
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

    elif set_type == 2:
        x = 0
        while x <= width:
            y = 0
            while y <= height:
                c = to_complex(x, y, target)
                in_set = is_in_burning_ship(0, exponent, c, 0)
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


def is_in_burning_ship(z, exponent, c, depth):
    
    # https://en.wikipedia.org/wiki/Burning_Ship_fractal
    result = (complex(abs(z.real), abs(z.imag))) ** exponent + c
    if (z.real ** 2 + z.imag ** 2 <= 4) and depth < 900:
        return(is_in_burning_ship(result, exponent, c, depth + 1))
    else:
        if depth < 900:
            return depth
        else:
            return False


def render_set():

    file = Text_Wrapper.get_file('set')
    
    red = Util.get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should red be rendered?")
    if red == 2:
        rshade = Util.get_number("Shade", bound=255)

    green = Util.get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should green be rendered?")
    if green == 2:
        gshade = Util.get_number("Shade", bound=255)

    blue = Util.get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should blue be rendered?")
    if blue == 2:
        bshade = Util.get_number("Shade", bound=255)

    data = Text_Wrapper.TextWrapperReader(file)
    window = Tk()
    window.title(file)
    canvas = Canvas(window, bg='#000000', width=data.width, height=data.height)
    canvas.pack()

    image = Image.new("RGB", (data.width, data.height))
    draw = ImageDraw.Draw(image)

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
            r = 255 - int(color)
        if red == 1:
            r = int(color)
        if red == 2:
            r = rshade
        if red == 3:
            r = 0

        if green == 0:
            g = 255 - int(color)
        if green == 1:
            g = int(color)
        if green == 2:
            g = gshade
        if green == 3:
            g = 0

        if blue == 0:
            b = 255 - int(color)
        if blue == 1:
            b = int(color)
        if blue == 2:
            b = bshade
        if blue == 3:
            b = 0

        fill_color = '#' + format(r, '02x') + format(g, '02x') + format(b, '02x')
        canvas.create_rectangle(x, y, x+res, y+res, fill=fill_color, outline=fill_color)
        draw.rectangle([x, y, x+res, y+res], fill=fill_color, outline=fill_color)
        print(str(int((i / (len(data.pixels) - 1)) * 100)) + "%", end='\r')

    image.save(file.replace('.set', '.png'))
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