import game
import numpy as np
if __name__ == '__main__':
    lol = game.GameSys()
    player_num = 15000
    random_numbers = np.random.normal(loc=1500, scale=500, size=player_num)
    for score in random_numbers:
        lol.add_player(int(score))
    for _ in range(24):
        lol.add_queue()
        lol.match()
    game.export_csv(lol.players)
