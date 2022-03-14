from Singleton import Singleton
from textColor import BoldColor


def process_give(args):
    gave_up = True
    return True

def process_cPrefix(args):
    settings = args['settings']
    color = args['color']
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    valid = False
    count = 0
    msg = "Please enter a single symbol for a prefix : "
    while not valid:
        if count > 0:
            msg = f"That is not a valid prefix. Please answer a single symbol for a prefix :"

        _prefix = input(msg)
        count = 1

        if _prefix not in alphabet and len(_prefix) == 1:
            valid = True
    settings.setSetting('prefix', _prefix)
    print(f"{color.RED}Changes have been saved.{color.END}")
    return True


def process_settings(args):
    settings = args['settings']
    color = args['color']
    prefix = settings.getValue('prefix')

    print(
        f"Please choose which setting you would like to change : {color.RED} (1) 'maxguess' | (2) 'difficulty' | (3) 'prefix' | (4) 'hint rate'{color.END}")
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
            f"Please code a difficulty level: 1 [easy], 2 [normal], 3 [hard].\nYour current difficulty is set to {settings.getValue('difficulty')}")
        settings.setSetting('difficulty', difficulty)
        print(color.RED + "Changes have been saved." + color.END)

    elif option == 3:
        c = input(f"{color.YELLOW} Would you like to CHANGE the prefix [CHANGE] or RESET the prefix [RESET]?")
        if c == 'CHANGE':
            CommandProcessor.instance().process_command('cPrefix', settings=settings, color=color)
        elif c == 'RESET':
            settings.setSetting('prefix', '/')
            print(f"{color.RED}Changes have been saved.{color.END}")
        else:
            print(f"{color.RED} Sorry that was an invalid input, please run the command again. A shortcut command to changing you prefix and resetting you prefix is {prefix}cPrefix and {prefix}rPrefix respectively. {color.END}")
    elif option == 4:
        settings.setSetting('hint rate', int(input(f"{color.RED}What would you like the cost of 1 hint to be?: {color.END}")))
        print(f"{color.RED}Changes are saved. You new hint rate is {settings.getValue('hint rate')}.{color.END}")
    else:
        print(f"{color.RED}Invalid setting option. Please run the command again.{color.END}")

    return True


def displayInfo(args):
    settings = args['settings']
    color = args['color']
    store = args['store']
    maxGuesses = settings.getValue('maxguess')
    prefix = settings.getValue("prefix")

    print(color.RED + "Some Basic Information:" + color.END)
    print("• The current PREFIX is : " + color.YELLOW + f"'{prefix}'" + color.END)
    print(
        "• The current maximum number of GUESSES you have is : " + color.RED + f"{maxGuesses} " + color.END + "guesses")
    print(
        "• Your current coin balance is " + color.YELLOW + f"{store.getCoinBalance()} " + color.END + f"coins, which you can use to{color.YELLOW} buy {color.END}hints")
    print(
        "• Your current hint balance is " + color.YELLOW + f"{store.getHintBalance()} " + color.END + "hints, which you can use to help you in the game")
    print()
    print(color.RED + "Also, here are some basic commands for you:" + color.END)
    print("• To set SETTINGS : " + color.YELLOW + prefix + "settings" + color.END)
    print("• To change the PREFIX : " + color.YELLOW + prefix + "cPrefix" + color.END)
    print("• To reset the PREFIX : " + color.YELLOW + prefix + "rPrefix" + color.END)
    print("• To get a HINT : " + color.YELLOW + prefix + "hint" + color.END)
    print("• To BUY HINTS : " + color.YELLOW + prefix + "buyHints" + color.END)
    print("• To GIVE UP : " + color.YELLOW + prefix + "give" + color.END)
    print("• To change your NAME : " + color.YELLOW + prefix + "name" + color.END)
    print("• To see this INFORMATION again : " + color.YELLOW + prefix + "info" + color.END)
    print()

def give_hint(args):
    color = BoldColor.instance()
    # try:
    store = args['store']
    answer = args['answer']
    settings = args['settings']
    prefix = settings.getValue('prefix')
    store.getHint(answer, prefix)
    return True
    # except:
    #     print(f"{color.ITALIC}{color.RED}Sorry hints are unavailable at this time. Please try again later.{color.END}")

def buy_hints(args):
    store = args['store']
    color = args['color']
    settings = args['settings']
    hint_count = store.getHintBalance()
    coin_balance = store.getCoinBalance()
    try:
        amount = int(input(f"{color.RED}How many hints would you like to buy? The hint rate it is {settings.getValue('hint rate')} coins per hint. {color.END}"))
        store.buyHints(amount)
        print(color.RED + f"• Your current hint balance is {store.getHintBalance()}\n" + f"• Your current coin balance is {store.getCoinBalance()}\n" + color.END)
    except:
        print("That is not a valid amount, please run the command again. ")

    return True

def set_name(args):
    player = args['player']
    player.setName(name=input("What is the name you want to change to? Please enter it here : "))

    return True


@Singleton
class CommandProcessor:
    def __init__(self):
        self.args = {}
        self.command_map = {}
        self.command_map['settings'] = process_settings
        self.command_map['info'] = displayInfo
        self.command_map['cPrefix'] = process_cPrefix
        self.command_map['give'] = process_give
        self.command_map['hint'] = give_hint
        self.command_map['buyHints'] = buy_hints
        self.command_map['name'] = set_name

    def getCommandMap(self):
        return self.command_map

    def init_args(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'store':
                self.args['store'] = value
            elif key == 'color':
                self.args['color'] = value
            elif key == 'settings':
                self.args['settings'] = value
            elif key == 'player':
                self.args['player'] = value
            elif key == 'answer':
                self.args['answer'] = value
            elif key == 'guess':
                self.args['guess'] = value

    def process_command(self, command_name, **kwargs):
        self.init_args(**kwargs)
        # command_name must be already without the prefix char

        if command_name not in self.command_map:
            return False

        return self.command_map[command_name](self.args)