import threading
from datetime import datetime
import air_conditioner_system.settings as st
# from backend.serializers import RoomStatusUpdateSerializer


class TaskQueue:
    queue = []
    mutex = threading.Lock()

    def push(self, request):
        self.mutex.acquire()
        for x in self.queue:
            if x[0].initial_data["room_id"] == request.initial_data['room_id']:
                self.queue.remove(x)
                break
        self.queue.append((request, datetime.now()))
        self.queue = sorted(self.queue, key=lambda x: (-st.PRIORITY[x[0].initial_data["ac_status"]], x[1]))
        self.mutex.release()

    def front(self):
        return self.queue[0][0]

    def pop(self):
        self.mutex.acquire()
        self.queue.pop(0)
        self.mutex.release()

    def length(self):
        return len(self.queue)

    def remove(self, room_id):
        for i in self.queue:
            if i[0].initial_data["room_id"] == room_id:
                self.queue.remove(i)
                return

    def __str__(self):
        string = '[\n'
        for i in self.queue:
            string += str(i[0].initial_data['room_id']) + ' ' + i[0].initial_data['ac_status'] + ' ' + str(i[1]) + '\n'

        string += ']'
        return string

taskQueue = TaskQueue()