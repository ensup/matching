import game
import numpy as np
if __name__ == '__main__':
    lol = game.Sys()
    player_num = 15
    random_numbers = np.random.normal(loc=1500, scale=500, size=player_num)
    for score in random_numbers:
        lol.add_player(int(score))
    for player in lol.players:
        lol.queue.enqueue(player)
    for _ in range(20):
        lol.match()
    for player in lol.players:
        print(player)
    game.export_txt(lol.players)
    game.export_csv(lol.players)