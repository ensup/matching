import game
import random
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
    while True:
        idx = 1
        if len(queue) > 2:
            for i in range(2, len(queue)):
                if abs(queue[i].score-queue[0].score) < abs(queue[idx].score-queue[0].score):
                    idx = i
            if(abs(queue[idx].score-queue[0].score) < 100):
                return idx
            else:
                queue.dequeue()
        else:
            return -1
def find_optimal_3(queue:List[game.Player]):
    """
    Randomly select the player to match with the first player in the queue
    """
    idx = random.randint(1, len(queue) - 1)
    return idx

def avg_waiting_time(system_log:List[tuple]):
    """
    Calculate the average waiting time of players in the queue
    """
    #name = "avg_waiting_time"
    print(system_log)
    print(len(system_log))
    waiting_time = 0
    for log in system_log:
        waiting_time += log[1] + log[2]
    if len(system_log) == 0:
        return None
    else:
        return waiting_time/(len(system_log)*2)

def max_waiting_time(system_log:List[tuple]):
    """
    Calculate the maximum waiting time of players in the queue
    """
    #name = "max_waiting_time"
    max_waiting_time = 0
    for log in system_log:
        max_waiting_time = max(max_waiting_time, log[1], log[2])
    return max_waiting_time

def avg_score_gap(system_log:List[tuple]):
    """
    Calculate the maximum score gap between matched players
    """
    #name = "avg_score_gap"
    max_gap = 0
    max_gap = sum([log[0] for log in system_log])
    return max_gap/len(system_log)

def max_score_gap(system_log:List[tuple]):
    """
    Calculate the maximum score gap between matched players
    """
    #name = "max_score_gap"
    max_gap = 0
    for slog in system_log:
        max_gap = max(max_gap, slog[0])
    return max_gap
    
def run_simulation(player_num:int, 
        matching_algorithm:Callable, 
        criterion:tuple[Callable],  
    ):
    """
    
    """
    lol = game.GameSys(matching_algorithm)
    # player_num = 15000
    random_numbers = random_numbers = [random.gauss(1500, 500) for _ in range(player_num)]
    for score in random_numbers:
        lol.add_player(int(score))
    for _ in range(24):
        lol.add_queue()
        lol.match()
    lol.save_log(matching_algorithm.__name__)
    game.export_csv(lol.players, matching_algorithm.__name__)
    #print(lol.match_log)
    score = {}
    for criteria in criterion:
        score[criteria] = criteria(lol.match_log)

    return score
if __name__ == '__main__':
    matching_algorithms = (find_optimal_1, find_optimal_2, find_optimal_3)
    criterion = [avg_waiting_time, max_waiting_time, avg_score_gap, max_score_gap]
    for matching_algorithm in matching_algorithms:
        res = run_simulation(15000, matching_algorithm, criterion)
        with open(f"{matching_algorithm.__name__}_result.txt", "w") as f:
            f.write(f"Matching Algorithm: {matching_algorithm.__name__}\n")
            for key, value in res.items():
                f.write(f"  {key.__name__}: {value}\n")
            
    print("Simulation completed")
    