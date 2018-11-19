from isolation import *


class Aqua(Player):
    def __init__(self, name, token):
        super(Aqua, self).__init__(name, token)

    def take_turn(self, board):
        """
        Make a move on the Isolation board
        :param board: a Board object
        :return: a Move object
        """
        # Each subclass must implement this method
        raise NotImplementedError


class Strategy:
    def __init__(self):
        return

    def move(self, board):
        """
        Returns the id of the space to move to
        :param board: a Board object
        :return: to_space_id
        """
        raise NotImplementedError

    def push(self, board):
        """
        Returns the id of the space to push
        :param board: a Board object
        :return: push_space_id
        """
        raise NotImplementedError


class LateStrat(Strategy):

    def __init__(self):
        super(LateStrat, self).__init__()


class EarlyStrat(Strategy):

    def __init__(self):
        super(EarlyStrat, self).__init__()
