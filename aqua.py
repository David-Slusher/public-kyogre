from isolation import *


class Aqua(Player):
    def __init__(self, name, token):
        super(Aqua, self).__init__(name, token)
        self._enemyToken = Board.BLUE_TOKEN if self._token == Board.RED_TOKEN else Board.RED_TOKEN

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
        enemyLocation = token_location(self._enemyToken)

        # TODO
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
    def __init__(self, board, token, enemyToken):
        self.board = board
        self.token = token
        self.enemyToken = enemyToken

    def move(self):
        """
        Returns the id of the space to move to
        :param board: a Board object
        :return: to_space_id
        """
        raise NotImplementedError

    def push(self):
        """
        Returns the id of the space to push
        :param board: a Board object
        :return: push_space_id
        """
        raise NotImplementedError

    def moving_closer(self, start, tile):
        """
        Return true if a tile is closer to the enemy pawn than a start tile
        :param start: The starting tile
        :param tile: The tile under consideration for moving to
        :return: True if tile is closer to the enemy pawn than start, False if not
        """
        if self.board.distance_between(tile, self.enemyToken) <= self.board.distance_between(start, self.enemyToken) - 1:
            return True
        else:
            return False

    def path_exists(self, start):
        """
        Determines if a path exists to the enemy pawn in which the player pawn can continuously move
        towards the enemy
        :param start: The starting tile
        :return: True if a path exists, False if not
        """
        exists = False
        for tile in self.board.neighbor_tiles(start):
            if self.moving_closer(start, tile):
                if exists or self.enemyToken in self.board.neighbor_tiles(tile):
                    return True
                else:
                    if not exists:
                        exists = self.path_exists(start)
        return exists

    def potentialMoves(self, start):
        """
        Determines which of the spaces possible is the safest to move to where safeness is defined
        as the number of neighbroing tiles a tile has such that the max safety is 8
        :param start: The starting tile
        :return: A sorted list of tuples containg the possible tiles with their safety rating
        """
        tileSafenessList = [(tile, self.safety(tile)) for tile in self.board.neighbor_tiles(start)
            if path_exists(tile)]
        tileSafenessListSorted = sorted(tileSafenessList, key = lambda x: x[1])

        return tileSafenessListSorted

    def safety(self, tile):
        """
        Deterimine the safety of a given tile where safety is defined on a scale of 0, meaning the
        tile has no neighboring tiles, to 8, meaning all neighboring tiles are present and not pushed out
        :param tile: a tile on the board
        :return: the number of neighboring tiles a tile has
        """
        return len(self.board.neighbor_tiles(tile))

    def potentialPushes(enemy):

        voidEdgeList = [(tile, getVoidEdges(tile)) for tile in self.board.neighbor_tiles(enemy)]
        voidEdgeListSorted = sorted(voidEdgeList, key = lambda x: x[1])

        return voidEdgeListSorted

    def getVoidEdges(tile):

        return 8 - len(neighbor_tiles(tile))


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
