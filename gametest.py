import isolation
from randomplayer import RandomPlayer
import random
import aqua


def main():
    tokens = {'Red' : isolation.Board.RED_TOKEN, 'Blue' : isolation.Board.BLUE_TOKEN}
    exceptions = []
    scores = {"aqua" : 0, "random" : 0}
    for i in range(10):
        us = random.choice(list(tokens.keys()))
        them = 'Red' if us == 'Blue' else 'Blue'

        try:
            if us == 'Red':
                isolation.Board.set_dimensions(6, 8)
                our_player = aqua.Aqua('Red', isolation.Board.RED_TOKEN)
                match = isolation.Match(RandomPlayer('Blue', isolation.Board.BLUE_TOKEN),
                                        our_player,
                                        isolation.Board())
            else:
                isolation.Board.set_dimensions(6, 8)
                our_player = aqua.Aqua('Blue', isolation.Board.BLUE_TOKEN)
                match = isolation.Match(our_player,
                                        RandomPlayer('Red', isolation.Board.RED_TOKEN),
                                        isolation.Board())

            match.start_play()

            if match.winner() == our_player:
                scores["aqua"] = scores["aqua"] + 1
            else:
                scores["random"] = scores["random"] + 1


        except Exception as e:
            exceptions.append(e)

    print("Aqua's Score: ", scores["aqua"])
    print("Enemy Score:  ", scores["random"])
    print("Error count:  ", len(exceptions))




if __name__ == '__main__':
    main()