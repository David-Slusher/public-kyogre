from isolation import *


class Aqua(Player):
    def __init__(self, name, token):
        super(Aqua, self).__init__(name, token)

    def take_turn(self, board):
        """
        Make a move on the Isolation board and push out space
        :param board: a Board object
        :return: a Move object
        """
        # Each subclass must implement this method
        raise NotImplementedError
        #make move
            #needs to move towards enemy pawn until it cant get closer


        # print("\n{} taking turn: ".format(self._name), end='')
        #
        # # Collect board state info to generate a move from
        # space_id = board.token_location(self._token)
        # neighbors = board.neighbor_tiles(space_id)
        # print('possible moves:', neighbors)
        # tiled_spaces = board.push_outable_square_ids()
        #
        # # Select a square to move to and a tile to push out.
        # # Once a neighbor square is chosen to move to,
        # # that square can no longer be pushed out, but
        # # the square vacated might be able to be pushed out
        # to_space_id = random.choice(list(neighbors))
        # tiled_spaces.discard(to_space_id)
        # # if space_id not in board.start_squares():
        # #     tiled_spaces.add(space_id)
        # tiled_spaces.add(space_id)
        # print('possible push outs:', tiled_spaces)
        # push_out_space_id = random.choice(list(tiled_spaces))
        #
        # # print('    Moving to', to_space_id, 'and pushing out', push_out_space_id)
        #
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
