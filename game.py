import random
import math

class QueueList(list):
    """
    class for List + Queue
    """
    def enqueue(self, item):
        self.append(item)

    def dequeue(self):
        return self.pop(0)
    
    ''' 
    def find_optimal(self):
        idx = 1
        for i in range(2, len(self)):
            if abs(self[i].score-self[0].score) < abs(self[idx].score-self[0].score):
                idx = i
        return idx
    '''


class GameSys:
    """
    Class of game system
    """
    def __init__(self, matching_algorithm):
        self.find_optimal = matching_algorithm
        self.players = []
        self.queue = QueueList()
        self.system_time = 0
        self.system_log = []
        self.match_log = []

    def add_player(self,score):
        self.players.append(Player(score,len(self.players)))
    
    def add_queue(self):
        self.system_time += 1
        for player in self.players:
            if player.is_available(self):
                self.queue.enqueue(player)
                msg = f"Player ID {player.id} added to queue at system time {self.system_time}"
                self.add_to_log(msg)
                player.update_enqueued_time(self.system_time)

    def match(self):
        while len(self.queue) > 2:
            idx = self.find_optimal(self.queue)
            if idx == -1:
                return
            player2 = self.queue[idx]
            del self.queue[idx]
            player1 = self.queue.dequeue()
            msg = f"Matched Player ID {player1.id} and Player ID {player2.id} (differ: {abs(player1.score-player2.score)}) at system time {self.system_time}"
            self.add_to_log(msg)
            p1_time_waited = self.system_time-player1.get_enqueued_time()
            p2_time_waited = self.system_time-player2.get_enqueued_time()
            self.add_match_log(abs(player1.score-player2.score), p1_time_waited, p2_time_waited)
            do_match((player1, player2))

    def get_time(self):
        return self.system_time
    
    def is_in_queue(self, player):
        return player in self.queue
    
    def add_to_log(self, logdata):
        self.system_log.append(logdata)

    def save_log(self, filename='game_log'):
        filename += '.log'
        with open(filename, 'w') as f:
            for log in self.system_log:
                f.write(log + '\n')
    def add_match_log(self, differ:int, times_waited_p1,times_waited_p2):
        self.match_log.append((differ, times_waited_p1, times_waited_p2))


class Player:
    """
    Save player data
    """
    def __init__(self, score, id):
        self.init_score = score
        self.score = score
        self.time = 0
        self.stt_time = random.randint(1, 24)
        self.end_time = random.randint(1, 24)
        self.id = id
        self.enqueued_time = 30

    def __str__(self):
        data = 'Initial score: ' + str(self.init_score) + ', Current score: ' + str(int(self.score)) + \
            ', Played time: ' + str(self.time)
        return data
    
    def is_available(self, game):
        system_time = game.get_time()
        return not game.is_in_queue(self) and self.in_time(system_time)
    
    def in_time(self,system_time):
        res = (self.stt_time <= system_time <= self.end_time
                or self.stt_time > self.end_time >= system_time
                or self.end_time < self.stt_time <= system_time <= 24)
        return res
    
    def get_score(self):
        return self.score
    
    def add_score(self, score):
        self.score += score
    
    def add_played_time(self):
        self.time += 1
    def update_enqueued_time(self,t):
        self.enqueued_time = t
    def get_enqueued_time(self):
        return self.enqueued_time
    """
    class SimTime():
        def __init__(self):
            self.hour = 0
            self.minute = 0
    """

def do_match(players:tuple):
    """
    Input: Tuple(Player, Player), Sys
    """
    p1, p2 = players
    #승률 계산
    prob1 = 1 / (1 + 10 ** ((p2.get_score() - p1.get_score()) / 400))
    prob2 = 1 - prob1
    # Update the Elo ratings
    if p1.time > 10: # If player1 has played more than 10 games, k1 = 32, else k1 = 64
        k1 = 32
    else:
        k1 = 64
    if p2.time > 10: # If player2 has played more than 10 games, k2 = 32, else k2 = 64
        k2 = 32
    else:
        k2 = 64

    if random.random() < prob1:
        # Player1 wins
        p1.add_score(k1 * (1 - prob1))
        p2.add_score(k2 * (0 - prob2))
    else:
        # Player2 wins
        p1.add_score(k1 * (0 - prob1))
        p2.add_score(k2 * (1 - prob2))
    # Update the time
    p1.add_played_time()
    p2.add_played_time()
    
def export_csv(lst, filename='output'):
    filename += '.csv'
    with open(filename, 'w') as f:
        f.write('ID,Initial Score,Current Score,Played Time,PlayingTimeStart,PlayingTimeEnd\n')
        for item in lst:
            f.write("%d,%d,%d,%d,%d,%d\n" % (item.id, item.init_score, item.score, item.time, item.stt_time, item.end_time))

def match_time(player1, player2):
    """
    Calculate the match time (in minutes) based on the score difference.
    """
    score_def = abs(player1.get_score()-player2.get_score())
    log_data = math.log10(5*score_def+1)
    match_time = 45-10*(log_data)
    return int(match_time)
