class TextWrapperReader():

    def __init__(self, filename):
        
        self.file = []
        with open(filename, 'r') as source:
            source_list = source.readlines()
            for line in source_list:
                self.file.append(line.strip())

        self.pixels = []
        for line in self.file:
            if '<x>' in line:
                x = int(self.read_meta(line, 'x'))
                y = int(self.read_meta(line, 'y'))
                depth = int(self.read_meta(line, 'depth'))
                self.pixels.append([x, y, depth])

        info = self.file[0]
        self.width = int(self.read_meta(info, 'width'))
        self.height = int(self.read_meta(info, 'height'))
        self.res = int(self.read_meta(info, 'res'))

    
    def read_meta(self, line, tag):

        length = 2 + len(tag)
        return line[line.index('<' + tag + '>') + length : line.index('</' + tag + '>')]


class TextWrapperWriter():

    def __init__(self, filename, width, height, res, c):

        from math import sqrt

        self.filename = filename + '.set'
        self.width = width
        self.height = height
        self.res = res
        self.c = c

        file = open(self.filename, 'w')
        file.close()

        self.write_meta(self.width, "width", newline=False)
        self.write_meta(self.height, "height", newline=False)
        self.write_meta(self.res, "res", newline=False)
        self.write_meta(self.c, "c", newline=False)

    
    def write_pixel(self, x, y, depth):

        self.write_meta(str(x), 'x', newline=False)
        self.write_meta(str(y), 'y', newline=False)
        self.write_meta(str(depth), 'depth')

    
    def write_meta(self, item, tag, newline=True):

        with open(self.filename, "a") as target:
            target.write("<" + tag + ">" + str(item) + "</" + tag + ">")
            if newline:
                target.write('\n')


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