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

        length = 2 + len(tag)
        return line[line.index('<' + tag + '>') + length : line.index('</' + tag + '>')]


def get_file(extension):

    from os import listdir

    files = []
    for file in listdir():
        if file.endswith('.' + extension):
            files.append(file)

    if len(files) == 0:
        print("No files with the extension \"" + extension + "\" found.")
        return False
    
    while True:
        print("Select a file (1 - " + str(len(files)) + "):")
        for i, file in enumerate(files):
            print(str(i + 1) + '. ' + file)
        choice = input('>>> ')

        try:
            choice = int(choice)
            if(choice > 0 and choice <= len(files)):
                return file[choice - 1]
            else:
                print("That's not one of the choices.")
        except ValueError:
            print("Please enter a number.")