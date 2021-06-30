import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger


def draw_graph():
    try:
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

    except:
        logger.critical("Error no data available in test.txt")
