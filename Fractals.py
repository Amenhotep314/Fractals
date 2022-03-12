from random import randint
from tkinter import Tk, Canvas

from Util import *
from Wrapper import *


def main():

    print("\nWelcome to Fractal Set Generator & Renderer")

    while True:
        choice = get_choice(["Generate a set", "Render a set to an image", "Quit"], "What would you like to do?")

        if choice == 0:
            generate_single_set()
        elif choice == 1:
            render_single_set()
        else:
            print("Thank you for using the Fractal Set Generator & Renderer!")
            quit()


def generate_single_set():

    set_types = [generate_mandelbrot_set, generate_julia_set, generate_burning_ship, generate_tricorn]
    set_type = get_choice(["Mandelbrot set", "Julia set", "Burning ship", "Tricorn"], "Set type")
    set_function = set_types[set_type]

    xmin = get_number("Minimum x value", use_float=True, require_positive=False)
    xmax = get_number("Maximum x value", use_float=True, require_positive=False)
    ymin = get_number("Minimum y value", use_float=True, require_positive=False)
    ymax = get_number("Maximum y value", use_float=True, require_positive=False)

    height = get_number("Height of set in pixels")
    width = int((height / abs(ymax - ymin)) * abs(xmax - xmin))
    print("Width auto-set to " + str(width) + ".")

    res = get_number("Resolution (0 checks one pixel at a time, 1 checks 4, 2 checks 9, ...)", bound=1079)

    if set_type == 1:
        c = get_complex("C value")
    else:
        c = None

    exponent = get_number("Exponent", use_float=True)

    filename = get_string("File to save set to")
    target = TextWrapperWriter(filename, width, height, xmin, xmax, ymin, ymax, res, c, exponent)
    
    set_function(target)


def generate_mandelbrot_set(target):

    y = 0
    while y <= target.height:
        x = 0
        while x <= target.width:
            c = to_complex(x, y, target)

            in_set = is_in_mandelbrot_set(0, target.exponent, c, 0)

            if in_set:
                target.write_pixel(x, y, in_set)
            print(str(int((y / (target.height + 1)) * 100)) + "%", end='\r')
            x += (1 + target.res)
        y += (1 + target.res)


def generate_julia_set(target):

    y = 0
    while y <= target.height:
        x = 0
        while x <= target.width:
            z = to_complex(x, y, target)

            in_set = is_in_julia_set(z, target.exponent, target.c, 0)

            if in_set:
                target.write_pixel(x, y, in_set)
            print(str(int((y / (target.height + 1)) * 100)) + "%", end='\r')
            x += (1 + target.res)
        y += (1 + target.res)

    
def generate_burning_ship(target):

    y = 0
    while y <= target.height:
        x = 0
        while x <= target.width:
            c = to_complex(x, y, target)

            in_set = is_in_burning_ship(0, target.exponent, c, 0)

            if in_set:
                target.write_pixel(x, y, in_set)
            print(str(int((y / (target.height + 1)) * 100)) + "%", end='\r')
            x += (1 + target.res)
        y += (1 + target.res)
        

def generate_tricorn(target):

    y = 0
    while y <= target.height:
        x = 0
        while x <= target.width:
            c = to_complex(x, y, target)

            in_set = is_in_tricorn(0, target.exponent, c, 0)

            if in_set:
                target.write_pixel(x, y, in_set)
            print(str(int((y / (target.height + 1)) * 100)) + "%", end='\r')
            x += (1 + target.res)
        y += (1 + target.res)


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


def is_in_tricorn(z, exponent, c, depth):

    result = complex_conjugate(z) ** exponent + c
    if (z.real ** 2 + z.imag ** 2 <= 4) and depth < 900:
        return(is_in_tricorn(result, exponent, c, depth + 1))
    else:
        if depth < 900:
            return depth
        else:
            return False


def render_single_set():

    file = get_file('set')
    data = TextWrapperReader(file, chunk=0)

    rshade = 0
    gshade = 0
    bshade = 0

    red = get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should red be rendered?")
    if red == 2:
        rshade = get_number("Shade", bound=255)

    green = get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should green be rendered?")
    if green == 2:
        gshade = get_number("Shade", bound=255)

    blue = get_choice(["Light to dark", "Dark to light", "Solid", "None"], "How should blue be rendered?")
    if blue == 2:
        bshade = get_number("Shade", bound=255)

    target = ImageWrapper(file, data.width, data.height, data.res, red, green, blue, rshade, gshade, bshade)

    if(data.width * data.height > 15000000):
        del data
        print("Defaulting to chunk-based approach for enormous data set. No interactive view available.")
        render_set_chunkily(file, target)
    else:
        render_set(data, target)


def render_set(data, target, interactive=True):

    if interactive:
        window = Tk()
        window.title(data.filename)
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
        color = int((-255 / (max_depth ** 2)) * ((pixel[2] - max_depth) ** 2) + 255)

        fill_color = target.write_pixel(x, y, color)

        if interactive:
            canvas.create_rectangle(x, y, x+res, y+res, fill=fill_color, outline=fill_color)
        print(str(int((i / (len(data.pixels) - 1)) * 100)) + "%", end='\r')

    # signature = TextWrapperReader("signature.set")
    # xorigin = data.width - 63
    # yorigin = data.height - 50
    # for pixel in signature.pixels:
    #     x = pixel[0]
    #     y = pixel[1]
    #     draw.rectangle([x+xorigin, y+yorigin, x+xorigin, y+yorigin], fill='#FFFFFF', outline='#FFFFFF')

    target.save_image()

    if interactive:
        window.mainloop()


def render_set_chunkily(file, target):

    max_depth = 0
    incrementer = 0
    data = TextWrapperReader(file, chunk=incrementer)
    res = target.res

    print("Calculating maximum recursion depth.")
    print("%\t#")
    while data.pixels:
        for i, pixel in enumerate(data.pixels):
            if pixel[2] > max_depth:
                max_depth = pixel[2]
            print(str(int((i / (len(data.pixels) - 1)) * 100)) + "%" + '\t' + str(incrementer + 1), end='\r')

        del data
        incrementer += 1
        data = TextWrapperReader(file, chunk=incrementer)
    print()

    incrementer = 0
    data = TextWrapperReader(file, chunk=incrementer)

    print("Rendering to image.")
    print("%\t#")
    while data.pixels:
        for i, pixel in enumerate(data.pixels):
            x = pixel[0]
            y = pixel[1]
            color = int((-255 / (max_depth ** 2)) * ((pixel[2] - max_depth) ** 2) + 255)
            target.write_pixel(pixel[0], pixel[1], color)
            print(str(int((i / (len(data.pixels) - 1)) * 100)) + "%" + '\t' + str(incrementer + 1), end='\r')

        del data
        incrementer += 1
        data = TextWrapperReader(file, chunk=incrementer)
        target.save_image()


if __name__ == "__main__":

    main()