import pandas as pd
import matplotlib.pyplot as plt


def write_json(power, frames, etuve, chanel):
    outfile = open('void.txt', 'a')
    outfile.write(str(power) + ' ' + str(frames) + ' ' + str(etuve) + ' ' + str(chanel) + '\n')
    outfile.close()


outfile = open('void.txt', 'w+')
outfile.close()

write_json(1, 10, 0, 0)
write_json(2, 16, 0, 0)
write_json(3, 20, 0, 0)
write_json(4, 39, 0, 0)
write_json(5, 49, 0, 0)
write_json(6, 56, 0, 0)

write_json(7, 10, 0, 1)
write_json(8, 16, 0, 1)
write_json(9, 20, 0, 1)
write_json(10, 39, 0, 1)
write_json(11, 49, 0, 1)
write_json(12, 56, 0, 1)

write_json(13, 10, 1, 0)
write_json(14, 16, 1, 0)
write_json(15, 20, 1, 0)
write_json(16, 39, 1, 0)
write_json(17, 49, 1, 0)
write_json(18, 56, 1, 0)

write_json(19, 10, 1, 1)
write_json(20, 16, 1, 1)
write_json(21, 20, 1, 1)
write_json(22, 39, 1, 1)
write_json(23, 49, 1, 1)
write_json(24, 56, 1, 1)

write_json(25, 10, 2, 0)
write_json(26, 16, 2, 0)
write_json(27, 20, 2, 0)
write_json(28, 39, 2, 0)
write_json(29, 49, 2, 0)
write_json(30, 56, 2, 0)

write_json(31, 10, 2, 1)
write_json(32, 16, 2, 1)
write_json(33, 20, 2, 1)
write_json(34, 39, 2, 1)
write_json(35, 49, 2, 1)
write_json(36, 56, 2, 1)

data = pd.read_csv('void.txt', sep='\s+', header=None)
data = pd.DataFrame(data)

X = {}
Y = {}
numbers_of_channel = (data[3][len(data) - 1]) + 1
number_of_temp = (data[2][len(data)-1]) + 1
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
    for n in range(0, numbers_of_channel):
        plt.plot(X[m][n], Y[m][n], color[m], marker=",")

plt.xlabel("Power at the entrance of the receiver in dBm")
plt.ylabel("% of packet lost")
plt.title("Graphical representation of sensitivity test results")
plt.show()