import pandas as pd
import matplotlib.pyplot as plt

color = {0: 'b', 1: 'r', 2: 'g', 3: 'y', 4: 'c', 5: 'lime', 6: 'black', 7: 'pink'}
freq = ['867.1']
freq_step = 0.2
paket_rate = 50
graph_type = 1

data = pd.read_csv('data.txt', sep='\s+', header=None)
data = pd.DataFrame(data)
temp = {0: data[4][0]}
X = {}
Y = {}
numbers_of_channel = max(data[3]) + 1
number_of_temp = max(data[2]) + 1
t = 0
d = 0
while t != len(data):
    if data[4][t] > temp[d]:
        d += 1
        temp[d] = data[4][t]
    if t != 0:
        t = t + 1
    else:
        for i in range(0, number_of_temp):
            X[i] = {}
            Y[i] = {}
    X[data[2][t]][data[3][t]] = [data[0][t]]
    Y[data[2][t]][data[3][t]] = [data[1][t]]
    try:
        while data[3][t] == data[3][t + 1]:
            X[data[2][t]][data[3][t]] = X[data[2][t]][data[3][t]] + [data[0][t + 1]]
            Y[data[2][t]][data[3][t]] = Y[data[2][t]][data[3][t]] + [data[1][t + 1]]
            t = t + 1
    except:
        break
if graph_type == 0:
    for m in range(0, number_of_temp):
        marker = "$" + str(m) + "$"
        for n in range(0, numbers_of_channel):
            plt.plot(X[m][n], Y[m][n], color[n], marker=marker, label="Channel " + str(n))
    plt.xlabel("Power at the entrance of the receiver in dBm")
    plt.ylabel("% of packet lost")
    plt.title("Graphical representation of sensitivity test results")
    plt.legend()
    plt.show()

x = 0
y = 0
G = {}
for r in range(0, numbers_of_channel):
    G[r] = {}
    if r != 0:
        freq = freq + [str(round(float(freq[r - 1]) + freq_step, 1))]

for x in range(0, number_of_temp):
    for y in range(0, numbers_of_channel):
        more_than_paket_rate = 0
        try:
            while Y[x][y][more_than_paket_rate] < paket_rate:
                more_than_paket_rate += 1
            if Y[x][y][more_than_paket_rate] == paket_rate:
                G[x][y] = X[x][y][more_than_paket_rate]
            else:
                delta_y = round(abs(X[x][y][more_than_paket_rate - 1] - X[x][y][more_than_paket_rate]), 10)
                delta_x = abs(Y[x][y][more_than_paket_rate - 1] - Y[x][y][more_than_paket_rate])
                delta = -(delta_x / delta_y)
                a = Y[x][y][more_than_paket_rate] - (delta * X[x][y][more_than_paket_rate])
                value = (50 - a) / delta
                G[x][y] = value
        except:
            pass

if graph_type == 1:
    j = 0
    for s in range(0, number_of_temp):
        if j > 7:
            j = 0
        plt.plot(freq[0:len(G[s].values())], G[s].values(), "o-", color=color[j], label=str(temp[s]) + "°C")
        j += 1
    plt.xlabel("Channel frequency")
    plt.ylabel("Power at the entrance of the receiver in dBm")
    plt.title(f"Graphical representation of sensitivity test results for {paket_rate}% of packet lost")
    plt.legend()
    plt.show()
