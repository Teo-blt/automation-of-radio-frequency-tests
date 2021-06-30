import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger


def draw_graph():
    try:
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
            for n in range(0, numbers_of_channel):
                plt.plot(X[m][n], Y[m][n], color[m], marker=",")

        plt.xlabel("Power at the entrance of the receiver in dBm")
        plt.ylabel("% of packet lost")
        plt.title("Graphical representation of sensitivity test results")
        plt.show()

    except:
        logger.critical("Error no data available in test.txt")
