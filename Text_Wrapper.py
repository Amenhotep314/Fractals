class Text_Wrapper_Reader():

    def __init__(self, filename):
        
        self.file = []
        with open(filename, 'r') as source:
            source_list = source.readlines()
            for line in source_list:
                self.file.append(line.strip())

        self.pixels = []
        for line in self.file:
            if line.index('<x>') != -1:
                x = int(read_meta(line, 'x'))
                y = int(read_meta(line, 'y'))
                pixels.append([x, y])

        info = self.file[0]
        self.width = int(read_meta(info, 'width'))
        self.height = int(read_meta(info, 'height'))
        self.res = int(read_meta(info, 'res'))

    
    def read_meta(self, line, tag):

        length = 2 + len(tag)
        return line[line.index('<' + tag + '>') + length : line.index('</' + tag + '>')]


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