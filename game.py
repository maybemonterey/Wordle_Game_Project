import string

from CommandProcessor import CommandProcessor
from setting import Setting
from wordbank import WordBank
from wordleword import WordleWord
from wordleplayer import WordlePlayer
from textColor import BoldColor
from store import Store

settings = Setting.instance()
settings.setSetting('maxguess', 6)
settings.setSetting('difficulty', 'normal')
settings.setSetting('prefix', '/')
settings.setSetting('hint rate', 50)

color = BoldColor.instance()

prefix = settings.getValue('prefix')
alphabet = "abcdefghijklmnopqrstuvwxyz"
letters = WordleWord("abcdefghijklmnopqrstuvwxyz")
maxGuesses = settings.getValue('maxguess')
gave_up = False
max_hints_per_round = 3
store = Store(settings)


def getPlayerGuess(answer):
    player_guess = input(f"Please enter a {len(answer)} letter word : ")
    player_guess.lower()
    return player_guess


def checkCommands(input):
    command = input[1:]
    if command in CommandProcessor.instance().getCommandMap():
        return True


def markGuess(word, guess, alpha):
    guessedChars = store.getGuessedChars()
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
            if guess.getWord()[v] not in guessedChars:
                guessedChars.append(guess.getWord()[v])

        elif guess_list[v] in word_list:
            guess.setMisplaced(v)
            letters.setMisplaced((alphabet.index(guess_list[v])))
            if guess.getWord()[v] not in guessedChars:
                guessedChars.append(guess.getWord()[v])


name = (input(color.YELLOW + "Please enter your name: \n" + color.END)).lower().capitalize()
print(color.PURPLE + color.BOLD + f"Hi {name}! Let's play the game of Wordle!\n" + color.END)


def playRound():
    global play

    CommandProcessor.instance().process_command('info', settings=settings, color=color, store=store, player=None)

    CC = input("Shall we start? Please type 'yes' or 'no'.\n")
    CP = checkCommands(CC)
    if CP:
        CommandProcessor.instance().process_command(CC[1:], settings=settings, color=color, store=store, player=None)
        valid = False
    if CC == 'yes' or CC == 'no' or CP:
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
        print(color.YELLOW + f"Remember, you can always access the commands using the prefix ('{prefix}') [which can be changed] to help you out.\n\n"
              + color.RED + color.UNDERLINE + "ALRIGHT LET'S PLAY!\n" + color.END)

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


def playWordle(max_Guesses):
    all_words = WordBank("words_alpha.txt")
    five_words = WordBank("common5letter.txt")
    answer = five_words.getRandom()
    # answer = "delta" --> for testing code
    player = WordlePlayer(name, max_Guesses)

    endRound = False
    round_count = 0
    tries = 0

    while not endRound:
        max_Guesses = int(settings.getValue('maxguess'))

        check = False
        player_guess = getPlayerGuess(answer)
        ww_player_guess = WordleWord(player_guess)

        check = checkCommands(player_guess)

        valid = True
        if check:
            CommandProcessor.instance().process_command(player_guess[1:], settings=settings, color=color, store=store,
                                                        player=player, answer=answer, guess=player_guess)
        elif not five_words.contains(player_guess) or not all_words.contains(player_guess) and not check:
            valid = False

        while not valid:
            check = checkCommands(player_guess)
            if check:
                CommandProcessor.instance().process_command(player_guess[1:], settings=settings, color=color, store=store, player=player, answer=answer, guess=player_guess)
                break
            elif not five_words.contains(player_guess) or not all_words.contains(player_guess):
                player_guess = input(
                    f"I'm sorry; that is not a valid guess nor a valid command. Please answer a {len(answer)} letter word : ")
                ww_player_guess = WordleWord(player_guess)
            else:
                valid = True

        if valid and not check:
            markGuess(answer, ww_player_guess, letters)
            print(f"\n{ww_player_guess}")
            print(f"{letters}\n")

            round_count += 1
            tries += 1

            if player_guess == answer:
                print(color.GREEN + f'You got it! You won within {tries} tries! Congratulations!' + color.END)
                player.updateStats(True, tries)
                endRound = True

        if (round_count >= max_Guesses) or gave_up:
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
