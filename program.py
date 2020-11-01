import csv
from _csv import reader
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import function

t = 21  # минуты с начала дня
M = 22  # мощность кВ
T = 23  # время в HH:mm

# скачки буду сохранять в файле с номером скачка и значениями времени

file = open("date.csv", encoding='utf-8')
file_reader = csv.reader(file, delimiter=";")
row21 = []  # время в минутах
row22 = []  # мощность в кВт

# samples = [1440]
peaks = dict()

for row in file_reader:
    if row[t].isdigit():
        row21.append(row[t])
        row22.append(float(row[M].replace(',', '.')))
        # samples.append(float(row[M].replace(',','.')))

# plt.style.use('fivethirtyeight')
x_vals = []
y_vals = []
mass_up = []
mass_up_name = []
up_name_count = 1
mass_low = []

k_up_check = 0  # подозрение на повышение
k_low_check = 0  # подозрение на понижение
k_up = 0  # повышение произошло
k_low = 0  # понижение произошло

index = count()  # счетчик для Х
it_arr = -1  # счетчик для массива, по которому проверяем изменения
arr = []  # массив для хранения предыдущих значений
kf = 1.17  # коэффициент изменения
normal = 0
normal_new = 0

last_peak = ''


def animate(i):
    global k_up_check, peak_comparator
    global k_low_check
    global k_up
    global k_low
    global arr
    global it_arr
    global peaks
    global last_peak
    global normal
    global mass_up
    global mass_up_name
    global up_name_count
    global mass_low
    it = next(index)  # берем следующее значение для прямой Х
    it_arr += 1
    #
    # если все переменные равны 0, то проверяем данные
    #
    if (k_low + k_up + k_up_check + k_low_check) == 0:

        # список не пустой и нынешнее значение больше предыдущего
        if len(arr) != 0 and row22[it] > arr[it_arr - 1]:
            if row22[it] > arr[it_arr - 1] * kf:
                k_up_check = arr[it_arr - 1]  # присваиваем индекс старой нормы
                normal = it_arr - 1
                last_peak = it

                print('Изменение напряжения!' + ' значение: ' + str(row22[it]) + ' индекс в массиве: ' + str(it))

            # print('Стало больше')
            arr.append(row22[it])
        # список не пустой и нынешнее значение меньше предыдущего
        elif len(arr) != 0 and row22[it] < arr[it_arr - 1]:
            if row22[it] * kf < arr[it_arr - 1]:
                k_low_check = arr[it_arr - 1]  # присваиваем индекс старой нормы
                normal = it_arr - 1
                # print('ПАДЕНИЕ!')
            # print('Стало меньше')
            arr.append(row22[it])

        # список не пустой и значение осталось прежним
        elif len(arr) != 0 and row22[it] == arr[it_arr - 1]:
            # print('Равно')
            arr.append(row22[it])
        # список пустой
        else:
            arr.append(row22[it])
            # print('Пусто')

    #
    # если подозрение на повышение или есть повышение
    #
    elif k_up_check != 0 or k_up != 0:
        # если еще не подтвердили
        if k_up == 0:
            if k_up_check != 0:
                if row22[it] > k_up_check * kf:
                    k_up = 1
                    # print('Снова больше')
                    # print('Подтверждение скачка')
                    arr.append(row22[it])
                else:
                    k_up_check = 0
                    # print('Вернулось к норме')
                    arr.append(row22[it])
        # если подтвердили
        else:
            # если в норме от предыдущего
            if arr[it_arr - 1] * kf > row22[it] > arr[it_arr - 1] * (2 - kf):
                m = []
                while normal != len(arr):
                    m.append(arr[normal])
                    normal += 1
                m.append(row22[it])
                # print(m)
                mass_up.append(m)
                arr = [row22[it]]  # обновляем массив

                counter = 0
                max_equal = 0
                equal_name = ''
                if len(mass_up) > 1:
                    for i in range(len(mass_up)):
                        if i != (len(mass_up) - 1):
                            if len(mass_up[i]) == len(mass_up[-1]) or \
                                    (len(mass_up[i]) - len(mass_up[-1])) == 1 or \
                                    (len(mass_up[i]) - len(mass_up[-1])) == -1:
                                r = function.func_kor(mass_up[i], mass_up[-1])
                                if r > 0.95:
                                    counter += 1
                                    if max_equal < r:
                                        max_equal = r
                                        equal_name = mass_up_name[i]

                if counter != 0:
                    print('Был подключен объект. Переходный процесс схож с объектом ' + equal_name)
                    mass_up_name.append(equal_name)
                else:
                    mass_up_name.append('a' + str(up_name_count))
                    up_name_count += 1
                    print('Был включен новый объект. Зададим код объекта ' + mass_up_name[-1])

                # print('Новая норма')
                normal = 0
                k_up = 0
                k_up_check = 0
                it_arr = 0

                print('Длительность пика: ' + str(it - last_peak) + ". C " + str(last_peak) + ' сек до ' + str(it))
                current_peak_name = 'Peak-' + str(last_peak)
                peaks[current_peak_name] = str(last_peak) + '-' + str(it)
                print(peaks)

                print('Peak time:')
                for i in range(last_peak, it):
                    print(str(i) + ': ' + str(row22[i]))

                # сравнение пиков
                if (len(peaks) != 0):
                    for key in dict.keys(peaks):
                        if (key != current_peak_name):
                            current_peak_duration = it - last_peak
                            peak_duration = peaks[key]
                            peak_start_time = int(peak_duration.split('-')[0])
                            peak_end_time = int(peak_duration.split('-')[1])
                            if (current_peak_duration == peak_end_time - peak_start_time):

                                peak_comparator = 0
                                for i in range(0, current_peak_duration):
                                    if (row22[peak_start_time + i] * kf > row22[it + i] > row22[peak_start_time + i] * (
                                            2 - kf)):
                                        peak_comparator += 1
                            # print (str(peak_comparator))
                            if (peak_comparator == current_peak_duration):
                                print('Peak: ' + key + ' and ' + current_peak_name + ' is equal')

            # если колебание относительно предыдущего
            else:
                arr.append(row22[it])
                k_up += 1



    #
    # если подозрение на понижение или есть понижение
    #
    elif k_low_check != 0 or k_low != 0:
        # если еще не подтвердили
        if k_low == 0:
            if k_low_check != 0:
                if arr[it_arr - 2] * kf > row22[it]:
                    k_low = 1
                    # print('Снова меньше')
                    arr.append(row22[it])
                else:
                    k_low_check = 0
                    # print('Вернулось к норме')
                    arr.append(row22[it])
        # если подтвердили
        else:
            # если в норме от предыдущего
            if arr[it_arr - 1] * kf > row22[it] > arr[it_arr - 1] * (2 - kf):
                m = []
                while normal != len(arr):
                    m.append(arr[normal])
                    normal += 1
                m.append(row22[it])
                # print(m)
                mass_low.append(m)
                arr = [row22[it]]  # обновляем массив
                x = [1, 2, 3, 4]
                x1 = [2, 3, 4, 5]
                y = m

                # print('Новая норма')
                normal = 0
                k_low = 0
                k_low_check = 0
                it_arr = 0
            else:
                arr.append(row22[it])
                k_low += 1

    x_vals.append(row21[it])
    y_vals.append(row22[it])
    plt.cla()
    plt.plot(x_vals, y_vals)
    plt.ylabel('power (kW)')
    plt.xlabel('time (min)')
    plt.grid()


ani = FuncAnimation(plt.gcf(), animate, interval=1)

plt.tight_layout()
plt.show()
