import game
import numpy as np
from typing import List, Callable

def find_optimal_1(queue:List[game.Player]):
    """
    Find the optimal player to match with the first player in the queue
    """
    idx = 1
    for i in range(2, len(queue)):
        if abs(queue[i].score-queue[0].score) < abs(queue[idx].score-queue[0].score):
            idx = i
    return idx

def find_optimal_2(queue:List[game.Player]):
    """
    Find the optimal player to match with the first player in the queue
    If the difference between the first player and the optimal player is more than 100, delay the matching
    """
    idx = 1
    while True:
        for i in range(2, len(queue)):
            if abs(queue[i].score-queue[0].score) > abs(queue[idx].score-queue[0].score):
                idx = i
        if(abs(queue[idx].score-queue[0].score) < 100):
            break
        else:
            tmp = queue.dequeue()
            queue.enqueue(tmp)
    return idx
def find_optimal_3(queue:List[game.Player]):
    """
    Randomly select the player to match with the first player in the queue
    """
    idx = np.random.randint(1, len(queue))
    return idx

def run_simulation(player_num:int, 
        matching_algorithm:Callable, 
        criterion:list[Callable],  
    ):
    """
    
    """
    lol = game.GameSys(matching_algorithm)
    # player_num = 15000
    random_numbers = np.random.normal(loc=1500, scale=500, size=player_num)
    for score in random_numbers:
        lol.add_player(int(score))
    for _ in range(24):
        lol.add_queue()
        lol.match()
    game.export_csv(lol.players)
    lol.save_log()
    score = {}
    
    for criteria in criterion:
        score[criteria] = criteria(lol.system_log)

    return score
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
    lol.save_log()
