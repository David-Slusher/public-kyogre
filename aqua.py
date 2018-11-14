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
