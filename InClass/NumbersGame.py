import random
from copy import deepcopy

numbers = random.sample(range(10000), 50)
numbers2 = deepcopy(numbers)

def play_game(game="biggest_end"):
    turn = random.randrange(0,1,1)
    player1, npc = 0, 0
    game_type = globals()[game]
    while len(numbers) != 0:
        print(numbers)
        if turn == 1:
            print("Player goes first")
            move = input("First or Last?\n")
            if move in ("first", "First"):
                player1 += numbers.pop(0)
            else:
                player1 += numbers.pop(len(numbers) - 1)
            turn = 0
        else:
            print("Computer goes first")
            npc += game_type()
            turn = 1
        print()
        print("Scores:")
        print("\tYour Score: ", player1)
        print("\t CPU Score: ", npc)
    if player1 > npc:
        print("You win!")
    else:
        print("Computer wins!")


def play_game_test(strat1="first", strat2="last"):
    turn = random.randrange(0,1,1)
    player1, player2 = 0, 0
    strategy1 = globals()[strat1]
    strategy2 = globals()[strat2]
    while len(numbers) != 0:
        print(numbers)
        if turn == 1:
            print("Turn: Player1")
            player1 += strategy1()
            turn = 0
        else:
            print("Turn: Player2")
            player2 += strategy2()
            turn = 1 
        print()
        print("Scores:")
        print("\tPlayer1 Score: ", player1)
        print("\tPlayer2  Score: ", player2)
    if strat1 == strat2:
        strat1 += "1"
        strat2 += "2"
    who = strat1
    if player1 > player2:
        print("Player1 wins!")
    else:
        print("Player2 wins!")
        who = strat2
    return who


def look_ahead():
    length = len(numbers)
    if length >= 3:
        start = numbers[0]
        mid1 = numbers[1]
        mid2 = numbers[2]
        end = numbers[length-1]
        if start >= end:
            if end >= mid2:
                if start >= mid1:
                    return first()
                else:
                    if (mid1 - start) <= (start - mid2):
                        return first()
                    else:
                        return last()
            else:
                if start >= mid1:
                    return first()
                else:
                    if (mid1 - start) >= (mid2 - end):
                        return first()
                    else:
                        return last()
        else:
            if end <= mid2:
                if start >= mid1:
                    if (start - mid1) >= (mid2 - end):
                        return first()
                    else:
                        return last()
                else:
                    if (mid1 - start) >= (mid2 - end):
                        return last()
                    else:
                        return first()
            else:
                if start >= mid1:
                    return last()
                else:
                    return first()
    else:
        return biggest_end()

def biggest_end():
    if numbers[0] > numbers[len(numbers) - 1]:
        return first()
    else:
        return last()

def first():
    print("Choose first")
    return numbers.pop(0)

def last():
    print("Choose last")
    return numbers.pop(len(numbers)-1)

def numDiv(num, div):
    if num <= 1:
        return 0
    if num == div:
        return 1
    return numDiv(num-div, div) + 1

rules = '''
The Numbers Game

Rules:
You and another player (here, the computer)
are given a even length list of some length.
You both repeatedly remove items from the
list until no more items remain by taking 
the first or last item.

Good luck!
'''

print(rules)

## ("Want to play?")
possible_strats = ["first", "last", "biggest_end", "look_ahead"]
winners = dict()

for item in possible_strats:
    for item2 in possible_strats:
        winners[str(item + " v " + item2)] = play_game_test(item, item2)
        numbers = deepcopy(numbers2)
outputFile = "numbers_game_results.txt"

with open(outputFile, "a+") as output:
    for key in winners:
        print(f"Test: {key} : \t\t {winners[key]}")
        output.write(str(winners[key]) + "\n")

results = dict()
for item in possible_strats:
    results[item] = 0

total = 0

with open(outputFile, "r") as readFile:
    for line in readFile:
        in_line = str(line).strip()
        if in_line in possible_strats:
            results[in_line] += 1
        total += 1

total = numDiv(total, len(possible_strats)^2)
print(total)

print("Average Wins per Appearance:")
for key in results:
    print(f"{key} : {100*results[key]/(total*(len(possible_strats)-1))} %")


#play_game("look_ahead")

