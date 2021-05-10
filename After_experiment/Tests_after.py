import tkinter as tk
import time

class Timer:
    def __init__(self, parent):
        # variable storing time
        self.seconds = 0
        # label displaying time
        self.label = tk.Label(parent, text="0 s", font="Arial 30", width=10)
        self.label.pack()
        # start the timer
        self.label.after(2000, lambda: self.refresh_label("gné1", "gné2"))

    def refresh_label(self, truc, truc2):
        """ refresh the content of the label every second """
        # increment the time
        self.seconds += 2
        # display the new time
        print(time.time())
        e = time.localtime(time.time())
        print(e)
        print("The test started at {} hours and {} minutes".format(e[3], e[4]))
        c = self.zuuuut()
        d = min(c)
        self.label.configure(text="%i s" % self.seconds)
        print(truc)
        print(truc2)

        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label.after(2000, lambda: self.refresh_label(d,d))

    def zuuuut(self):
        a = 2
        b = 6
        return [a, b]


if __name__ == "__main__":
    root = tk.Tk()
    timer = Timer(root)
    root.mainloop()
