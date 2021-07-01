import pandas as pd
import matplotlib.pyplot as plt


def write_json(power, frames, etuve, chanel):
    outfile = open('void.txt', 'a')
    outfile.write(str(power) + ' ' + str(frames) + ' ' + str(etuve) + ' ' + str(chanel) + '\n')
    outfile.close()


outfile = open('void.txt', 'w+')
outfile.close()

write_json(-125, 20, 0, 0)
write_json(-126, 41, 0, 0)
write_json(-127, 82, 0, 0)
write_json(-128, 95, 0, 0)

write_json(-125, 19, 0, 1)
write_json(-126, 40, 0, 1)
write_json(-127, 87, 0, 1)
write_json(-128, 90, 0, 1)

write_json(-125, 7, 0, 2)
write_json(-126, 18, 0, 2)
write_json(-127, 74, 0, 2)
write_json(-128, 84, 0, 2)

write_json(-125, 19, 0, 3)
write_json(-126, 39, 0, 3)
write_json(-127, 78, 0, 3)
write_json(-128, 90, 0, 3)

write_json(-125, 21, 0, 4)
write_json(-126, 42, 0, 4)
write_json(-127, 90, 0, 4)
write_json(-128, 100, 0, 4)

write_json(-125, 1, 0, 5)
write_json(-126, 20, 0, 5)
write_json(-127, 67, 0, 5)
write_json(-128, 80, 0, 5)

write_json(-125, 15, 1, 0)
write_json(-126, 67, 1, 0)
write_json(-127, 80, 1, 0)
write_json(-128, 95, 1, 0)

write_json(-125, 4, 1, 1)
write_json(-126, 15, 1, 1)
write_json(-127, 35, 1, 1)
write_json(-128, 93, 1, 1)

write_json(-125, 3, 1, 2)
write_json(-126, 32, 1, 2)
write_json(-127, 64, 1, 2)
write_json(-128, 99, 1, 2)

write_json(-125, 15, 1, 3)
write_json(-126, 48, 1, 3)
write_json(-127, 74, 1, 3)
write_json(-128, 98, 1, 3)

write_json(-125, 13, 1, 4)
write_json(-126, 25, 1, 4)
write_json(-127, 55, 1, 4)
write_json(-128, 73, 1, 4)

write_json(-125, 0, 1, 5)
write_json(-126, 14, 1, 5)
write_json(-127, 34, 1, 5)
write_json(-128, 84, 1, 5)

data = pd.read_csv('void.txt', sep='\s+', header=None)
data = pd.DataFrame(data)

X = {}
Y = {}
numbers_of_channel = (data[3][len(data) - 1]) + 1
number_of_temp = (data[2][len(data) - 1]) + 1
t = 0
while t != len(data):
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
color = {0: 'b', 1: 'r', 2: 'g', 3: 'y', 4: 'c', 5: 'lime', 6: 'black', 7: 'pink'}
for m in range(0, number_of_temp):
    marker = "$" + str(m) + "$"
    for n in range(0, numbers_of_channel):
        pass
        #plt.plot(X[m][n], Y[m][n], color[n], marker=marker)

plt.xlabel("Power at the entrance of the receiver in dBm")
plt.ylabel("% of packet lost")
plt.title("Graphical representation of sensitivity test results")
#plt.show()
x = 0
y = 0
G = {}
freq = ['867.1']
for r in range(0, numbers_of_channel):
    G[r] = {}
    if r != 0:
        freq = freq + [str(round(float(freq[r - 1]) + 0.2, 1))]

for x in range(0, number_of_temp):
    for y in range(0, numbers_of_channel):
        more_than_50 = 0
        while Y[x][y][more_than_50] <= 50:
            more_than_50 += 1
        delta_y = abs(X[x][y][more_than_50 - 1] - X[x][y][more_than_50])
        delta_x = abs(Y[x][y][more_than_50 - 1] - Y[x][y][more_than_50])
        delta = -(delta_x / delta_y)
        a = Y[0][0][0] - (delta * X[0][0][0])
        value = (50 - a) / delta
        G[x][y] = value

for s in range(0, number_of_temp):
    plt.plot(freq, G[s].values(), "o-", color=color[s],  label=str(s*10) + "°C")
plt.xlabel("Channel frequency")
plt.ylabel("Power at the entrance of the receiver in dBm")
plt.title("Graphical representation of sensitivity test results for 50% of packet lost")
plt.legend()
plt.show()