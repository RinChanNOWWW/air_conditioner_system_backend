import threading


class PauseList:
    pause_list = []
    mutex = threading.Lock()

    def __str__(self):
        s = '['
        for item in self.pause_list:
            s += '(' + str(item[0].room_id) + ',' + str(item[1]) + ')'
        s += ']'
        return s

    def append(self, room, mode):
        self.mutex.acquire()
        self.pause_list.append((room, mode))
        self.mutex.release()

    def look_up(self, room_id):
        for item in self.pause_list:
            if room_id == item[0].room_id:
                return True
        return False

    def remove(self, room_id):
        self.mutex.acquire()
        for item in self.pause_list:
            if room_id == item[0].room_id:
                self.pause_list.remove(item)
                self.mutex.release()
                return
        self.mutex.release()

    def length(self):
        return len(self.pause_list)


pauseList = PauseList()
