import random


class Hotel_rooms:
    '''
    Класс создает для каждого номера словарь, далее генерирует
    из этих словарей список и про помощи метода get_rooms возвращает его.
    '''
    def __init__(self, file=None):
        self._file = file
        with open(self._file) as file_room:
            lst_rooms = []
            for line in file_room.readlines():
                room = line.split()
                d = dict()
                d['номер номера'] = room[0].replace('\ufeff', '')
                d['тип номера'] = room[1]
                if room[1] == 'одноместный':
                    d['цена номера'] = 2900.0
                elif room[1] == 'двухместный':
                    d['цена номера'] = 2300.0
                elif room[1] == 'полулюкс':
                    d['цена номера'] = 3200.0
                elif room[1] == 'люкс':
                    d['цена номера'] = 4100.0
                d['максимальная вместимость номера'] = room[2]
                d['степень комфортности'] = room[3]
                if room[3] == 'стандарт_улучшенный':
                    d['цена номера'] *= 1.2
                elif room[3] == 'апартамент':
                    d['цена номера'] *= 1.5
                lst_rooms.append(d)
        self._lst_rooms = lst_rooms

    def __str__(self):
        string = ''
        for item in self._lst_rooms:
            string += item['номер номера'] + ' ' + \
                      item['тип номера'] + ' ' + \
                      str(item['максимальная вместимость номера']) + ' ' + \
                      item['степень комфортности'] + ' ' + str(item['цена номера']) + ' '
            string += '\n'
        return string

    def __repr__(self):
        return self.__str__()

    def get_rooms(self):
        return self._lst_rooms


class Choice(Hotel_rooms):
    '''
    Класс наследуется от класса "генератора списка комнат" и создает
    новый список из всех вариантов размещения номеров.
    '''
    def __init__(self, file=None):
        lst_choice = []
        super().__init__(file)
        for room in self._lst_rooms:
            for num in range(3):
                if num == 0:
                    a = room.copy()
                    a['питание'] = 'без питания'
                    lst_choice.append(a)

                elif num == 1:
                    b = room.copy()
                    b['питание'] = 'завтрак'
                    b['цена номера'] = b['цена номера'] + 280
                    lst_choice.append(b)

                elif num == 2:
                    c = room.copy()
                    c['питание'] = 'полупансион'
                    c['цена номера'] = c['цена номера'] + 1000
                    lst_choice.append(c)
        self._lst_choice = lst_choice

    def __str__(self):
        return 'Пока пусто'

    def __repr__(self):
        return self.__str__()

    def get_choice(self):
        return self._lst_choice


class Accommodation_option(Choice):
    '''
    Основной класс.
    Наследуется от класса, который создает всевозможные варианты размещения клиента,
    подбирает номер для клиента и определяет бронирование.
    '''
    def __init__(self, file_rooms, file_clients):
        super().__init__(file_rooms)
        self.final_group = []

        self._file_clients = file_clients
        with open(self._file_clients) as file_clients:
            lst_clients = []
            for line in file_clients:
                client = line.split()
                setting = dict()
                setting['дата бронирования'] = client[0].replace('\ufeff', '')
                setting['имя клиента'] = client[1] + ' ' + client[2] + ' ' + client[3]
                setting['количество человек'] = client[4]
                setting['дата въезда'] = client[5]
                setting['количество суток'] = client[6]
                setting['сумма'] = client[7]
                lst_clients.append(setting)
        self._lst_clients = lst_clients

    def get_clients(self):
        return self._lst_clients

    @staticmethod
    def minimum_of_list_price(lst, price):
        lst_delta = []
        for item in lst:
            delta = int(price) - int(item['цена номера'])
            if delta >= 0:
                lst_delta.append(int(price) - int(item['цена номера']))
        item = lst_delta[0]
        for num in lst_delta:
            b = int(num)
            if b < item:
                item = b
        ind = lst_delta.index(item)
        return lst[ind]

    def __busting_rooms(self, client, dates, lst):
        list_candidates = []
        places_1, places_2, places_3, places_5, places_6 = [], [], [], [], []
        list_dates_client = set()

        for day in range(int(client['количество суток'])):
            list_dates_client.add(str(int(client['дата въезда'][:2]) + day) + client['дата въезда'][2:])

        for var in self.get_choice():
            if var['максимальная вместимость номера'] >= client['количество человек']:
                if dates[var['номер номера']] & list_dates_client == set():

                    if var['цена номера'] <= int(client['сумма']):
                        list_candidates.append(var)

        for room in list_candidates:
            if room['максимальная вместимость номера'] == '1':
                places_1.append(room)
            elif room['максимальная вместимость номера'] == '2':
                places_2.append(room)
            elif room['максимальная вместимость номера'] == '3':
                places_3.append(room)
            elif room['максимальная вместимость номера'] == '5':
                places_5.append(room)
            elif room['максимальная вместимость номера'] == '6':
                places_6.append(room)

        for i in [places_1, places_2, places_3, places_5, places_6]:
            if i:
                fin_room = self.minimum_of_list_price(i, client['сумма'])
                for date in list_dates_client:
                    dates[fin_room['номер номера']].add(date)
                lst.append((fin_room['тип номера'], list(list_dates_client)))
                return fin_room

        if places_1 == [] and places_2 == [] and places_3 == [] and places_5 == [] and places_6 == []:
            return 'БЕДНЯГА'

    def options(self):
        room_card = {'одноместный': 9, 'двухместный': 6, 'полулюкс': 5, 'люкс':4}
        count = {'одноместный': 0, 'двухместный': 0, 'полулюкс': 0, 'люкс': 0,
                 'Процент загруженности гостиницы': 0, 'Доход за день': 0, 'Упущенный доход': 0}
        dict_of_date = {}
        list_of_date = []
        for num in self.get_rooms():
            dict_of_date[num['номер номера']] = set()
        for client in self._lst_clients:
            Yes_No = random.randint(0, 100)
            for key in dict_of_date:
                if str(int(client['дата бронирования'][:2]) - 1) + client['дата бронирования'][2:] in dict_of_date[key]:
                    dict_of_date[key].remove(str(int(client['дата бронирования'][:2]) - 1) + client['дата бронирования'][2:])

            fin = self.__busting_rooms(client, dict_of_date, list_of_date)

            for i in list_of_date:
                if str(int(client['дата бронирования'][:2]) - 1) + client['дата бронирования'][2:] in i[1]:
                    i[1].remove(str(int(client['дата бронирования'][:2]) - 1) + client['дата бронирования'][2:])
                if i[1] == [] and i[0] == 'одноместный':
                    count['одноместный'] -= 0
                    list_of_date.remove(i)

            if fin != 'БЕДНЯГА':
                if Yes_No in range(26, 101):
                    if count[fin['тип номера']] < room_card[fin['тип номера']]:
                        self.final_group.append([client, fin, 'Клиент согласен. Номер забронирован.'])
                        count['Доход за день'] += int(fin['цена номера']) * int(client['количество человек'])
                        sms = 'тип номера'
                        if fin[sms] == 'одноместный':
                            if dict_of_date[fin['номер номера']] == set():
                                count['одноместный'] += 0
                            else:
                                count['одноместный'] += 1
                        elif fin[sms] == 'двухместный':
                            if dict_of_date[fin['номер номера']] == set():
                                count['двухместный'] += 0
                            else:
                                count['двухместный'] += 1
                        elif fin[sms] == 'полулюкс':
                            if dict_of_date[fin['номер номера']] == set():
                                count['полулюкс'] += 0
                            else:
                                count['полулюкс'] += 1
                        elif fin[sms] == 'люкс':
                            if dict_of_date[fin['номер номера']] == set():
                                count['люкс'] += 0
                            else:
                                count['люкс'] += 1
                    else:
                        self.final_group.append([client, fin, 'Клиент согласен. Номер забронирован.'])
                else:
                    self.final_group.append([client, fin, 'Клиент отказался от варианта.'])
            else:
                self.final_group.append([client, fin, 'Предложений по данному запросу нет. В бронировании отказано.'])
        return self.final_group

    def __str__(self):
        string = ''
        for item in self.options():
            if item[1] != 'БЕДНЯГА':
                string += '------------------------------------------------------------------------------------' + \
                          '\n' + '\nПоступила заявка на бронирование:' + '\n' * 2 + \
                          str(item[0]['дата бронирования']) + ' ' + str(item[0]['имя клиента']) + \
                          ', количество человек: ' + str(item[0]['количество человек']) + \
                          ', дата въезда: ' + str(item[0]['дата въезда']) + ', на сколько: ' + \
                          str(item[0]['количество суток']) + ', сумма: ' + str(item[0]['сумма']) + \
                          '\n' * 2 + 'Найден:\n' + 'Номер ' + str(int(item[1]['номер номера'])) +\
                            ' ' + str(item[1]['тип номера']) + ' ' + str(item[1]['степень комфортности']) + \
                            ' расситан на ' + str(item[1]['максимальная вместимость номера']) + ' чел.' + \
                          ' фактически ' + str(item[0]['количество человек']) + ' ' + str(item[1]['питание']) +\
                          ' стоимость '

                if item[0]['количество человек'] == item[1]['максимальная вместимость номера']:
                    string += str(round(int(item[1]['цена номера']) * int(item[0]['количество человек']))) + \
                              '.00 руб./сутки\n\n'
                elif item[0]['количество человек'] < item[1]['максимальная вместимость номера']:
                    string += str(round(int(item[1]['цена номера']) * int(item[0]['количество человек'])) * 0.7) +\
                              '.00 руб./сутки\n\n'

                if item[2] == 'Клиент согласен. Номер забронирован.':
                    string += item[2] + '\n\n'
                elif item[2] == 'Клиент отказался от варианта.':
                    string += item[2] + '\n\n'

            else:
                string += '------------------------------------------------------------------------------------' +\
                          '\n' + '\nПоступила заявка на бронирование:' + '\n' * 2 + \
                          str(item[0]['дата бронирования']) + ' ' + str(item[0]['имя клиента']) + \
                          ', количество человек: ' + str(item[0]['количество человек']) + \
                          ', дата въезда: ' + str(item[0]['дата въезда']) + ', на сколько: ' + \
                          str(item[0]['количество суток']) + ', сумма: ' + str(item[0]['сумма']) + '\n' * 2 +\
                          'Предложений по данному запросу нет. В бронировании отказано.\n\n'
        return string

    def __repr__(self):
        return self.__str__()

