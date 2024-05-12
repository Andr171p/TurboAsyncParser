import datetime
from datetime import date


class DatetimeConverter:
    def __init__(self):
        self.DATES_dict = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12
        }

    # this function return float time from string:
    def str_to_time(self, time_string):
        time_datetime = datetime.datetime.strptime(time_string, "%H:%M").time()
        return round(float(time_datetime.hour) + float(time_datetime.minute) / 60, 2)

    # this function accept int: year, int: month, int: day and return datetime object
    def convert_to_datetime(self, year, month, day, time):
        date_string = f"{year}-{month}-{day} {int(time)}:{int((time - int(time)) * 60)}"
        date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M")
        return date_object

    # this function return date-time object from string pattern of avito:
    def current_date(self, date_string_pattern):
        # get date:
        date_pattern_list = date_string_pattern.split()
        date_of_day = date_pattern_list[1]
        time = date_pattern_list[-1]
        if date_of_day == "сегодня":
            # today date/time:
            today_date = date.today()
            year, month, day = today_date.year, today_date.month, today_date.day
            time_float = self.str_to_time(time)

            return self.convert_to_datetime(year, month, day, time_float)

        elif date_of_day == "вчера":
            # yesterday date/time:
            today_date = date.today()
            yesterday_date = today_date - datetime.timedelta(days=1)
            yesterday_date.strftime('%Y-%m-%d')
            year, month, day = yesterday_date.year, yesterday_date.month, yesterday_date.day
            # str --> time-object:
            time_float = self.str_to_time(time)

            return self.convert_to_datetime(year, month, day, time_float)

        else:
            # get today year:
            current_year = datetime.datetime.now().year
            # get date number and month:
            number = int(date_pattern_list[1])
            month = self.DATES_dict[date_pattern_list[2]]
            current_time = time.replace(':', '.')

            return self.convert_to_datetime(current_year, month, number, float(current_time))

