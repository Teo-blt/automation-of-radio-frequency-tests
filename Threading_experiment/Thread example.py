import threading
import time


# test of the functioning of the threading

class Mythread(threading.Thread):
    def __init__(self, data, var):  # data = additional data
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        self.data = data  # additional data added to the class
        self.var = var

    def run(self):
        if self.var == 1:
            for i in range(0, self.data):
                print("thread ", i)
                time.sleep(0.2)
        else:
            for i in range(0, self.data):
                print("thread2 ", i)
                time.sleep(0.2)

m = Mythread(10, 1)  # build the thread
m.start()  # lunch the thread,
m2 = Mythread(10, 2)

# instruction is executed in milliseconds, whatever the length of the thread


# __Main__
for i in range(0, 10):
    print("programme ", i)
    time.sleep(0.2)  # wait 100 milliseconds without doing anything,  makes the display easier to read
m2.start()