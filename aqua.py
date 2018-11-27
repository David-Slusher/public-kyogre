from isolation import *


class Aqua(Player):
    def __init__(self, name, token):
        super(Aqua, self).__init__(name, token)
        self.enemyToken = Board.BLUE_TOKEN if self._token == Board.RED_TOKEN else Board.RED_TOKEN
    def take_turn(self, board):
        """
        Make a move on the Isolation board and push out space
        :param board: a Board object
        :return: a Move object
        """
        # Each subclass must implement this method
        raise NotImplementedError

        # where pawn currently is
        currentTile = board.token_location(self._token)

        # 8 (max) surrounding squares
        neighbors = board.neighbor_tiles(space_id)

        # everything that can be pushed out
        tiledSpaces = board.push_outable_square_ids()

        # start spaces that cannot be pushed out
        startSpaces = board.start_squares()

        # get enemy current location
        # used to see if we can move towards the enmey
        enemyLocation = token_location(self.enemyToken)

        #TODO
        # spaceMovedTo = algorithm decision

        # remove the space we moved to from the spaces that can be pushed out
        tiledSpaces.discard(spaceMovedTo)

        #space we just moved from can be pushed out now
        tiled_spaces.add(space_id)

        # to choose which space to be pushed out, select one that is closest to enemy
        # and has the most number of void edges where a void edge is defined as
        # a space neighboring the selected space that is pushed out and edges of the board count as
        # pushed out

        # neighbors include pushed out squares
        enemyNeighbors = neighbors(enemyLocation)

        # move = isolation.Move(to_space_id, push_out_space_id)
        # print('   ', move)
        # return move
        #


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
    """
    Follow the Late Strategy of moving to space with
    most available moves on next turn
    """
    def __init__(self):
        super(LateStrat, self).__init__()



class EarlyStrat(Strategy):
    """
    Follow the Early Strategy of moving toward enemy pawn
    """
    def __init__(self):
        super(EarlyStrat, self).__init__()
