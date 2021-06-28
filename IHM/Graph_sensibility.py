import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger


def draw_graph():
    try:
        data = pd.read_csv('test.txt', sep='\s+', header=None)
        data = pd.DataFrame(data)
        x = []
        y = []
        x1 = []
        y1 = []
        x2 = []
        y2 = []
        x3 = []
        y3 = []
        for i in range(0, len(data)):
            if data[2][i] == 0:
                if (data[3][i]) == 0:
                    x = x + [data[0][i]]
                    y = y + [data[1][i]]
                else:
                    x1 = x1 + [data[0][i]]
                    y1 = y1 + [data[1][i]]
            else:
                if data[3][i] == 0:
                    x2 = x2 + [data[0][i]]
                    y2 = y2 + [data[1][i]]
                else:
                    x3 = x3 + [data[0][i]]
                    y3 = y3 + [data[1][i]]

        plt.plot(x, y, 'b', marker=",")
        plt.plot(x1, y1, 'r', marker=",")
        plt.plot(x2, y2, 'y', marker=",")
        plt.plot(x3, y3, 'g', marker=",")

        plt.xlabel("bla 1")
        plt.ylabel("bla 2")
        plt.title("Graphical representation of sensitivity test results")
        plt.show()

    except:
        logger.critical("Error no data available in test.txt")
