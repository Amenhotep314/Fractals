def get_choice(options, prompt):

    while True:
        print(prompt + "(1 - " + str(len(options)) + "):")
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