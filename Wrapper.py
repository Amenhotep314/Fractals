from PIL import Image, ImageDraw


class TextWrapperReader():

    def __init__(self, filename, chunk=0):
        
        self.filename = filename
        self.pixels = []

        with open(filename) as source:
            for i, line in enumerate(source):
                if i == 0:
                    info = line
                    continue

                if i < 15000000 * (chunk + 1):
                    if i >= 15000000 * chunk:
                        self.pixels.append([
                            self.read_meta(line, 'x'),
                            self.read_meta(line, 'y'),
                            self.read_meta(line, 'd')
                        ])
                else:
                    break

        if not self.pixels:
            return None

        self.width = self.read_meta(info, 'w')
        self.height = self.read_meta(info, 'h')
        self.res = self.read_meta(info, 'r')

        self.xmin = self.read_meta(info, 'xmin', use_float=True)
        self.xmax = self.read_meta(info, 'xmax', use_float=True)
        self.ymin = self.read_meta(info, 'ymin', use_float=True)
        self.ymax = self.read_meta(info, 'ymax', use_float=True)

    
    def read_meta(self, line, tag, use_float=False):

        length = len(tag)
        try:
            ans = line[line.index(tag) + length : line.index('/' + tag)]
            return float(ans) if use_float else int(ans)
        except:
            return None


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