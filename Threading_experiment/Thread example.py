import threading
import time


# test of the functioning of the threading

class Mythread(threading.Thread):
    def __init__(self, data):  # data = additional data
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        self.data = data  # additional data added to the class

    def run(self):
        for i in range(0, self.data):
            print("thread ", i)
            time.sleep(0.2)

m = Mythread(10)  # build the thread
m.start()  # lunch the thread,
# instruction is executed in milliseconds, whatever the length of the thread


# __Main__
for i in range(0, 10):
    print("programme ", i)
    time.sleep(0.2)  # wait 100 milliseconds without doing anything,  makes the display easier to read
