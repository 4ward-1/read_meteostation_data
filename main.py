import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import os
from datetime import datetime
import pylab

def readfile(file_name = 'all'):
    if file_name == 'all': #Чтение и загрузка файлов (все файлы в директории)
        combined = pd.DataFrame()
        file_names = ''
        for file in os.listdir():
            if file.endswith(".txt") or file.endswith(".TXT"):
                file_names += os.path.join(file) + ' '
        file_names_list = file_names.split()

        for file_ in file_names_list:
            data = pd.read_csv(file_, header=None)
            data['filename'] = file_
            # Объединение данных
            combined = pd.concat([combined, data])
        # Преобразование данных в массив
        data = np.array(combined)
    else: #Чтение и загрузка файлов (1 конкретный файл)
        data = pd.read_csv(file_name, header=None)
        # Преобразование данных в массив
        data = np.array(data)

    data_all = data
    N = int(len(data_all))

    # Массив для чисел типа int
    year   = np.arange(0, N, 1)
    month  = np.arange(0, N, 1)
    day    = np.arange(0, N, 1)
    hour   = np.arange(0, N, 1)
    minut  = np.arange(0, N, 1)
    second = np.arange(0, N, 1)

    # Массив для чисел типа float
    temp1  = np.empty([N, 1], dtype=float)
    temp2  = np.empty([N, 1], dtype=float)
    temp3  = np.empty([N, 1], dtype=float)
    humadi = np.empty([N, 1], dtype=float)

    for i in range(len(data_all)):
        a1 = str(data_all[i])
        a1 = a1.split()
        beg    = a1[0]
        end    = a1[9]

        year[i]   = int(beg[2:len(beg)])
        month[i]  = int(a1[1])
        day[i]    = int(a1[2])
        hour[i]   = int(a1[3])
        minut[i]  = int(a1[4])
        second[i] = int(a1[5])
        temp1[i]  = float(a1[6])
        temp2[i]  = float(a1[7])
        temp3[i]  = float(a1[8])
        humadi[i] = float(end[0:len(end) - 2])

    # Если температура с датчиков некорректная, то изменяем на ближайшую
    for i in range(len(temp1)):
        if ((temp1[i] == 85.00) or (temp2[i] == 85.00)) and i == 0:
            temp1[i] = temp1[i+1]
            temp2[i] = temp2[i+1]
        elif ((temp1[i] == 85.00) or (temp2[i] == 85.00)) and i != 0:
            temp1[i] = temp1[i-1]
            temp2[i] = temp2[i-1]

    # Время в днях и в годах от начала записи файла
    time_day  = np.arange(0, len(year), 1, dtype=float)
    time_year = np.arange(0, len(year), 1, dtype=float)

    for i in range(len(year)):
        time_day[i]  = day[i] + hour[i]/24 + minut[i]/60/24 + second[i]/60/60/24
        time_year[i] = year[i] + month[i]/12 + day[i]/31/12 + hour[i]/24/31/12 + minut[i]/60/24/31/12 + second[i]/60/60/24/31/12

    # Время в формате date
    time_values = []
    for i in range(len(year)):
        time_values.append(datetime(year[i],month[i],day[i],hour[i],minut[i],second[i]))
    temp_mean = (temp1 + temp2 + temp3) / 3
    dates1 = dates.date2num(time_values)

    # Сортировка времени при склеивании файлов по возрастанию, дальше найти индекс
    # из сортированного массива и сопоставить его с индексом из несортированного массива
    time_year_sorted = np.sort(time_year)
    print(time_year_sorted)
    indexes_sorted = []
    for i in range(len(time_year_sorted)):
        indexes_sorted.append(np.where(time_year == time_year_sorted[i])[0][0])
    print(indexes_sorted[0])
    # Отсортированные по времени данные
    time_values_sorted = []
    temp_mean_sorted   = []
    humadi_sorted      = []

    for i in range(len(time_year_sorted)):
        time_values_sorted.append(time_values[indexes_sorted[i]])
        temp_mean_sorted.append(temp_mean[indexes_sorted[i]])
        humadi_sorted.append(humadi[indexes_sorted[i]])
    dates1_sorted = dates.date2num(time_values_sorted)

    pylab.subplot(2, 1, 1)
    pylab.plot_date(dates1_sorted[:], temp_mean_sorted[:],'-')
    plt.grid(color='red', linewidth=1, linestyle='--')
    plt.ylim([min(temp_mean) - 3, max(temp_mean) + 3])
    pylab.title("График изменения температуры")
    pylab.ylabel("град.C")

    pylab.subplot(2, 1, 2)
    pylab.plot_date(dates1_sorted[:], humadi_sorted[:],'-')
    plt.grid(color='red', linewidth=1, linestyle='--')
    plt.ylim([min(humadi) - 3, max(humadi) + 3])
    pylab.title("График изменения влажности")
    pylab.ylabel("%")
    pylab.xlabel("Время")
    plt.show()

readfile('all') # 'all' - загружает все файлы и объединяет их, 'имя файла' - загружает конктретный файл