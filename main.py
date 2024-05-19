import math
import random
import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import scipy


time = 0.0                      # переменная времени
Tp = 0.0                        # время после T, когда уходит последний пациент
Na = 0                          # количество прибывших пациентов к моменту времени t
Nd = 0                          # количество уходов пациентов к моменту времени t
n = 0                           # количество пациентов к моменту времени t

Amount = 0
Work = 0.0

A = []                          # массив времени прибытия
W = []                          # массив время задержки пациента i в очереди
D = []                          # массив времени ухода пациента i по завершении обслуживания (приема)
TimeEvent = []                  # массив времен
N = []                          # количество клиентов
Event = []                      # список событий
ClientOfEvent = []              # список клиентов событий


# Функция дискретной интенсивности
def intensity_func(t):
    t = t + 8
    if 8 <= t < 9:
        return 13.1
    elif 9 <= t < 10:
        return 10.5
    elif 10 <= t < 11:
        return 12.7
    elif 11 <= t < 12:
        return 15.7
    elif 12 <= t < 13:
        return 14.1
    elif 13 <= t < 14:
        return 17.9
    elif 14 <= t < 15:
        return 18.5
    elif 15 <= t < 16:
        return 16.2
    elif 16 <= t < 17:
        return 16.6
    elif 17 <= t < 18:
        return 13.2
    elif 18 <= t < 19:
        return 15.0
    elif 19 <= t < 20:
        return 15.4
    elif 20 <= t < 21:
        return 14.6
    elif 21 <= t <= 22:
        return 13.2
    else:
        return 1


# Функция для генерации случайных времен обслуживания клиентов, используя экспоненциальное распределение.
def exponential_process(lambd):
    u = random.uniform(0, 1)
    t_process = -math.log(u) / lambd                            # случайное время обслуживания пациента
    return t_process


# Функция для генерации случайных времен прихода клиентов (Неоднородный Пуассоновский процесс)
def poison_process(t, poisson_lambda):
    while True:
        u1 = random.uniform(0, 1)
        t = t - (math.log(u1) / poisson_lambda)                # генерация интервальных времен
        u2 = random.uniform(0, 1)
        probability = intensity_func(t) / poisson_lambda       # вероятность появления клиентов
        if u2 <= probability:
            return t


# Приход пациента
def add_client():
    global time, Ta, Na, n, Amount, Td
    time = Ta                                                   # Ta - время прибытия пациента
    Na += 1                                                     # Na - количество прибывших клиентов (номер клиента)
    n += 1                                                      # n - количество пациентов
    Ta = poison_process(time, poisson_lambda)                   # Ta = Tt время следующего прибытия пациента
    if n == 1:
        Td = time + exponential_process(exponential_lambda)     # Td - время уход пациента
    A.append(time)                                              # A - время прихода пациента
    Amount = Amount + 1                                         # Amount - количество пациентов
    N.append(n)                                                 # N - количество клиентов
    TimeEvent.append(time)                                      # TimeEvent - время события
    Event.append('Приход клиента ' + str(Na))               # Event - событие (пациент пришел)


# Уход пациента
def remove_client():
    global Td, Nd, n, time
    time = Td                                                   # Td - время ухода пациента
    Nd += 1                                                     # Nd - количество уходов пациента
    n -= 1                                                      # n - количество пациентов (уменьшается если уходит пациент)
    if n == 0:                                                  # Если уходит последний пациент
        Td = 1e6                                                # Бесконечность
    else:                                                       # Если не уходит последний пациент
        Td = time + exponential_process(exponential_lambda)     # Td - время ухода пациента
    D.append(time)                                              # D - время ухода пациента
    N.append(n)                                                 # N - количество клиентов
    TimeEvent.append(time)                                      # TimeEvent - время события
    Event.append('Уход клиента ' + str(Nd))                     # Event - событие (пациент ушел)


# Пациенты, которые остались в очереди, но время работы закончилось
def remove_last_clients():
    global Td, Nd, n, time
    time = Td                                                   # Td - время ухода пациента
    Nd += 1                                                     # Nd - количество уходов пациента
    n -= 1                                                      # n - количество пациентов (уменьшается если уходит пациент)
    if n > 0:                                                   # Если уходит последний пациент
        Td = time + exponential_process(exponential_lambda)     # Td - время ухода пациента
    D.append(time)                                              # D - время ухода пациента
    TimeEvent.append(time)                                      # TimeEvent - время события
    N.append(n)                                                 # N - количество клиентов
    Event.append('Уход клиента ' + str(Nd))                    # Event - событие (пациент ушел)


# Если нет никаких пациентов
def end_shift():
    global n, Tp, time, T
    Tp = max(time - T, 0)                                       # время после T, когда уходит последний пациент




exponential_lambda = 20
poisson_lambda = 60
T_start = 8                     # Время начала работы
T_end = 22                      # Время конца работы
time = 0.0                      # Переменная времени
T = T_end - T_start
Ta = exponential_process(exponential_lambda)
Td = 1e6


print(f'Время начала смены: {T_start}')                         # Время начала смены
print(f'Время окончания смены: {T_end}')                        # Время окончания смены
print(f'Время работы: {T}')                                     # Время работы


while True:
    if Ta <= Td and Ta <= T:
        add_client()                                            # Добавить клиента
    if Td < Ta and Td <= T:
        remove_client()                                         # Обслужить клиента
    if min(Ta, Td) > T and n > 0:
        remove_last_clients()                                   # Обслужить последних клиентов
    if min(Ta, Td) > T and n == 0:
        end_shift()                                             # Закончить смену
        break




table1 = PrettyTable(['Событие',
                      'Время события',
                      'Клиентов в очереди'])
for i in range(10):
    if i == 9:
        table1.add_row([Event[i], TimeEvent[i] + 8, N[i]], divider=True)
    else:
        table1.add_row([Event[i], TimeEvent[i] + 8, N[i]])
for i in range(len(Event) - 10, len(Event)):
    table1.add_row([Event[i], TimeEvent[i] + 8, N[i]])
print(table1)




for i in range(len(TimeEvent)):
    # Если событие - приход клиента (первый в очереди), и в очереди только один клиент,
    # то его время ожидания равно 0.
    if Event[i][0] == 'П' and (N[i] <= 1):
        W.append(0)

    # Если событие - приход клиента, и в очереди уже есть другие клиенты,
    # вычисляем время ожидания как разницу между временем его прихода и временем прихода предыдущего клиента.
    elif Event[i][0] == 'П':
        ClientOfEvent.append(TimeEvent[i])

    # Если событие - уход клиента, и в очереди есть ожидающие клиенты,
    # извлекаем время прихода первого клиента из списка ожидающих и вычисляем его время ожидания.
    if Event[i][0] == 'У' and (len(ClientOfEvent) != 0):
        elem = ClientOfEvent[0]
        ClientOfEvent = ClientOfEvent[1:]
        W.append(TimeEvent[i] - elem)

    # обновляем время начала работы устройства.
    if Event[i][0] == 'П':
        if (i == 0) or (N[i - 1] == 0):
            if i == 0:
                Work = TimeEvent[i]
            else:
                Work = TimeEvent[i] - TimeEvent[i - 1]
    # Если событие - приход клиента, и это либо первый клиент в системе, либо после него был уход клиента,


table2 = PrettyTable(['№',
                      'Время прибытия(Ai)',
                      'Время ухода(Di)',
                      'Время обслуживания(Vi)',
                      'Время в очереди(Wi)',
                      'Время в системе(Di - Ai)'])
for i in range(10):
    if i == 9:
        table2.add_row([i + 1, A[i] + 8, D[i] + 8, D[i] - A[i] - W[i], W[i], D[i] - A[i]], divider=True)
    else:
        table2.add_row([i + 1, A[i] + 8, D[i] + 8, D[i] - A[i] - W[i], W[i], D[i] - A[i]])
for i in range(len(A) - 10, len(A)):
    table2.add_row([i + 1, A[i] + 8, D[i] + 8, D[i] - A[i] - W[i], W[i], D[i] - A[i]])
print('\n\n', table2)




print("Оценки:")
print('Количество клиентов за смену: ', Amount)
print('Время задержки закрытия: ', Tp)
print('Среднее время клиента в очереди: ', np.mean(W))
print('Среднее время клиента в системе: ', np.mean(np.array(D) - np.array(A)))
print('Коэффициент занятости устройства: ', 1 - (Work / T))
print('Средняя длина очереди: ', np.mean(N))

print("A = ", *A, sep='\n')
print("D = ", *D, sep='\n')
print("W = ", *W, sep='\n')

plt.title("Очереди")
plt.plot(np.arange(T_start, T_end, T / len(N)), N)
plt.show()

V = [D[i] - A[i] - W[i] for i in range(len(A))]
plt.title("График обслуживания")
plt.plot(list(range(len(A))), V)
plt.show()


V = [D[i] - A[i] for i in range(len(A))]
plt.title("График времени в системе")
plt.plot(list(range(len(A))), V)
plt.show()