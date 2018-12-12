from isolation import *
from math import *
from itertools import *
import copy


class Aqua(Player):
    def __init__(self, name, token):
        super(Aqua, self).__init__(name, token)
        # self._token, self._name in superclass
        self._enemyToken = Board.BLUE_TOKEN if self._token == Board.RED_TOKEN else Board.RED_TOKEN
        self._strategy = EarlyStrat(self._token, self._enemyToken)

    def take_turn(self, board):
        """
        Make a move on the Isolation board and push out space
        :param board: a Board object
        :return: a Move object
        """
        if not self._strategy.moves(board, currentTile):
            self._strategy = LateStrat(self._token, self._enemyToken)
        return self._strategy.minimax(board, 20, -math.inf, math.inf, True)[1]

class Strategy:
    def __init__(self, token, enemyToken):
        # self.board = board
        self._token = token
        self._enemyToken = enemyToken

    def moves(self, board, token):
        """
        Returns the ids of the potential spaces to move to
        :param board: a Board object
        :param token: a token string
        :return: to_space_id
        """
        raise NotImplementedError

    def pushouts(self, board, token):
        """
        Returns the ids of the potential spaces to push
        :param board: a Board object
        :param token: a token string
        :return: push_space_id
        """
        raise NotImplementedError

    def safety(self, board, tile):
        """
        Deterimine the safety of a given tile where safety is defined on a scale of 0,
        meaning the tile has no neighboring tiles, to 8, meaning all neighboring tiles
        are present and not pushed out
        :param board: a Board object
        :param tile: a tile on the board
        :return: the number of neighboring tiles a tile has
        """
        return len(board.neighbor_tiles(tile))

    # position is board state, children are all possible moves, static eval of position is
    # number of neighbor_tiles
    # alpha should be -infinity, beta should be +infinity
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):

        # if at end of a path on the tree OR their are no possible moves to make
        if depth == 0 or not board.neighbor_tiles(self._token) or not board.neighbor_tiles(self._enemyToken): #or len(self.board.neighbor_tiles(token_location)) == 0:
            return len(board.neighbor_tiles(self._token)) - len(board.neighbor_tiles(self._enemyToken)), None
        if maximizingPlayer:
            maxEval = -math.inf
            bestMove = None
            # max 8 children - one for each neighbor tile that a pawn can move to
            for child in list(combinations_with_replacement(self.moves(board, self._token),
                                                            self.pushouts(board, self._enemyToken))):
                ourMove = Move(child[0], child[1])
                boardCopy = copy.deepcopy(board)
                boardCopy.make_move(self._token, ourMove)
                eval = self.minimax(boardCopy, depth - 1, alpha, beta, False)[0]
                if eval > maxEval:
                    bestMove = ourMove
                    maxEval = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, bestMove

        else:
            minEval = math.inf
            for child in list(combinations_with_replacement(board.neighbor_tiles(board.token_location(self._enemyToken)),
                                                            board.push_outable_square_ids())):
                theirMove = Move(child[0], child[1])
                boardCopy = copy.deepcopy(board)
                boardCopy.make_move(self._token, theirMove)
                eval = self.minimax(boardCopy, depth - 1, alpha, beta, True)[0]
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if alpha <= beta:
                    break
            return minEval, None


class LateStrat(Strategy):
    """
    Follow the Late Strategy of moving to space with
    most available moves on next turn
    """
    def __init__(self, token, enemyToken):
        super(LateStrat, self).__init__(token, enemyToken)

    def moves(self, board, token):
        """
        Returns the ids of the potential spaces to move to
        :param board: a Board object
        :param token: a token string
        :return: to_space_id
        """
        return board.neighbor_tiles(token)

    def pushouts(self, board, token):
        """
        Returns the ids of the potential spaces to push
        :param board: a Board object
        :param token: a token string
        :return: push_space_id
        """
        return board.push_outable_square_ids()

class EarlyStrat(Strategy):
    """
    Follow the Early Strategy of moving toward enemy pawn
    """
    def __init__(self, token, enemyToken):
        super(EarlyStrat, self).__init__(token, enemyToken)

    def moves(self, board, token):
        """
        Returns list of first values in list of tuples created in potentialEarlyMoves
        :param board: A Board object
        :param token: a token string
        :return: a list of tile ids that are possible move locations
        """
        return [move[0] for move in self.potentialEarlyMoves(board, board.token_location(token))]

    def pushouts(self, board, token):
        """
        Returns the ids of the potential spaces to push
        :param board: a Board object
        :param token: a token string
        :return: push_space_id
        """
        return [push[0] for push in self.potentialPushes(board, board.token_location(token))]

    def potentialEarlyMoves(self, board, tokenLocation):
        """
        Determines which of the spaces possible is the safest to move to where safeness is defined
        as the number of neighbroing tiles a tile has such that the max safety is 8
        :param board: A Board object
        :param tokenLocation: a tile id for the token
        :return: A sorted list of tuples containg the possible tiles with their safety rating
        """
        tileSafenessList = [(tile, self.safety(board, tile)) for tile in board.neighbor_tiles(tokenLocation)
                            if self.path_exists(board, tile)]
        tileSafenessListSorted = sorted(tileSafenessList, key=lambda x: x[1], reverse=True)

        return tileSafenessListSorted

    def path_exists(self, board, start):
        """
        Determines if a path exists to the enemy pawn in which the player pawn can continuously move
        towards the enemy
        :param board: A Board object
        :param start: The starting tile
        :return: True if a path exists, False if not
        """
        exists = False
        for tile in board.neighbor_tiles(start):
            if self.moving_closer(board, start, tile):
                if exists or self._enemyToken in board.neighbor_tiles(tile):
                    return True
                else:
                    if not exists:
                        exists = self.path_exists(board, tile)
        return exists

    def moving_closer(self, board, start, tile):
        """
        Return true if a tile is closer to the enemy pawn than a start tile
        :param board: A Board object
        :param start: The starting tile
        :param tile: The tile under consideration for moving to
        :return: True if tile is closer to the enemy pawn than start, False if not
        """
        if board.distance_between(tile, self._enemyToken) <= board.distance_between(start, self._enemyToken) - 1:
            return True
        else:
            return False

    def potentialPushes(self, board, enemy):
        """
        Determine which of the enemy's neighboring tiles is the best tile to push using void edge
        heuristic where the tile with the most void edges in the neighbor tiles is the ideal push
        :param board: A Board object
        :param enemy: the enemy tile location
        :return: a sorted list of the neighboring tiles in descending order of void edges
        """
        voidEdgeList = [(tile, self.getVoidEdges(board, tile)) for tile in board.neighbor_tiles(enemy)]
        voidEdgeListSorted = sorted(voidEdgeList, key=lambda x: x[1], reverse=True)

        return voidEdgeListSorted

    def getVoidEdges(self, board, tile):
        """
        Determine the number of void edges of a given tile
        :param board: A Board object
        :param tile: a tile on the Board
        :return: an integer representing the number of pushed out spaces within the
        neighbors of tile
        """
        return 8 - len(board.neighbor_tiles(tile))
