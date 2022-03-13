from textColor import BoldColor

class Store():
    def __init__(self):
        self.store_name = "Wacky Wordle Store"

        self.hints = 3
        self.coin_balance = 500
        self.hintRate = 50


    def getCoinBalance(self):
        return self.coin_balance

    def getHintBalance(self):
        return self.hints


    def buyHints(self, amount):
        balance = self.coin_balance - (amount * self.hintRate)
        if balance < 0:
            print("Sorry, you cannot buy hints at this time. You don't have enough money.")
        else:
            self.coin_balance = balance
            self.hints += amount

    def getHint(self, answer, prefix):
        color = BoldColor
        if self.hints - 1 < 0:
            print(color.RED + f"Sorry, you do not have any more hints left. Please buy hints from the {self.store_name} using the command " + color.END + color.YELLOW + prefix + "buyHints" + color.END)
        else:
            self.hints -= 1

            char_list = []
            for l in answer:
                char_list.append(l)






        print(color.RED + "Your current hint balance is now ", self.hints, "hints" + color.END)