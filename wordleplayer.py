from textColor import BoldColor
from store import Store
from setting import Setting

setting = Setting.instance()

class WordlePlayer():
    def __init__(self, name, total_tries):
        self.store = Store(setting)
        self.name = name
        self.total_tries = total_tries # Max number of tries a player has to guess the correct answer

        # GUESS GRAPH
        self.graph_dictionary = {}  # a (key : value) dictionary of the player's attempts
        self.graph_tags = {}  # a (key : value) dictionary of hashtags

        for key in range(1, self.total_tries + 1):
            self.graph_dictionary[key] = 0  # initializes all the attempts to be 0
            self.graph_tags[key] = '#'

        # UPDATE STATS
        self.played_games = 0
        self.won_games = 0

        # STREAKS (CURRENT AND MAX)
        self.current_streak = 0
        self.max_streak = 0

    def getName(self):
        return self.name

    def updateStats(self, won, tries):
        color = BoldColor.instance()
        # GENERAL UPDATES
        self.played_games += 1

        # CONDITIONALS
        if won:
            self.store.coin_balance += self.store.win_rate
            self.won_games += 1
            self.current_streak += 1
            self.graph_dictionary[tries] += 1
            if self.max_streak < self.current_streak:
                self.max_streak = self.current_streak
        else:
            self.current_streak = 0

        try:
            # GUESS GRAPH
            graph_keys = []
            graph_values = []
            for k in self.graph_dictionary:
                graph_keys.append(k)
                graph_values.append(self.graph_dictionary[k])
            idx = 0
            graph_tag_values = []
            for v in graph_values:
                graph_tag_values.append((v, graph_keys[idx]))
                idx += 1

            graph_tag_values = sorted(graph_tag_values, reverse=True)
            greatest = graph_tag_values[0][0]
            count = 1
            for t in graph_tag_values:
                interval = t[count]
                value = t[count - 1]
                set_tags = int(20 * (value / greatest))

                if value == 0:
                    self.graph_tags[interval] = '#'
                else:
                    self.graph_tags[interval] = (set_tags * '#') + '#'

            self.guess_graph = ''
            for x in self.graph_tags:
                self.guess_graph += color.PURPLE + color.BOLD + f'{x}' + color.END + ' : ' + color.RED + self.graph_tags[x] + color.END + '\n'

        except:
            print(color.RED + color.BOLD + "There was an error in updating your stats. Please try again later.\n\n" + color.END)

    def winPercentage(self):
        try:
            self.win_percentage = (self.won_games / self.played_games) * 100
            return f"{self.win_percentage}%"
        except:
            print("There was an error in updating your stats. Please try again later.")

    def gamesPlayed(self):
        return self.played_games

    def currentStreak(self):
        return self.current_streak

    def maxStreak(self):
        return self.max_streak

    def displayStats(self):
        color = BoldColor.instance()
        possessive_stats = f"{self.name}'s Stats:"
        print(color.PURPLE + color.BOLD + color.UNDERLINE + possessive_stats.upper() + color.END)
        print(color.BLUE + color.BOLD + "Games Played: ", end='' + color.END)
        print(self.gamesPlayed())
        print(color.BLUE + color.BOLD + "Win Percentage: ", end='' + color.END)
        print(self.winPercentage())
        print(color.BLUE + color.BOLD + "Current Streak: ", end='' + color.END)
        print(self.currentStreak())
        print(color.BLUE + color.BOLD + "Maximum Streak: ", end='' + color.END)
        print(self.maxStreak())
        print(color.BLUE + color.BOLD + "Guess Graph: " + color.END)
        try:
            print(self.guess_graph)
        except:
            print("There was an error in updating your graph. Please try again later.")

    def setName(self, name):
        self.name = name
