# This is a sample Python script.
import abc
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import random
from enum import Enum
from itertools import cycle

KNOCKOUTROLL = 16
HIGHEST_ROLL = 6
LOWERST_ROLL = 1
MAX_LIFE = 6


class Action(Enum):
    ROLL = 1
    DECREMENT_LIFE = 2


class StartRule(Enum):
    RANDOMSTART = 1
    LOSERSTARTS = 2
    FIXED = 3


class Player(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def play(self, currentCount, numberOfLifes, nextPlayerLifes, avgPlayerLives):
        pass

    @abc.abstractmethod
    def getId(self):
        pass


class Dennis(Player):
    id = -1

    def __init__(self, playerId):
        self.id = playerId

    @classmethod
    def play(self, currentCount, numberOfLifes, nextPlayerLifes, avgPlayerLives):
        if numberOfLifes == 1:
            return Action.ROLL
        if currentCount + HIGHEST_ROLL >= KNOCKOUTROLL:
            return Action.DECREMENT_LIFE
        return Action.ROLL

    def getId(self):
        return self.id

class Mario(Player):
    id = -1

    def __init__(self, playerId):
        self.id = playerId

    @classmethod
    def play(self, currentCount, numberOfLifes, nextPlayerLifes, avgPlayerLives):
        if numberOfLifes == 1:
            return Action.ROLL
        if currentCount == 10:
            return Action.ROLL
        if currentCount + HIGHEST_ROLL >= KNOCKOUTROLL:
            return Action.DECREMENT_LIFE
        return Action.ROLL

    def getId(self):
        return self.id

class Andre(Player):
    id = -1

    def __init__(self, playerId):
        self.id = playerId

    @classmethod
    def play(self, currentCount, numberOfLifes, nextPlayerLifes, avgPlayerLives):
        if numberOfLifes == 1:
            return Action.ROLL
        if currentCount == 10 and numberOfLifes < avgPlayerLives:
            return Action.ROLL
        if currentCount + HIGHEST_ROLL >= KNOCKOUTROLL:
            return Action.DECREMENT_LIFE
        return Action.ROLL

    def getId(self):
        return self.id


def roll():
    return random.randint(LOWERST_ROLL, HIGHEST_ROLL)


def applyThreeIsZeroRule(roll):
    if roll == 3:
        return 0
    return roll


class Game:
    playerList = []
    score = {}

    def __init__(self, playerList):
        self.playerList = playerList
        for player in playerList:
            self.score[player.getId()] = MAX_LIFE

    def start(self):
        #print("Game Started")
        currentCount = 0
        running = True
        pool = cycle(self.playerList)
        nextPlayer = next(pool)
        while running:
            player, nextPlayer = nextPlayer, next(pool)
            action = player.play(currentCount, self.score[player.getId()], self.score[nextPlayer.getId()], sum(self.score.values()) / len(self.score))
            if action == Action.DECREMENT_LIFE:
                self.score[player.getId()] = self.score[player.getId()] - 1
                #print("Player " + str(player.getId()) + " DECREMENT LIFE FROM: " + str(
                #    self.score[player.getId()] + 1) + "-->" + str(
                #    self.score[player.getId()]))
                currentCount = 0
                if self.score[player.getId()] == 0:
                    #print("Player " + str(player.getId()) + " LOST")
                    return player
            rollValue = roll()
            currentCount = currentCount + applyThreeIsZeroRule(rollValue)
            #print("Player " + str(player.getId()) + " ROLL: " + str(rollValue) + " new COUNT: " + str(currentCount))
            if currentCount >= KNOCKOUTROLL:
                #print("Player " + str(player.getId()) + " LOST")
                return player


def restart_list(lst, restart_index):
    return lst[restart_index:] + lst[:restart_index]
class Session:
    playerAndScore = {}
    numberOfGames = 100
    startrule = StartRule.RANDOMSTART

    def __init__(self, playerlist, numberOfGames, startrule):
        for player in playerlist:
            self.playerAndScore[player] = 0
        self.numberOfGames = numberOfGames
        self.startrule = startrule


    def sortByStartRule(self, players, rule, lastLooserId):
        if rule == StartRule.RANDOMSTART:
            random.shuffle(players)
        if rule == StartRule.LOSERSTARTS:
            restart_index = players.index(lastLooserId);
            players = restart_list(players, restart_index)
        return players

    def run(self):
        playerList = list(Session.playerAndScore.keys())
        for i in range(self.numberOfGames):
            #print("Start Game No.: " + str(i + 1))
            game = Game(playerList)
            loserPlayer = game.start()
            playerList = self.sortByStartRule(playerList, self.startrule, loserPlayer)
            Session.playerAndScore[loserPlayer] = Session.playerAndScore.get(loserPlayer, 0) + 1

    def printResult(self):
        for player, losts in self.playerAndScore.items():
            print("Player " + str(player.getId()) + " of type: " + str(type(player).__name__) + " lost games: " + str(
                losts) + " lost pct: " + str((losts/sum(self.playerAndScore.values())) * 100) + "%")


def createDennisOnlyGame(numberOfPlayers):
    playerList = []
    for i in range(numberOfPlayers):
        playerList.append(Mario(i + 1))
    return playerList


def oneMarioAgainstFourDennis():
    return [Mario(1), Mario(2), Mario(3), Mario(4), Dennis(5)]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    session = Session([Mario(1), Mario(2), Mario(3)], 100000, StartRule.LOSERSTARTS)
    session.run()
    print("---------- RESULTS ----------")
    session.printResult()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
