from lib2to3.pgen2.parse import ParseError
# from typing import List
import numpy as np
from numpy.random import randint
from termcolor import colored

class Raflespil:
    def __init__(self, deterministic = False):
        self.det = deterministic
        self.board  = list(range(1,10))
        self.played = []

    def partitions(self, n, I=1):
        yield (n,)
        for i in range(I, n//2 + 1):
            for p in self.partitions(n-i, i):
                if i not in p:
                    yield (i,) + p

    def tick(self, die_sum, plays):
        s = sum(plays)
        # PLAY JUST A SINGLE TICK
        if die_sum == s:
            if all([ x not in self.played for x in plays ]):
                self.played += plays
                return True
            else:
                ticked = [ x in self.played for x in plays ]
                print(f"Invalid play, you've ticked {ticked} already.")
                return False
        else:
            print("Invalid play, the two dice must sum to your ticks.")
            return False

    def roll(self):
        if sum([ x for x in self.board if x not in self.played ]) <= 6:
            return [randint(1,6)]
        return [randint(1,6), randint(1,6)]

    def help(self):
        return

    def valid_plays(self, die_sum, played_param = None):
        if played_param == None:
            played_param = self.played
        parts = list(self.partitions(die_sum))
        plays = [ part for part in parts if all([ x not in played_param for x in part ]) ]
        return plays

    def is_valid_play(self, die_sum, played_param = None):
        if played_param == None:
            played_param = self.played
        return len(self.valid_plays(die_sum, played_param)) > 0

    def round(self):
        die = self.roll()
        print(f"Current board: [", end=" ")
        for n in self.board:
            if n not in self.played:
                print(f"[{n}] ", end="")
            else:
                print(" X ", end=" ")
        print("]")
        die_str = " and a ".join([ str(d) for d in die ])
        print(f"You rolled a {die_str}.")

        if not self.is_valid_play(sum(die)):
            return False

        print(f"What would you like to knock down:")
        while(True):
            try:
                ans = input()
                plays = [ int(i) for i in ans.split() ]
                if len(plays) == 0:
                    print("Please input an answer.")
                if len(plays) <= 4:
                    if self.tick(sum(die), plays):
                        break
                else:
                    print("Too many ticks, please input only two.")
            except ParseError:
                print("Parse error, please try input again.")
        
        return True

    def play(self):
        print("Would you like to read the rules? [y/n]")
        ans = input()
        if (ans == "y"):
            self.help()
        while (self.round()):
            pass
        print(colored("Game over.", attrs=['bold']), "Your score is:")
        nums = "".join([ str(i) for i in range(1,10) if i not in self.played ])
        score = "0 (WIN!)" if nums == "" else nums
        print(score)
        return

MEMO = {}

def all_Raf_helper(G, played):
    scores = []
    for sum_roll in range(2, 13):
        if not G.is_valid_play(sum_roll, played):
            score = "".join([ str(i) for i in range(1,10) if i not in played ])
            if score == "":
                score = "0"
            scores += [ score ]
        else:
            for play in G.valid_plays(sum_roll, played):
                played_str = "".join([ str(x) for x in sorted(played) ])
                play_str   = "".join([ str(x) for x in sorted(list(play)) ])
                if (play_str, played_str) in MEMO:
                    scores += MEMO[(play_str, played_str)]
                else:
                    res = all_Raf_helper(G, played + list(play))
                    MEMO[(play_str, played_str)] = res
                    scores += res       
    return scores

def all_Rafles(G):
    scores = all_Raf_helper(G, [])
    score_np = np.array(scores)
    return score_np
    

def simulation():
    G = Raflespil()
    all_scores = all_Rafles(G)
    print(np.unique(all_scores, return_counts=True))
    return
    # pass

if __name__ == "__main__":
    #### RUN SIMULATION
    # simulation()

    #### PLAY USING CLI
    while (True):
        print("Want to play", colored("Raflespil?", attrs=['bold']), "[y/n]")
        ans = input()
        if (ans != "y"):
            break
        game = Raflespil()
        game.play()
