import random

# Constants
DICE_NUM_SIDES = 6
COMPUTER = 0
HUMAN = 1
OPTIONS = ["r", "q"]
COMPUTER_WINNING_PROB = 0.7


# Dice class
class Dice(object):
    def __init__(self, sides):
        self.sides = sides

    # Roll method that returns a random number between 1 and DICE_NUM_SIDES for this dice.
    def roll(self):
        return random.randrange(1, self.sides + 1)  # randrange excludes the end value, so we add 1

    # Roll method that returns a random number between half the range and DICE_NUM_SIDES for this dice.
    def roll_upper_half_of_range(self):
        return random.randrange(self.sides / 2 + 1, self.sides + 1)  # randrange excludes the end value, so we add 1


# Class that stores the result of the roll of 2 dices. It implements various methods to compare 2 rolls' results.
class TwoDiceResult(object):
    def __init__(self, result):
        self.result = result

    def __str__(self):
        return str(self.result)

    def __eq__(self, other):
        return self.result[0] == other.result[0] and self.result[1] == other.result[1]

    def __lt__(self, other):
        return self.result[0] < other.result[0] and self.result[1] < other.result[1]

    def __gt__(self, other):
        return self.result[0] > other.result[0] and self.result[1] > other.result[1]

    # Checks if the current result is a double result (same value for both dices)
    def is_double(self):
        return self.result[0] == self.result[1]

    # Returns the total value of the current result
    def get_total(self):
        return self.result[0] + self.result[1]


# Player class. It stores all the players data such as name, type, points, dices, and current roll result.
class Player(object):
    def __init__(self, name, player_type, points):
        self.name = name
        self.player_type = player_type
        self.points = points
        self.dice_1 = Dice(DICE_NUM_SIDES)
        self.dice_2 = Dice(DICE_NUM_SIDES)
        self.current_result = TwoDiceResult([0, 0])

    def __str__(self):
        return "Player: " + self.name + ", points = " + str(self.points)

    # Check if this player is "Human" or "Computer"
    def is_human(self):
        return self.player_type == HUMAN

    # Increased the player's points (by 1) and prints a winning message.
    def win(self):
        self.points += 1
        print("Player " + self.name + " wins!")

    # Roll the dices and stores their results in the "current_result" object. It also prints the result.
    def roll_dices(self):
        print("Rolling dices...")

        if self.player_type == COMPUTER:
            # Here we introduce the 70% winning probability for the "Computer" player
            if random.random() < COMPUTER_WINNING_PROB:
                # We force a random number to be generated on the upper half part of the range. This happens half
                # the times for the first dice and the other for the second dice
                if random.randrange(1, 11) % 2 == 0:
                    self.current_result = TwoDiceResult([self.dice_1.roll(), self.dice_2.roll_upper_half_of_range()])
                else:
                    self.current_result = TwoDiceResult([self.dice_1.roll_upper_half_of_range(), self.dice_2.roll()])
            else:
                self.current_result = TwoDiceResult([self.dice_1.roll(), self.dice_2.roll()])
        else:
            self.current_result = TwoDiceResult([self.dice_1.roll(), self.dice_2.roll()])

        print(self.current_result)

    # Prints the player current playing. If it's "Human" it prompts the user to choose an option: Roll or Quit.
    # This is checked with the valid options stored in the "OPTIONS" list. The "Computer" player returns the default
    # and only possible option: Roll.
    def play_turn(self):
        print("\nCurrent player: " + self.name + "\tScore: " + str(self.points))

        if self.is_human():
            while True:
                print("R: Roll dices \t Q: Quit")

                option = input("Enter an option: ").lower()

                if option in OPTIONS:
                    return option
                else:
                    print("Invalid option.")
        else:
            return OPTIONS[0]


# Function that handles a round based on the order of the players. When the "Human" player chooses an option, this is
# compared with the quitting option "Quit" ("q") before rolling the dices. The "Computer" player does not need this
# checking and rolls the dices immediately. A list "OPTIONS" is used to store all possible options. When both players
# have rolled the dices, their results are compared with the "check_results" function.
def play_round(players):
    if players[0].is_human():
        if players[0].play_turn() == OPTIONS[1]:
            return OPTIONS[1]

        players[0].roll_dices()

        players[1].play_turn()
        players[1].roll_dices()
    else:
        players[0].play_turn()
        players[0].roll_dices()

        if players[1].play_turn() == OPTIONS[1]:
            return OPTIONS[1]

        players[1].roll_dices()

    check_results(players)


# Function to compare the rolls' results of 2 players. the player method "win" is called on the appropriate player
# in order to update and print the score. When both players get the same result a message is printed.
def check_results(players):
    if players[0].current_result.is_double() and not players[1].current_result.is_double():
        players[0].win()
    elif not players[0].current_result.is_double() and players[1].current_result.is_double():
        players[1].win()
    elif players[0].current_result.is_double() and players[1].current_result.is_double():
        if players[0].current_result > players[1].current_result:
            players[0].win()
        elif players[0].current_result < players[1].current_result:
            players[1].win()
        else:
            print("It's a draw!")
    elif players[0].current_result.get_total() > players[1].current_result.get_total():
        players[0].win()
    elif players[0].current_result.get_total() < players[1].current_result.get_total():
        players[1].win()
    else:
        print("It's a draw!")


# Main function that initializes the players, the rounds counter and starts an infinite loop. Inside the loop the mod
# operator is used on the round number to switch the order of the players' turns. The loop finalizes when the player
# has chosen the Quit option ("q").
def main():
    print("Welcome to the Cheater’s Dice game")
    player_name = input("Enter your name: ")

    computer = Player("COMPUTER", COMPUTER, 0)
    player = Player(player_name, HUMAN, 0)

    current_round = 1
    quitting = False

    while not quitting:
        if current_round % 2 == 0:
            players = [computer, player]
        else:
            players = [player, computer]

        print("\n***** Round " + str(current_round) + " *****")
        option = play_round(players)

        if option == "q":
            quitting = True

        current_round += 1


if __name__ == "__main__":
    main()
