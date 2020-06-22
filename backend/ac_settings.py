priority = {
    'off': 0,
    'low': 1,
    'medium': 2,
    'high': 3
}


class ACSettings:
    wind_power = {
        'off': 0,
        'low': 1,
        'medium': 2,
        'high': 3
    }
    power_price = 1
    max_serve_num = 3
    default_temp = 26.0
    mode = 'cold'
    temp_period = {
        'min': 18,
        'max': 26
    }
    room_num = 50

    def set_room_num(self, num):
        if num is not None:
            self.room_num = num

    def set_temp_period(self, period):
        if period['min'] is not None and period['max'] is not None:
            self.temp_period['min'] = period['min']
            self.temp_period['max'] = period['max']

    def set_mode(self, mode):
        if mode is not None:
            self.mode = mode

    def set_default_temp(self,temp):
        if temp is not None:
            self.default_temp = temp

    def set_max_serve_num(self, num):
        if num is not None:
            self.max_serve_num = num

    def set_power_price(self, price):
        if price is not None:
            self.power_price = price

    def set_wind_power(self, low=1, medium=2, high=3):
        if low is not None:
            self.wind_power['low'] = low
        if medium is not None:
            self.wind_power['medium'] = medium
        if high is not None:
            self.wind_power['high'] = high


acSettings = ACSettings()
