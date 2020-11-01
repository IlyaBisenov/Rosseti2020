'''
В данном файле хранятся функции для сравнения двух переходных процессов
Сравнение проводится при помощи корреляции
Функция func_kor возвращает значение коэффициента парной линейной корреляции
'''


def func_kor(x, y):
    if len(x) == len(y):
        return korr(x, y)
    elif len(x) > len(y):
        x1 = []
        x2 = []
        for i in range(len(x) - 1):
            x1.append(x[i])
            x2.append(x[i + 1])

        a = korr(x1, y)
        b = korr(x2, y)
        return max(a, b)
    else:
        y1 = []
        y2 = []
        for i in range(len(y) - 1):
            y1.append(y[i])
            y2.append(y[i + 1])

        a = korr(x, y1)
        b = korr(x, y2)
        return max(a, b)


def korr(x, y):
    sum_Xi = 0
    sum_Xi2 = 0
    sum_Yi = 0
    sum_Yi2 = 0
    sum_XiYi = 0

    for i in range(len(x)):
        sum_Xi += x[i]
        sum_Yi += y[i]
        sum_XiYi += x[i] * y[i]
        sum_Xi2 += x[i] * x[i]
        sum_Yi2 += y[i] * y[i]

    cisl = 4 * sum_XiYi - sum_Xi * sum_Yi
    znam = ((4 * sum_Xi2 - sum_Xi * sum_Xi) * (4 * sum_Yi2 - sum_Yi * sum_Yi)) ** 0.5
    r = cisl / znam
    return r