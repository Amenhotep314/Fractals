class TextWrapperReader():

    def __init__(self, filename):
        
        self.filename = filename
        self.file = []
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

    def __init__(self, filename, width, height, xmin, xmax, ymin, ymax, res):

        self.filename = filename + '.set'
        self.width = width
        self.height = height
        self.res = res

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        file = open(self.filename, 'w')
        file.close()
        self.file = open(self.filename, 'a')
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


def get_file(extension):

    from os import listdir
    from Util import get_choice

    files = []
    for file in listdir():
        if file.endswith('.' + extension):
            files.append(file)

    if len(files) == 0:
        print("No files with the extension \"" + extension + "\" found.")
        return False

    return files[get_choice(files, "Please select a file")]