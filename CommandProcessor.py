from Singleton import Singleton

command_map = {}


def init():
    command_map["settings"] = process_settings
    command_map["info"] = displayInfo


"""
This class processes commands
"""


def process_settings(args):
    settings = args['settings']
    color = args['color']

    print(
        "Please choose which setting you would like to set : " + color.RED + "1) 'maxguess'" + color.END + ', ' + color.RED + "2) 'difficulty'" + color.END)
    try:
        option = int(input("Enter the setting number : "))
    except:
        print("Invalid input, please run the command again.")
    if option == 1:
        amt = input("What are the maximum number of guesses you would like to have? : ")
        settings.setSetting('maxguess', amt)
        print(color.RED + "Changes have been saved." + color.END)

    elif option == 2:
        difficulty = input(
            f"Please code a difficulty level: 1 [easy], 2 [normal], 3 [hard].\nYour current difficulty is set to {settings['difficulty']}")
        settings['difficulty'] = difficulty
        print(color.RED + "Changes have been saved." + color.END)
    else:
        print(f"{color.RED}Invalid setting option. Please run the command again.{color.END}")

    return True


def displayInfo(args):
    settings = args['settings']
    color = args['color']
    store = args['store']
    maxGuesses = settings.getValue('maxguess')
    prefix = settings["prefix"]

    print(color.RED + "Some Basic Information:" + color.END)
    print("• The current PREFIX is : " + color.YELLOW + f"'{prefix}'" + color.END)
    print(
        "• The current maximum number of GUESSES you have is : " + color.RED + f"{maxGuesses} " + color.END + color.YELLOW + "guesses" + color.END)
    print(
        "• Your current coin balance is " + color.YELLOW + f"{store.getCoinBalance()} " + color.END + "coins, which you can use to buy hints")
    print(
        "• Your current hint balance is " + color.YELLOW + f"{store.getHintBalance()} " + color.END + "hints, which you can use to buy hints")
    print()
    print(color.RED + "Also, here are some commands for you:" + color.END)
    print("To set SETTINGS : " + color.YELLOW + prefix + "settings" + color.END)
    print("To change the PREFIX : " + color.YELLOW + prefix + "cPrefix" + color.END)
    print("To reset the PREFIX : " + color.YELLOW + prefix + "rPrefix" + color.END)
    print("To GIVE UP : " + color.YELLOW + prefix + "give" + color.END)
    print("To get a HINT : " + color.YELLOW + prefix + "hint" + color.END)
    print("To BUY HINTS : " + color.YELLOW + prefix + "buyHints" + color.END)
    print("To change your NAME : " + color.YELLOW + prefix + "name" + color.END)
    print("To see this INFORMATION again : " + color.YELLOW + prefix + "info" + color.END)
    print()


@Singleton
class CommandProcessor:
    def __init__(self):
        self.args = {}

    def init_args(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'store':
                self.args['store'] = value
            elif key == 'color':
                self.args['color'] = value
            elif key == 'settings':
                self.args['settings'] = value

    def process_command(self, command_name, **kwargs):

        self.init_args(**kwargs)

        if command_name not in command_map:
            return False

        return command_map[command_name](self.args)
