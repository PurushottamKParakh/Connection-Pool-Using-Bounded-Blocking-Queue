from collections import deque
from threading import Condition


class BlockingQueue:

    def __init__(self, max_size):
        self.max_size = max_size
        self.curr_size = 0
        self.cond = Condition()
        self.q = deque()

    def deque(self):
        self.cond.acquire()
        while self.curr_size == 0:
            self.cond.wait()

        item = self.q.popleft()
        self.curr_size -= 1

        self.cond.notify_all()
        self.cond.release()

        return item

    def enque(self, item):
        self.cond.acquire()
        while self.curr_size == self.max_size:
            self.cond.wait()

        self.q.append(item)
        self.curr_size += 1
        self.cond.notify_all()
        self.cond.release()

    def empty(self):
        return self.curr_size == 0
