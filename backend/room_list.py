import threading


class RoomList:
    room_list = []
    mutex = threading.Lock()

    def add_room(self, room):
        self.mutex.acquire()
        self.room_list.append(room)
        self.mutex.release()

    def remove_room(self):
        self.mutex.acquire()
        self.room_list.pop(len(self.room_list) - 1)
        self.mutex.release()

    def length(self):
        return len(self.room_list)

    def get_room(self, room_id):
        for room in self.room_list:
            if room_id == room.room_id:
                return room
        return None


roomList = RoomList()
