import numpy as np
class QueueList(list):
    def enqueue(self, item):
        self.append(item)
    def dequeue(self):
        return self.pop(0)
    def find_optimal(self):
        idx = 1
        for i in range(2, len(self)):
            if self[i]-self[0] < self[idx]-self[0]:
                idx = i
        return idx
class Sys:
    def __init__(self):
        self.players = []
        self.queue = QueueList()
    def add_player(self,score):
        self.players.append(Player(score))
    def add_queue(self):
        for player in self.players:
            self.queue.enqueue(player)
class Player:
    def __init__(self, score):
        tmp=np.random.normal()
        self.init_score = score
        self.score = score
        self.time = 0