def get_choice(options, prompt):

    while True:
        print('\n' + prompt + " (1 - " + str(len(options)) + "):")
        for i, option in enumerate(options):
            print(str(i + 1) + '. ' + option)
        choice = input('>>> ')

        try:
            choice = int(choice)
            if(choice > 0 and choice <= len(options)):
                return choice - 1
            else:
                print("That's not one of the choices.")
        except ValueError:
            print("Please enter a number.")


def get_number(prompt, bound=0, require_positive=True, use_float=False):

    while True:
        print('\n' + prompt)
        choice = input('>>> ')

        try:
            if use_float:
                choice = float(choice)
            else:
                choice = int(choice)
            if bound != 0 and choice > bound:
                print("That value is too high.")
            elif require_positive and choice < 0:
                print("Your input must be positive.")
            else:
                return choice
        except ValueError:
            print("Please enter a number.")


def get_complex(prompt):

    while True:
        print('\n' + prompt)
        real = get_number("Real part", require_positive=False, use_float=True)
        imaginary = get_number("Imaginary part", require_positive=False, use_float=True)

        try:
            choice = complex(float(real), float(imaginary))
            return choice
        except ValueError:
            print("Please enter numbers.")


def get_string(prompt):

    print('\n' + prompt)
    choice = input('>>> ')
    return choice


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


def to_complex(x, y, target):
    
    real = (((target.xmax - target.xmin) / target.width) * x) + target.xmin
    imaginary = (((target.ymin - target.ymax) / target.height) * y) + target.ymax
    return complex(real, imaginary)