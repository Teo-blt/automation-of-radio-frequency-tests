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
data = pd.read_csv('test.txt', sep='\s+', header=None)
data = pd.DataFrame(data)

x = {}
y = {}
i = 0

while i != len(data):
    if i != 0:
        i = i + 1
    x[data[3][i]] = ([data[0][i]])
    y[data[3][i]] = ([data[1][i]])
    try:
        while data[3][i] == data[3][i + 1]:
            x[data[3][i]] = x[data[3][i]] + [data[0][i + 1]]
            y[data[3][i]] = y[data[3][i]] + [data[1][i + 1]]
            i = i + 1
    except:
        break

print('fini')
color = {0: 'b', 1: 'r', 2: 'g', 3: 'y', 4: 'c', 5: 'lime', 6: 'black', 7: 'pink'}
for m in range(0, 8):
    plt.plot(x[m], y[m], color[m], marker=",")

plt.xlabel("Power at the entrance of the receiver in dBm")
plt.ylabel("% of packet lost")
plt.title("Graphical representation of sensitivity test results")
plt.show()
