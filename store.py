from textColor import BoldColor
import random
from setting import Setting


class Store():
    def __init__(self, settings):
        self.settings = settings
        self.reveal_order = []
        self.store_name = "Wacky Wordle Store"
        self.win_rate = 100

        self.hints = 3
        self.coin_balance = 500
        self.hint_rate = 50
        self.guessedChars = []
        self.hint_count = 0
        self.hintSTR = []
        for i in range(settings.getValue('maxguess')-1):
            self.hintSTR.append('_ ')

    def getGuessedChars(self):
        return self.guessedChars

    def getCoinBalance(self):
        return self.coin_balance

    def getHintBalance(self):
        return self.hints

    def buyHints(self, amount):
        self.hint_rate = self.settings.getValue('hint rate')
        color = BoldColor.instance()
        balance = self.coin_balance - (amount * self.hint_rate)
        if balance < 0:
            print("Sorry, you cannot buy hints at this time. You don't have enough money.")
        else:
            self.coin_balance = balance
            self.hints += amount
            print(f"{color.GREEN}You had {color.YELLOW}{self.hints - amount}{color.END} hints and {color.YELLOW}{self.coin_balance + (amount * self.hint_rate)}{color.END} coins previously but now you have {color.END}{color.YELLOW}{self.hints}{color.END}{color.GREEN} hints and your balance is {color.END}{color.YELLOW}{self.coin_balance}{color.END}{color.GREEN} coins. {color.END}")

    def getHint(self, answer: str, prefix):
        color = BoldColor.instance()
        if self.hints - 1 < 0:
            print(
                color.BLUE + f"Sorry, you do not have any more hints left. Please buy hints from the {self.store_name} using the command " + color.END + color.YELLOW + prefix + "buyHints" + color.END)
        else:
            self.hints -= 1
            hint = ''
            ans_char_lst = []
            for c in answer:
                ans_char_lst.append(c)

            if self.hint_count == 0:
                end = False
                while not end:
                    number = random.randrange(0, len(answer))
                    if number not in self.reveal_order:
                        self.reveal_order.append(number)
                    if len(self.reveal_order) == len(answer):
                        end = True

            for i in range(len(answer)):
                if i == self.reveal_order[self.hint_count]:
                    self.hintSTR[i] = answer[self.reveal_order[self.hint_count]] + " "

            for v in self.hintSTR:
                hint += v

            self.hint_count += 1
            print()
            print(color.YELLOW + hint + color.END)

            print(color.RED + "Your current hint balance is now ", self.hints, "hints" + color.END)