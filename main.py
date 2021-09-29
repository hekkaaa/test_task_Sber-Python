import json
import datetime
from operator import itemgetter


# функция для print
def filter(i, direction):
    res_from = res[i][direction].split(' ')
    if (len(res_from[-1]) == 16):

        number = res_from.pop()
        number = f"{number[0:4]} {number[4:6]}** **** {number[12:16]}"
        res_from = " ".join(res_from)
        return res_from, number

    else:
        number = res_from.pop()
        number = f"**{number[16:20]}"
        res_from = " ".join(res_from)
        return res_from, number


# читаем файл json. utf решает проблему кодировки.
with open("operations.json", "r", encoding='utf-8') as info_json:
    data = json.load(info_json)

data_new = []
# Меняем формат даты для дальнейшей сортировки.
for i in range(len(data)):
    try:
        res = data[i]['date']
        res = res.replace("T", " ")
        date_time_obj = datetime.datetime.strptime(res, '%Y-%m-%d %H:%M:%S.%f')
        res = date_time_obj.date()
        data[i]['date'] = res

        # пересохраняем в связи с багом sorted для файлов открытых через utf-8
        data_new.append(data[i])

    except:
        continue

# Сортировка по дате и времени. Часы оставил для большей точности.
res = sorted(data_new, key=itemgetter('date'), reverse=True)

# Вывод информации в консоль
for i in range(5):
    try:
        from_res = filter(i, 'from')
        to_res = filter(i, 'to')

        print(f"{res[i]['date'].strftime('%d.%m.%Y')} {res[i]['description']}\n"
              f"{from_res[0]} {from_res[1]} -> {to_res[0]} {to_res[1]}\n"
              f"{res[i]['operationAmount']['amount']} {res[i]['operationAmount']['currency']['name']}\n")

    # Если нет from
    except:
        to_res = filter(i, 'to')
        print(f"{res[i]['date'].strftime('%d.%m.%Y')} {res[i]['description']}\n"
              f"{to_res[0]} {to_res[1]}\n"
              f"{res[i]['operationAmount']['amount']} {res[i]['operationAmount']['currency']['name']}\n")
