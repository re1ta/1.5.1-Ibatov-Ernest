import csv
import re
from datetime import datetime
from prettytable import PrettyTable

def get_dictionary(array):
    _dict = []
    for i in range(1,len(array)):
        _dict.append([])
        _dict[i-1] = dict(zip(array[0],array[i]))
    return _dict

def cut_chars(array, title):
    for i in range(0,len(array)):
        for line in title:
            if len(array[i][line]) > 100:
                array[i][line] = array[i][line][:100] + '...'
    return array

def trans_skills(array):
    for i in range(0, len(array)):
        array[i]["Навыки"] = array[i]["Навыки"].split(', ')
        array[i]["Навыки"] = '\n'.join(array[i]["Навыки"])
    return array

def format_cash(x):
    if int(x) <= 1000:
        return x
    else:
        return x[0:len(x) - 3] + ' ' + x[len(x) - 3:len(x)]


def сsv_reader(file_name):
    with open(file_name, "r", encoding='utf-8-sig', newline='') as csv_file:
        return list(csv.reader(csv_file, delimiter=","))


def csv_filer(reader):
    if len(reader) == 0:
        flag = False
        print('Пустой файл')
        return flag
    elif len(reader) == 1:
        flag = False
        print('Нет данных')
        return flag
    else:
        for item in reader[:]:
            if '' in item or len(item) != len(reader[0]): reader.remove(item)
            for i in range(0, len(item)):
                item[i] = re.sub("<.*?>", '', item[i])
                item[i] = item[i].strip()
                item[i] = item[i].replace("\r\n", ', ')
                item[i] = item[i].replace("\n", ', ')
                item[i] = re.sub(" +", ' ', item[i])
                item[i] = ' '.join(item[i].split())
        return reader

def formatter(data_vacancies, dic_naming):
    for item in data_vacancies[:]:
        for i in range(0, len(item)):
            if item[i] in dic_naming:
                item[i] = dic_naming[item[i]]

    data_vacancies[0] = data_vacancies[0][0:7] + data_vacancies[0][10:12]
    for i in range(1, len(data_vacancies)):
        dv6 = str(int(float(data_vacancies[i][6])))
        dv7 = str(int(float(data_vacancies[i][7])))
        if data_vacancies[i][8] == 'Да':
            data_vacancies[i][6] = format_cash(dv6) + ' - ' + format_cash(dv7) + ' ' + data_vacancies[i][
                9] + ' ' + '(Без вычета налогов)'
        else:
            data_vacancies[i][6] = format_cash(dv6) + ' - ' + format_cash(dv7) + ' ' + data_vacancies[i][
                9] + ' ' + '(С вычетом налогов)'

        data_vacancies[i] = data_vacancies[i][0:7] + data_vacancies[i][10:12]
        PATTERN_IN = "%Y-%m-%dT%H:%M:%S%z"
        PATTERN_OUT = "%d.%m.%Y"
        date = datetime.strptime(data_vacancies[i][8], PATTERN_IN)
        data_vacancies[i][8] = datetime.strftime(date, PATTERN_OUT)
    return data_vacancies

def print_vacancies(data_vacancies, dic_naming, limit, names):
    for i in range(0, len(data_vacancies[0])):
        if data_vacancies[0][i] in dic_naming:
            data_vacancies[0][i] = dic_naming[data_vacancies[0][i]]

    data_vacancies = formatter(data_vacancies, translate1)
    title = data_vacancies[0]
    data_vacancies = get_dictionary(data_vacancies)
    data_vacancies = trans_skills(data_vacancies)
    data_vacancies = cut_chars(data_vacancies,title)
    if len(limit) == 1: limit.append(len(data_vacancies)+1)
    elif len(limit) == 0:
        limit.append(1)
        limit.append(len(data_vacancies)+1)
    if len(names) == 0: names = list(title)
    filtered = []
    n = 1
    for i in range(0,len(data_vacancies)):
        filtered.append([])
        for name in title:
            filtered[i].append(data_vacancies[i][name])
        filtered[i].insert(0, n)
        n += 1
    title.insert(0, "№")
    names.insert(0, "№")
    mytable = PrettyTable(title)
    mytable.add_rows(filtered)
    mytable.hrules = True
    mytable.align = "l"
    mytable.max_width = 20
    print(mytable.get_string(start = int(limit[0])-1, end = int(limit[1])-1, fields = names))

translate = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки', 'experience_id': 'Опыт работы',
             'premium': 'Премиум-вакансия', 'employer_name': 'Компания', 'salary_from': 'Оклад',
             'salary_to': 'Верхняя граница вилки оклада', 'salary_gross': 'Оклад указан до вычета налогов',
             'salary_currency': 'Идентификатор валюты оклада', 'area_name': 'Название региона',
             'published_at': 'Дата публикации вакансии'}

translate1 = {"AZN": "(Манаты)", "BYR": "(Белорусские рубли)", "EUR": "(Евро)", "GEL": "(Грузинский лари)",
              "KGS": "(Киргизский сом)",
              "KZT": "(Тенге)", "RUR": "(Рубли)", "UAH": "(Гривны)", "USD": "(Доллары)", "UZS": "(Узбекский сум)",
              "noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет", "between3And6": "От 3 до 6 лет",
              "moreThan6": "Более 6 лет", "False": "Нет", "True": "Да"}
#  vacancies_medium.csv
text = input()
limit = input().split(' ')
if '' in limit: limit.remove('')
names = input().split(', ')
if '' in names: names.remove('')
reader = сsv_reader(text)
reader = csv_filer(reader)
if type(reader) == list:
    print_vacancies(reader, translate, limit, names)