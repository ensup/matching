import random
class QueueList(list):
    """
    class for List + Queue
    """
    def enqueue(self, item):
        self.append(item)
    def dequeue(self):
        return self.pop(0)
    def find_optimal(self):
        idx = 1
        for i in range(2, len(self)):
            if abs(self[i].score-self[0].score) < abs(self[idx].score-self[0].score):
                idx = i
        return idx
class GameSys:
    """
    Class of game system
    """
    def __init__(self):
        self.players = []
        self.queue = QueueList()
        self.system_time = 0
        self.system_log = []
    def add_player(self,score):
        self.players.append(Player(score))
    def add_queue(self):
        self.system_time += 1
        for player in self.players:
            if player.is_available(self):
                self.queue.enqueue(player)
                msg = f"Player ID {self.players.index(player)} added to queue at system time {self.system_time}"
                self.add_to_log(msg)
    def match(self):
        while len(self.queue) > 2:
            idx = self.queue.find_optimal()
            player2 = self.queue[idx]
            del self.queue[idx]
            player1 = self.queue.dequeue()
            msg = f"Matched Player ID {self.players.index(player1)} and Player ID {self.players.index(player2)} at system time {self.system_time}"
            self.add_to_log(msg)
            do_match((player1, player2))
    def get_time(self):
        return self.system_time
    def is_in_queue(self, player):
        return player in self.queue
    def add_to_log(self, logdata):
        self.system_log.append(logdata)
    def save_log(self):
        with open('log.txt', 'w') as f:
            for log in self.system_log:
                f.write(log + '\n')

class Player:
    """
    Save player data
    """
    def __init__(self, score):
        self.init_score = score
        self.score = score
        self.time = 0
        self.stt_time = random.randint(1, 24)
        self.end_time = random.randint(1, 24)
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

def do_match(players:tuple):
    """
    Input: Tuple(Player, Player), Sys
    """
    p1, p2 = players
    #승률 계산
    prob1 = 1 / (1 + 10 ** ((p2.score - p1.score) / 400))
    prob2 = 1 - prob1
    # Update the Elo ratings
    k=32
    if random.random() < prob1:
        # Player1 wins
        p1.score += k * (1 - prob1)
        p2.score += k * (0 - prob2)
    else:
        # Player2 wins
        p1.score += k * (0 - prob1)
        p2.score += k * (1 - prob2)
    # Update the time
    p1.time += 1
    p2.time += 1
'''
def export_txt(list):
    with open('output.txt', 'w') as f:
        i=0
        for item in list:
            f.write("Player %d: %s\n" % (i, item))
            i+=1
'''
def export_csv(lst):
    with open('output.csv', 'w') as f:
        f.write('ID,Initial Score,Current Score,Played Time,PlayingTimeStart,PlayingTimeEnd\n')
        i=0
        for item in lst:
            f.write("%d,%d,%d,%d,%d,%d\n" % (i, item.init_score, item.score, item.time, item.stt_time, item.end_time))
            i+=1
