class Text_Wrapper_Reader():

    def __init__(self, filename):

        with open(filename, 'r') as source:
            self.file = [line.rstrip() for line in source.readlines()]

        self.pixels = ()
        for line in file:
            if line.index('<x>') != -1:
                x = int(read_meta(line, 'x'))
                y = int(read_meta(line, 'y'))
                pixels += (x, y)

        info = file.get(0)
        self.width = int(read_meta(info, 'width'))
        self.height = int(read_meta(info, 'height'))
        self.xscale = int(read_meta(info, 'xscale'))
        self.yscale = int(read_meta(info, 'yscale'))
        self.res = int(read_meta(info, 'res'))

    
    def read_meta(self, line, tag):
        return line[line.index('<' + tag + '>') + (2 + len(tag)) : line.index('</' + tag + '>'))]