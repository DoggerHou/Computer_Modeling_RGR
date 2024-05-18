import math
import random
import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import scipy


time = 0.0 # переменная времени
Tp = 0.0 # время после T, когда уходит последний пациент
Na = 0 # количество прибывших пациентов к моменту времени t
Nd = 0 # количество уходов пациентов к моменту времени t
n = 0 # количество пациентов к моменту времени t

Amount = 0
Work = 0.0

A = [] # массив времени прибытия
W = [] # массив время задержки пациента i в очереди
D = [] # массив времени ухода пациента i по завершении обслуживания (приема)
TimeEvent = [] # массив времен
N = [] # количество клиентов
Event = [] # список событий
ClientOfEvent = [] # список клиентов событий


exponential_lambda = 30
poisson_lambda = 1.5
T_start = 8                     # Время начала работы
T_end = 22                      # Время конца работы
time = 0.0                      # Переменная времени


# Функция дискретной интенсивности
def intensity_func(t):
    t = t + 8
    if 8 <= t < 9:
        return 0.2183
    elif 9 <= t < 10:
        return 0.175
    elif 10 <= t < 11:
        return 0.2117
    elif 11 <= t < 12:
        return 0.2617
    elif 12 <= t < 13:
        return 0.235
    elif 13 <= t < 14:
        return 0.2983
    elif 14 <= t < 15:
        return 0.3083
    elif 15 <= t < 16:
        return 0.27
    elif 16 <= t < 17:
        return 0.2767
    elif 17 <= t < 18:
        return 0.22
    elif 18 <= t < 19:
        return 0.25
    elif 19 <= t < 20:
        return 0.2567
    elif 20 <= t < 21:
        return 0.2433
    elif 21 <= t <= 22:
        return 0.22
    else:
        return 1


# Функция для генерации случайных времен обслуживания клиентов, используя экспоненциальное распределение.
def exponential_process(lambd):
    u = random.uniform(0, 1)
    t_process = -math.log(u) / lambd  # случайное время обслуживания пациента
    return t_process


# Функция для генерации случайных времен прихода клиентов (Неоднородный Пуассоновский процесс)
def poison_process(t, lambd):
    while True:
        u1 = random.uniform(0, 1)
        t = t - (math.log(u1) / lambd)                          # генерация интервальных времен
        u2 = random.uniform(0, 1)
        probability = intensity_func(t) / lambd                 # вероятность появления клиентов
        if u2 <= probability:
            print(f'Вероятность появления клиентов (от 0 до 1) = {probability}')
            print('Время прибытия клиента =', t)
            return t


# Приход пациента
def arrival_patient():
    global time, Ta, Na, n, Amount, Td
    time = Ta                                                   # Ta - время прибытия пациента
    Na = Na + 1                                                 # Na - количество прибывших пациентов (номер пациента)
    n = n + 1                                                   # n - количество пациентов
    Ta = poison_process(time, poisson_lambda)                   # Ta = Tt время следующего прибытия пациента
    if n == 1:
        Td = time + exponential_process(exponential_lambda)     # Td - время уход пациента
    A.append(time)                                              # A - время прихода пациента
    Amount = Amount + 1                                         # Amount - количество пациентов
    N.append(n)                                                 # N - количество клиентов
    TimeEvent.append(time)                                      # TimeEvent - время события
    Event.append('Пациент ' + str(Na) + ' пришел')              # Event - событие (пациент пришел)


# Уход пациента
def leave_patient():
    global Td, Nd, n, time
    time = Td                                                   # Td - время ухода пациента
    Nd = Nd + 1                                                 # Nd - количество уходов пациента
    n = n - 1                                                   # n - количество пациентов (уменьшается если уходит пациент)
    if n == 0:                                                  # Если уходит последний пациент
        Td = 1e6                                                # Бесконечность
    else:                                                       # Если не уходит последний пациент
        Td = time + exponential_process(exponential_lambda)     # Td - время ухода пациента
    D.append(time)                                              # D - время ухода пациента
    N.append(n)                                                 # N - количество клиентов
    TimeEvent.append(time)                                      # TimeEvent - время события
    Event.append('Уход пациента ' + str(Nd))                    # Event - событие (пациент ушел)

# Пациенты, которые остались в очереди, но время работы закончилось
def last_patient():
    global Td, Nd, n, time
    time = Td                                                   # Td - время ухода пациента
    Nd += 1                                                     # Nd - количество уходов пациента
    n -= 1                                                      # n - количество пациентов (уменьшается если уходит пациент)
    if (n > 0):                                                 # Если уходит последний пациент
        Td = time + exponential_process(exponential_lambda)     # Td - время ухода пациента
    D.append(time)                                              # D - время ухода пациента
    TimeEvent.append(time)                                      # TimeEvent - время события
    N.append(n)                                                 # N - количество клиентов
    Event.append('Уход пациента: ' + str(Nd))                   # Event - событие (пациент ушел)


# Если нет никаких пациентов
def end_patient():
    global n, Tp, time, T
    Tp = max(time - T, 0)                                       # время после T, когда уходит последний пациент
    # N.append(n) # N - количество клиентов


T = T_end - T_start
Ta = exponential_process(exponential_lambda)
Td = 1e6

print(f'Время начала смены: {T_start}') # Время начала смены
print(f'Время окончания смены: {T_end}') # Время окончания смены
print(f'Время работы: {T}') # Время работы

while True:
    if Ta <= Td and Ta <= T:
        arrival_patient()
    if Td < Ta and Td <= T:
        leave_patient()
    if min(Ta, Td) > T and n > 0:
        last_patient()
    if min(Ta, Td) > T and n == 0:
        end_patient()
        break


table1 = PrettyTable(['Событие', 'Время события', 'Пациентов в очереди'])
for i in range(len(TimeEvent)):
    table1.add_row([Event[i], TimeEvent[i] + 8, N[i]])

    # Если событие - приход клиента (первый в очереди), и в очереди только один клиент,
    # то его время ожидания равно 0.
    if (Event[i][0] == 'П') and (N[i] <= 1):
        W.append(0)

    # Если событие - приход клиента, и в очереди уже есть другие клиенты,
    # вычисляем время ожидания как разницу между временем его прихода и временем прихода предыдущего клиента.
    elif (Event[i][0] == 'П'):
        ClientOfEvent.append(TimeEvent[i] + 8)

    # Если событие - уход клиента, и в очереди есть ожидающие клиенты,
    # извлекаем время прихода первого клиента из списка ожидающих и вычисляем его время ожидания.
    if (Event[i][0] == 'У') and (len(ClientOfEvent) != 0):
        elem = ClientOfEvent[0]
        ClientOfEvent = ClientOfEvent[1:]
        W.append(TimeEvent[i] + 8 - elem)

    # Если событие - приход клиента, и это либо первый клиент в системе, либо после него был уход клиента,
    # обновляем время начала работы устройства.
    if (Event[i][0] == 'П'):
        if (i == 0) or (N[i - 1] == 0):
            if (i == 0):
                Work = TimeEvent[i]
                print(f'Work i == 0 {Work}')
            else:
                Work = TimeEvent[i] - TimeEvent[i - 1]
                print(f'Work else {Work}')

print(table1)