import string

from CommandProcessor import CommandProcessor
from setting import Setting
from wordbank import WordBank
from wordleword import WordleWord
from wordleplayer import WordlePlayer
from textColor import BoldColor
from store import Store

settings = Setting()
settings.setSetting('maxguess', 6)
settings.setSetting('difficulty', 'normal')
settings.setSetting('prefix', '/')

color = BoldColor.instance()

prefix = settings['prefix']
alphabet = "abcdefghijklmnopqrstuvwxyz"
letters = WordleWord("abcdefghijklmnopqrstuvwxyz")
maxGuesses = settings.getValue('maxguess')
gave_up = False
max_hints_per_round = 3
store = Store()


def getPlayerGuess(answer):
    player_guess = input(f"Please enter a {len(answer)} letter word : ")
    player_guess.lower()
    return player_guess


def process_settings():
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


def displayInfo():
    maxGuesses = settings.getValue('maxguess')
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


def checkCommands(guess, answer, player, prefix):
    command = guess[1:]

    return CommandProcessor.instance().process_command(command, setings=settings, color=color, store=store)

    # if command == 'settings':
    #     return process_settings()
    # elif command == 'cPrefix':
    #     return process_cPrefix()
    # elif command == 'rPrefix':
    #     prefix = '/'
    #     return True
    #
    # elif command == 'give':
    #     gave_up = True
    #     return True
    #
    # elif command == 'hint':
    #     store.getHint(answer, prefix)
    #     return True
    #
    # elif command == 'buyHints':
    #     try:
    #         amount = int(input("How many hints would you like to buy? "))
    #     except:
    #         print("That is not a valid amount, please run the command again. ")
    #
    #     store.buyHints(amount)
    #     print(
    #         color.RED + f"• Your current hint balance is {hint_count}\n" + f"• Your current coin balance is {coin_balance}\n" + color.END)
    #     return True
    #
    # elif command == 'name':
    #     player.setName(name=input("What is the name you want to change to? Please enter it here : "))
    #
    #     return True
    #
    # elif command == 'info':
    #     print()
    #     print(color.UNDERLINE + color.LIGHT_PURPLE + "INFORMATION COMMAND RUN:" + color.END)
    #     displayInfo()
    #     return True
    #
    #
def process_cPrefix():
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
    print(color.RED + "Changes have been saved." + color.END)
    settings["prefix"] = _prefix
    prefix = settings["prefix"]
    return True


def markGuess(word, guess, alpha):
    word_list = []
    guess_list = []
    for l in word:
        word_list.append(l)
    for l in guess.getWord():
        if l not in guess_list:
            guess_list.append(l)
        else:
            guess_list.append(None)

    for v in range(len(word_list)):
        if word_list[v] == guess_list[v]:
            guess.setCorrect(v)
            letters.setCorrect(alphabet.index(guess_list[v]))
        elif guess_list[v] in word_list:
            guess.setMisplaced(v)
            letters.setMisplaced((alphabet.index(guess_list[v])))


command_list = ['settings', 'cPrefix', 'rPrefix', 'give', 'hint', 'name', 'info', 'buyHints']

name = (input("Please enter your name: ")).lower().capitalize()
print(color.PURPLE + color.BOLD + f"Let's play the game of Wordle {name}!" + color.END)


def playRound():
    global play

    displayInfo()

    CC = input("Shall we start? Please type 'yes' or 'no'.")
    if CC == 'yes' or CC == 'no':
        valid = True
    else:
        valid = False

    while not valid:
        if CC != 'yes' and CC != 'no':
            CC = input("I'm sorry; that is not a valid input. Please answer either 'yes' or 'no'.")
        else:
            valid = True
            break
    if CC == 'no':
        play = False
    else:
        play = True

    # PLAY WORDLE
    while play:
        print(color.RED + color.UNDERLINE + "ALRIGHT LET'S PLAY!" + color.END)

        playWordle(maxGuesses)

        CC = input("Do you want to play again? Please type 'yes' or 'no'.")

        if CC == 'yes' or CC == 'no':
            valid = True
        while not valid:
            if CC != 'yes' or CC != 'no':
                CC = input("I'm sorry; that is not a valid input. Please answer either 'yes' or 'no'.")
            else:
                valid = True
        if CC == 'no':
            play = False
            print(color.BLUE + "Okay! Bye, bye! <3" + color.END)
        else:
            play = True


def playWordle(maxGuesses):
    all_words = WordBank("words_alpha.txt")
    five_words = WordBank("common5letter.txt")
    # answer = five_words.getRandom()
    answer = "delta"
    player = WordlePlayer(name, maxGuesses)

    endRound = False
    round_count = 0
    tries = 0

    while not endRound:

        check = False
        player_guess = getPlayerGuess(answer)
        ww_player_guess = WordleWord(player_guess)

        check = checkCommands(player_guess, answer, player, prefix)

        valid = True
        if not five_words.contains(player_guess) or not all_words.contains(player_guess):
            valid = False

        while not valid:
            if not five_words.contains(player_guess) or not all_words.contains(player_guess):
                if not check:
                    player_guess = input(
                        f"I'm sorry; that is not a valid guess. Please answer a {len(answer)} letter word : ")
                    ww_player_guess = WordleWord(player_guess)
                else:
                    break
            else:
                valid = True

        if valid:
            markGuess(answer, ww_player_guess, letters)
            print(ww_player_guess)
            print(letters)

            if not check:
                round_count += 1
                tries += 1

            if player_guess == answer:
                print(color.GREEN + f'You got it! You won within {tries} tries! Congratulations!' + color.END)
                player.updateStats(True, tries)
                endRound = True

        if (round_count >= maxGuesses) or gave_up:
            print(
                color.RED + f"Sorry, you lost with {tries} tries. The word was " + color.END + color.YELLOW + answer + color.END)
            player.updateStats(False, tries)
            endRound = True
            break

    player.displayStats()


def main():
    playRound()


if __name__ == "__main__":
    main()
