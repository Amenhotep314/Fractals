from tkinter import *
from random import randint


width = 400
height = 400

window = Tk()
canvas = Canvas(window, width=width, height=height)
canvas.pack()


def main():

    for i in range(width):
        for j in range(height):
            fill = random_color()
            print(fill + "\t" + str(i) + ' x ' + str(j))
            canvas.create_rectangle(i, j, i, j, fill=fill, outline='')
            


def random_color():

    r = format(randint(0, 255), '02x')
    g = format(randint(0, 255), '02x')
    b = format(randint(0, 255), '02x')

    return '#' + r + g + b


if __name__ == "__main__":
    main()
    window.mainloop()