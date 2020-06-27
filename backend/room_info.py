from .ac_settings import acSettings
from datetime import datetime
import threading
from .waiting_queue import waitingQueue
from .service_list import serviceList
from .pause_list import pauseList
from .models import CommonLog
from .controller import interval
from datetime import date, datetime


class Detail:
    def __init__(self, room_id, ac_status, temp, target_temp, elec):
        self.room_id = room_id
        self.ac_status = ac_status
        self.temp = temp
        self.target_temp = target_temp
        self.elec = elec
        self.total_money = round(elec * acSettings.power_price, 1)
        self.timestamp = datetime.now()


class RoomInfo:
    def __str__(self):
        return self.room_id

    def __init__(self, room_id, online_time=0, ac_status='off', temp=acSettings.default_temp,
                 target_temp=acSettings.default_temp, elec=0, money=0):
        self.mutex = threading.Lock()
        self.room_id = room_id
        self.ac_status = ac_status
        self.target_temp = target_temp
        self.elec = elec
        self.details = []
        self.online_time = online_time
        self.checked = False
        self.total_money = money
        self.checkin_time = None
        self.price = 0
        if self.room_id == 1:
            self.temp = 32.0
        elif self.room_id == 2:
            self.temp = 28.0
        elif self.room_id == 3:
            self.temp = 30.0
        elif self.room_id == 4:
            self.temp = 29.0
        elif self.room_id == 5:
            self.temp = 35.0
        else:
            self.temp = temp

    def same_mode(self, mode):
        return self.ac_status == mode

    def set(self, **settings):
        self.mutex.acquire()
        if 'checked' in settings:
            self.checked = settings['checked']
        if 'ac_status' in settings:
            if settings['ac_status'] != self.ac_status and settings['ac_status'] != 'off':
                obj, _ = CommonLog.objects.get_or_create(
                    room_id=self.room_id,
                    date=date.today()
                )
                obj.change_wind_times += 1
                obj.save()
            self.ac_status = settings['ac_status']
            self.price = acSettings.power_price * acSettings.wind_power[self.ac_status]
        if 'temp' in settings:
            self.temp = float(settings['temp'])
        if 'target_temp' in settings:
            if settings['target_temp'] != self.target_temp:
                obj, _ = CommonLog.objects.get_or_create(
                    room_id=self.room_id,
                    date=date.today()
                )
                obj.change_temp_times += 1
                obj.save()
            self.target_temp = float(settings['target_temp'])
        if 'money' in settings:
            self.total_money = settings['money']
        if 'elec' in settings:
            self.elec = settings['elec']
        if 'online_time' in settings:
            self.online_time = settings['online_time']
        if 'checkin_time' in settings:
            self.checkin_time = settings['checkin_time']
        if 'price' in settings:
            self.price = settings['price']
        self.mutex.release()

    def check_in(self):
        self.mutex.acquire()
        self.checked = True
        self.checkin_time = datetime.now()
        self.mutex.release()

    def check_out(self):
        if serviceList.look_up(self.room_id):
            serviceList.remove(self.room_id)
        if waitingQueue.look_up(self.room_id):
            waitingQueue.remove(self.room_id)
        if pauseList.look_up(self.room_id):
            pauseList.remove(self.room_id)
        target = 0
        if self.room_id == 1:
            target = 32.0
        elif self.room_id == 2:
            target = 28.0
        elif self.room_id == 3:
            target = 30.0
        elif self.room_id == 4:
            target = 29.0
        elif self.room_id == 5:
            target = 35.0
        else:
            target = acSettings.default_temp
        self.set(
            checked=False,
            ac_status='off',
            target_temp=target,
            elec=0,
            online_time=0,
            money=0,
            checkin_time=None,
            price=0,
        )


    def is_checked(self):
        return self.checked

    def add_detail(self):
        self.mutex.acquire()
        detail = Detail(
            room_id=self.room_id,
            ac_status=self.ac_status,
            temp=self.temp,
            target_temp=self.target_temp,
            elec=self.elec
        )
        self.details.append(detail)
        obj, _ = CommonLog.objects.get_or_create(
            room_id=self.room_id,
            date=date.today()
        )
        obj.detail_num += 1
        obj.save()
        self.mutex.release()

    def get_details(self):
        return self.details

    def update_elec(self):
        # if len(self.details) > 0:
        #     last_detail = self.details[len(self.details) - 1]
        #     self.elec = last_detail.elec + self.online_time * acSettings.wind_power[self.ac_status]
        # else:
        #     self.elec = self.online_time * acSettings.wind_power[self.ac_status]
        # self.elec += interval * acSettings.wind_power[self.ac_status]
        self.elec += acSettings.wind_power[self.ac_status]
        self.elec = round(self.elec, 1)
        # print(self.elec)
        obj, _ = CommonLog.objects.get_or_create(
            room_id=self.room_id,
            date=date.today()
        )
        # obj.scheduled_times += self.online_time * acSettings.wind_power[self.ac_status]
        obj.total_money += round(acSettings.wind_power[self.ac_status] * acSettings.power_price, 1)
        obj.save()

    def update_money(self):
        self.total_money = round(self.elec * acSettings.power_price, 1)
