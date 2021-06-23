import pandas as pd
data = pd.read_csv('test.txt', sep=' ',header=None)
data = pd.DataFrame(data)

import matplotlib.pyplot as plt
x = data[0]
print(x)
y = data[1]
print(y)
plt.plot(x, y,'r--')
plt.show()