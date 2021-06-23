import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger

def draw_graph():
    try:
        data = pd.read_csv('test.txt', sep='\s+', header=None)
        data = pd.DataFrame(data)
        x = data[0]
        y = data[1]
        plt.plot(x, y, 'r', marker=",")
        plt.legend("test")
        plt.show()
    except:
        logger.critical("Error no data available in test.txt")

draw_graph()