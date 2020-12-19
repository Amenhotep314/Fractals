def get_choice(options, prompt):

    while True:
        print(prompt + " (1 - " + str(len(options)) + "):")
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


def get_number(prompt, bound=0, require_positive=True):

    while True:
        print(prompt)
        choice = input('>>> ')

        try:
            choice = int(choice)
            if bound != 0 and choice > bound:
                print("That value is too high.")
            elif require_positive and choice < 0:
                print("Your input must be positive.")
            else:
                return choice
        except ValueError:
            print("Please enter a number.")


def get_string(prompt):

    print(prompt)
    choice = input('>>> ')
    return choice

