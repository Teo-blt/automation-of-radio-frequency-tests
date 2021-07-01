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

write_json(-125, 15, 1, 0)
write_json(-126, 67, 1, 0)
write_json(-127, 80, 1, 0)
write_json(-128, 95, 1, 0)

write_json(-125, 4, 1, 1)
write_json(-126, 15, 1, 1)
write_json(-127, 35, 1, 1)
write_json(-128, 93, 1, 1)

write_json(-125, 28, 1, 2)
write_json(-126, 48, 1, 2)
write_json(-127, 52, 1, 2)
write_json(-128, 68, 1, 2)

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

print(G)
plt.plot(G.keys(), G.values(), color='r', marker=' ')
plt.xlabel("Number of channel")
plt.ylabel("Power at the entrance of the receiver in dBm")
plt.title("Graphical representation of sensitivity test results for 50% of packet lost")
plt.show()