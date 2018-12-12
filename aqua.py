from isolation import *
from math import *
from itertools import *

class Aqua(Player):
    def __init__(self, name, token):
        super(Aqua, self).__init__(name, token)
        self._enemyToken = Board.BLUE_TOKEN if self._token == Board.RED_TOKEN else Board.RED_TOKEN
        self._strategy = EarlyStrat()

    def take_turn(self, board):
        """
        Make a move on the Isolation board and push out space
        :param board: a Board object
        :return: a Move object
        """
        # Each subclass must implement this method
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
        if not self._strategy.moves(currentTile):
            self._strategy = LateStrat()

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

        # intial call
        # minimax(currentPosition, depth of tree, -infinity, +infinity, true)


class Strategy:
    def __init__(self, board, token, enemyToken):
        self.board = board
        self.token = token
        self.enemyToken = enemyToken

    def moves(self):
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

    def safety(self, tile):
        """
        Deterimine the safety of a given tile where safety is defined on a scale of 0,
        meaning the tile has no neighboring tiles, to 8, meaning all neighboring tiles
        are present and not pushed out
        :param tile: a tile on the board
        :return: the number of neighboring tiles a tile has
        """
        return len(self.board.neighbor_tiles(tile))

    # position is board state, children are all possible moves, static eval of position is
    # number of neighbor_tiles
    # alpha should be -infinity, beta should be +infinity
    def minimax(board, depth, alpha, beta, maximizingPlayer):
        maxEval = math.inf
        # if at end of a path on the tree OR their are no possible moves to make
        if depth == 0: #or len(self.board.neighbor_tiles(token_location)) == 0:
            return len(neighbor_tiles(token)) - len(neighbor_tiles(enemyToken))
        if maximizingPlayer:
            #
            # max 8 children - one for each neighbor tile that a pawn can move to
            for child in list(combinations_with_replacement(moves(board), pushouts(board))):
                ourMove = Move()
                ourMove.to_square_id = child[0]
                ourMove.pushout_square_id = child[1]
                boardCopy = copy.deepcopy(board)
                boardCopy.make_move(token, ourMove)
                eval = minimax(child, depth - 1, alpha, beta, false)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = -math.inf
            for child in list(combinations_with_replacement(moves(board), pushouts(board))):
                theirMove = Move()
                theirMove.to_square_id = child[0]
                theirMove.pushout_square_id = child[1]
                boardCopy = copy.deepcopy(board)
                boardCopy.make_move(token, theirMove)
                eval = minimax(child, depth - 1, alpha, beta, true)
                minEval = max(minEval, eval)
                beta = max(beta, eval)
                if alpha <= beta:
                    break
            return minEval

class LateStrat(Strategy):
    """
    Follow the Late Strategy of moving to space with
    most available moves on next turn
    """
    def __init__(self):
        super(LateStrat, self).__init__()

    def potentialLateMoves(self,token):
        """
        Determine the spaces that we can move to with the highest safety and extended safety
        :return: dictionary of moves with tuples of safety and extended safety as the value
        """
        neighbors = self.board.neighbor_tiles(self.board.token_location(token))
        moveDict = {}
        for neighbor in neighbors:
            tile = neighbor
            safeness = safety(neighbor)
            totalSafeness = 0
            extendedNeighbors = self.board.neighbor_tiles(neighbor)
            for extendedNeighbor in extendedNeighbors:
                extended_safeness = safety(extendedNeighbor)
                totalSafeness += extended_safeness
            moveDict[tile] = (safeness, totalSafeness)
        return moveDict

    def boxThemIn(self, enemyToken):
        """
        Determine the best push to box the enemy in so that they have a smaller playing space than
        our token
        :param enemyToken: the location of the enemy
        :return: the best move as decided by hueristic to reduce the enemy playing space
        """



class EarlyStrat(Strategy):
    """
    Follow the Early Strategy of moving toward enemy pawn
    """
    def __init__(self):
        super(EarlyStrat, self).__init__()

    def moves(self, start):
        """
        Returns list of first values in list of tuples created in potentialEarlyMoves
        :param start: starting tile
        :return: a list of tile ids that are possible move locations
        """
        return [move[0] for move in self.potentialEarlyMoves(start)]

    def potentialEarlyMoves(self, start):
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

    def potentialPushes(enemy):
        """
        Determine which of the enemy's neighboring tiles is the best tile to push using void edge
        heuristic where the tile with the most void edges in the neighbor tiles is the ideal push
        :param enemy: the enemy tile location
        :return: a sorted list of the neighboring tiles in descending order of void edges
        """
        voidEdgeList = [(tile, getVoidEdges(tile)) for tile in self.board.neighbor_tiles(enemy)]
        voidEdgeListSorted = sorted(voidEdgeList, key = lambda x: x[1])

        return voidEdgeListSorted

    def getVoidEdges(tile):
        """
        Determine the number of void edges of a given tile
        :param tile: a tile on the Board
        :return: an integer representing the number of pushed out spaces within the
        neighbors of tile
        """
        return 8 - len(neighbor_tiles(tile))
