from tkinter import Tk, Canvas
from random import randint


def main():

    for i in range(width):
        for j in range(height):
            fill = random_color()
            print(fill + "\t" + str(i) + ' x ' + str(j))        


def render_set(data):

    window = Tk()
    canvas = Canvas(window, width=data.width, height=data.height)
    canvas.pack()

    res = data.res

    for pixel in data.pixels:
        x = pixel(0)
        y = pixel(1)
        canvas.create_rectangle(x, y, x+res, y+res, fill='#FF00FF', outline='')

    window.mainloop()


if __name__ == "__main__":
    main()