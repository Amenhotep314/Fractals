from PIL import Image, ImageDraw


class TextWrapperReader():

    def __init__(self, filename, chunk=None):
        
        self.filename = filename
        self.file = []

        if chunk:
            with open(filename) as source:
                for i, line in enumerate(source):
                    if i < 15000000 * (chunk + 1):
                        if i >= 15000000 * chunk:
                            self.file.append(line)
                    else:
                        break
                    
            if not self.file:
                return False

        else:
            with open(filename, 'r') as source:
                source_list = source.readlines()
                for line in source_list:
                    self.file.append(line.strip())

        self.pixels = []
        for line in self.file:
            if '/d' in line:
                x = int(self.read_meta(line, 'x'))
                y = int(self.read_meta(line, 'y'))
                depth = int(self.read_meta(line, 'd'))
                self.pixels.append([x, y, depth])

        info = self.file[0]
        self.width = int(self.read_meta(info, 'w'))
        self.height = int(self.read_meta(info, 'h'))
        self.res = int(self.read_meta(info, 'r'))

        self.xmin = float(self.read_meta(info, 'xmin'))
        self.xmax = float(self.read_meta(info, 'xmax'))
        self.ymin = float(self.read_meta(info, 'ymin'))
        self.ymax = float(self.read_meta(info, 'ymax'))

    
    def read_meta(self, line, tag):

        length = len(tag)
        return line[line.index(tag) + length : line.index('/' + tag)]


class TextWrapperWriter():

    def __init__(self, filename, width, height, xmin, xmax, ymin, ymax, res, c, exponent):

        self.filename = filename
        self.width = width
        self.height = height
        self.res = res

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self.c = c
        self.exponent = exponent

        file = open(self.filename + '.set', 'w')
        file.close()
        self.file = open(self.filename + '.set', 'a')
        self.write_meta(self.width, "w", newline=False)
        self.write_meta(self.height, "h", newline=False)
        self.write_meta(self.xmin, "xmin", newline=False)
        self.write_meta(self.xmax, "xmax", newline=False)
        self.write_meta(self.ymin, "ymin", newline=False)
        self.write_meta(self.ymax, "ymax", newline=False)
        self.write_meta(self.res, "r")

    
    def write_pixel(self, x, y, depth):

        self.write_meta(str(x), 'x', newline=False)
        self.write_meta(str(y), 'y', newline=False)
        self.write_meta(str(depth), 'd')

    
    def write_meta(self, item, tag, newline=True):

        self.file.write(tag + str(item) + '/' + tag)
        if newline:
            self.file.write('\n')


class ImageWrapper():

    def __init__(self, filename, width, height, res, red, green, blue, rshade, gshade, bshade):
        
        self.filename = filename
        self.width = width
        self.height = height
        self.res = res

        self.red = red
        self.green = green
        self.blue = blue
        self.rshade = rshade
        self.gshade = gshade
        self.bshade = bshade

        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    
    def write_pixel(self, x, y, color):

        r = self.calculate_shade(self.red, self.rshade, color)
        g = self.calculate_shade(self.green, self.gshade, color)
        b = self.calculate_shade(self.blue, self.bshade, color)
        fill_color = '#' + format(r, '02x') + format(g, '02x') + format(b, '02x')
        self.draw.rectangle([x, y, x+self.res, y+self.res], fill=fill_color, outline=fill_color)
        return fill_color


    def calculate_shade(self, choice, chosen_shade, color):

        if choice == 0:
            return 255 - color
        if choice == 1:
            return color
        if choice == 2:
            return chosen_shade
        if choice == 3:
            return 0


    def save_image(self):

        self.image.save(self.filename.replace('.set', '.png'))