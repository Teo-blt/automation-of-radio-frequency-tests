from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk  # ("""FigureCanvasTkAgg,""")
from matplotlib.figure import Figure
import numpy as np
# from matplotlib.animation import FuncAnimation
# from random import randint
import tkinter as tk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_4(self, amplitude, frequency):
    root = tk.Toplevel(self)
    root.wm_title("Embedding in Tk")
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)

    fig.add_subplot(111).plot(t, amplitude * np.sin(frequency * np.pi * t))

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    button = tk.Button(master=root, text="Quit", command=lambda: root.destroy())
    button.pack(side=tk.BOTTOM)


def draw_5(self, elcolor, scale1, scale2):
    root = tk.Toplevel(self)
    root.title('This is my Draw window')
    root.config(background='#fafafa')

    xar = []
    yar = []

    style.use('ggplot')
    fig = plt.figure(figsize=(10, 4.5), dpi=100)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_ylim(0, 100)
    line, = ax1.plot(xar, yar, 'r', marker='o')

    button12 = tk.Button(root, text="quit",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: root.destroy())
    button12.grid(row=1, column=1, ipadx=4, ipady=4, padx=0, pady=0)


    def animate(i):
        print(scale1.get())
        yar.append(99 - scale1.get())
        xar.append(i)
        line.set_data(xar, yar)
        ax1.set_xlim(0, i + scale2.get())

    plotcanvas = FigureCanvasTkAgg(fig, root)
    plotcanvas.get_tk_widget().grid(column=0, row=0)
    ani = animation.FuncAnimation(fig, animate, interval=1000, blit=False)

    root.mainloop()


""""
def draw_2(self):
    global x1, y1, dx, dy, flag
    flag = 0  # switch
    x1, y1 = 10, 10  # innitialisation
    dx, dy = 15, 10  # 'step' of the move

    def move():
        "move the ball"
        global x1, y1, dx, dy, flag
        x1, y1 = x1 + dx, y1 + dy
        if x1 > 210:
            x1, dx, dy = 210, 0, 15
        if y1 > 210:
            y1, dx, dy = 210, -15, 0
        if x1 < 10:
            x1, dx, dy = 10, 0, -15
        if y1 < 10:
            y1, dx, dy = 10, 15, 0
        can1.coords(oval1, x1, y1, x1 + 30, y1 + 30)
        if flag > 0:
            my_graphic_frame_2.after(50, move)  # => loop after 50 millisecondes

    def stop_it():
        "stop the animation"
        global flag
        flag = 0

    def start_it():
        start annimation
        global flag
        if flag == 0:  # for only one loop
            flag = 1
        move()

    my_graphic_frame_2 = LabelFrame(self, text="Graphic")
    my_graphic_frame_2.grid(row=0, column=3, ipadx=40, ipady=5, padx=0, pady=0)
    can1 = Canvas(my_graphic_frame_2, bg='dark grey', height=250, width=250)
    can1.pack(side=LEFT, padx=5, pady=5)
    oval1 = can1.create_oval(x1, y1, x1 + 30, y1 + 30, width=2, fill='red')
    bou1 = Button(my_graphic_frame_2, text='Quit', width=8, command=my_graphic_frame_2.destroy)
    bou1.pack(side=BOTTOM)
    bou2 = Button(my_graphic_frame_2, text='Start', width=8, command=start_it)
    bou2.pack()
    bou3 = Button(my_graphic_frame_2, text='Stop', width=8, command=stop_it)
    bou3.pack()
    ====================================================================
def draw_3(self)
    my_graphic_frame_2 = LabelFrame(self, text="Graphic")
    my_graphic_frame_2.grid(row=0, column=3, ipadx=40, ipady=5, padx=0, pady=0)
    canv = Canvas(my_graphic_frame_2, bg="white", height=200, width=200)
    canv.pack()
    oval = (0, 0, 200, 200)
    line1 = (0, 0, 200, 200)
    line2 = (0, 200, 200, 0)
    canv.create_oval(oval, outline="red", width=10)
    canv.create_line(line1, fill="black", width=10)
    canv.create_line(line2, fill="black", width=10)
    canv.create_rectangle((0, 0), (200, 200),
                          fill="cyan", outline="blue", width=5)

    canv.create_oval((0, 0), (200, 200),
                     fill="pink", outline="red", width=3)

    canv.create_line((0, 0), (180, 100), (200, 200),
                     fill="gray", width=3, dash=(8, 4))

    canv.create_line((0, 0), (180, 100), (200, 200),
                     fill="black", width=5, smooth=True,
                     arrow="last", arrowshape=(30, 45, 15))
=================================================================
def draw_1(self, small_width, small_height):
    global chain
    my_graphic_frame_1 = LabelFrame(self, text="Graphic")
    my_graphic_frame_1.grid(row=1, column=2, ipadx=0, ipady=0, padx=0, pady=0)
    canv = Canvas(my_graphic_frame_1, width=small_width, height=small_height, bg="white")
    canv.bind("<Motion>", pointeur_in)
    canv.bind("<Leave>", pointeur_out)
    canv.bind("<Double-Button-1>", pointeur_double)
    chain = Label(my_graphic_frame_1, text="")
    chain.pack()
    canv.pack()
    w = canv.winfo_reqwidth()  # Get current width of canvas
    h = canv.winfo_reqheight()  # Get current height of canvas
    canv.create_line([(2, 0), (2, h)], fill="Black", width=1, tag='grid_line')
    canv.create_line([(0, 2), (w, 2)], fill="Black", width=1, tag='grid_line')

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, 50):
        canv.create_line([(i, 0), (i, h)], fill="black", width=1, tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, 50):
        canv.create_line([(0, i), (w, i)], fill="black", width=1, tag='grid_line')


def pointeur_in(event):
    chain.configure(text="Clic detecte in X =" + str(event.x) + ", Y =" + str(event.y))


def pointeur_out(event):
    chain.configure(text="")


def pointeur_double(event):
    big_graph = tk.Toplevel()
    big_graph.configure(bg="grey")
    big_graph.title("big window")
    big_graph.geometry('530x600')
    draw_1(big_graph, 500, 500)

"""
