import threading
from datetime import datetime
from .ac_settings import priority


class WaitingQueue:
    waiting_queue = []
    mutex = threading.Lock()

    def push(self, request):
        self.mutex.acquire()
        # if self.look_up(request['room_id']):
        #     self.remove(request['room_id'])
        # self.waiting_queue.append((request, datetime.now()))
        self.waiting_queue.append([request, 0])
        self.waiting_queue = sorted(self.waiting_queue, key=lambda x: (-priority[x[0]['ac_status']], -x[1]))
        self.mutex.release()

    def front(self):
        return self.waiting_queue[0][0]

    def get_front_waited_time(self):
        return self.waiting_queue[0][1]

    def pop(self):
        self.mutex.acquire()
        self.waiting_queue.pop(0)
        self.mutex.release()

    def length(self):
        return len(self.waiting_queue)

    def look_up(self, room_id):
        for request in self.waiting_queue:
            if room_id == request[0]['room_id']:
                return True
        return False

    def remove(self, room_id):
        self.mutex.acquire()
        for request in self.waiting_queue:
            if request[0]['room_id'] == room_id:
                self.waiting_queue.remove(request)
                self.mutex.release()
                return
        self.mutex.release()


waitingQueue = WaitingQueue()
