from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk  # ("""FigureCanvasTkAgg,""")
from matplotlib.figure import Figure
import numpy as np
# from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import *
import random
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_4(self, elcolor):
    a = IntVar()
    f = IntVar()
    root = tk.Toplevel(self)
    root.wm_title("Embedding in Tk")
    my_scale_frame_2 = LabelFrame(root)
    my_scale_frame_2.pack()
    scale1 = Scale(my_scale_frame_2, orient='vertical', variable=a, troughcolor=elcolor, from_=100, to=0,
                   resolution=1, tickinterval=25, length=100, command=0,
                   label='amplitude', state="active")
    scale1.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale1.set(1)
    amplitude = Entry(my_scale_frame_2, validate="all", textvariable=a)
    amplitude.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale2 = Scale(my_scale_frame_2, orient='vertical', variable=f, troughcolor=elcolor, from_=10, to=0,
                   resolution=1, tickinterval=1, length=100, command=0,
                   label='frequency', state="active")
    scale2.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale2.set(1)
    frequency = Entry(my_scale_frame_2, validate="all", textvariable=f)
    frequency.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    button1 = tk.Button(master=my_scale_frame_2, text="Quit", command=lambda: root.destroy())
    button1.pack(side=LEFT)
    button2 = tk.Button(master=my_scale_frame_2, text="Start", command=lambda: eldraw(scale1, scale2))
    button2.pack(side=LEFT)
    fig = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    toolbar = NavigationToolbar2Tk(canvas, root)
    canvas.draw()
    toolbar.update()

    def eldraw(scale1, scale2):
        t = np.arange(0, 3, .01)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        fig.add_subplot(111).plot(t, scale1.get() * np.sin(scale2.get() * np.pi * t))


def draw_5(self, elcolor):
    global ani
    global ani2
    b = IntVar()
    root = tk.Toplevel(self)
    root.title('This is my Draw window')
    root.config(background='#fafafa')
    my_settings_frame = LabelFrame(root, text="Settings")
    my_settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    my_settings_frame.config(background='#fafafa')
    my_scale_frame = LabelFrame(my_settings_frame, bd=0)  # , text="Scales"
    my_scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    my_scale_frame.config(background='#fafafa')
    my_auto_scale_frame = LabelFrame(my_settings_frame, bd=0,
                                     text="my_auto_scale_frame")  # , text="my_auto_scale_frame"
    my_auto_scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    my_auto_scale_frame.config(background='#fafafa')
    my_button_frame = LabelFrame(my_settings_frame, bd=0)  # , text="Buttons"
    my_button_frame.pack(padx=0, pady=0, expand=True, fill="both", side=RIGHT)
    my_button_frame.config(background='#fafafa')
    my_RB_frame = LabelFrame(my_settings_frame, bd=0)  # , text="Choice"
    my_RB_frame.pack(padx=0, pady=0, expand=True, fill="both", side=RIGHT)
    my_RB_frame.config(background='#fafafa')

    button12 = tk.Button(my_scale_frame, text="Reset",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [scale_root_1.set(0), scale_root_2.set(40), scale_root_3.set(1)])
    button12.pack(padx=1, pady=1, expand=True, fill="both", side=LEFT)
    scale_root_1 = Scale(my_scale_frame, orient='vertical', troughcolor=elcolor, from_=120, to=-40,
                         resolution=1, tickinterval=25, length=100, command=0,
                         label='Order', state="active")
    scale_root_1.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    scale_root_2 = Scale(my_scale_frame, orient='vertical', troughcolor=elcolor, from_=100, to=1,
                         resolution=1, tickinterval=50, length=100, command=0,
                         label="window length", state="active")
    scale_root_2.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    scale_root_2.set(40)
    scale_root_3 = Scale(my_scale_frame, orient='vertical', troughcolor=elcolor, from_=10, to=0.1,
                         resolution=0.1, tickinterval=1, length=100, command=0,
                         label='delay in second', state="active")
    scale_root_3.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    scale_root_3.set(1)
    button13 = tk.Button(my_button_frame, text="Start",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [a(scale_root_3)[0].resume()])
    button13.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    button14 = tk.Button(my_button_frame, text="Stop",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [ani.pause()])
    button14.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    button15 = tk.Button(my_button_frame, text="Resume",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [ani.resume()])
    button15.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    button11 = tk.Button(my_button_frame, text="Quit",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: root.destroy())
    button11.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    RB2 = tk.Radiobutton(my_RB_frame, text="Automatic",
                         variable=b, value=1, cursor="right_ptr",
                         indicatoron=1, command=lambda: [my_scale_frame.pack_forget(),
                                                         my_auto_scale_frame.pack(padx=0, pady=0,
                                                                                  expand=True, fill="both", side=LEFT)])
    RB2.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    RB1 = tk.Radiobutton(my_RB_frame, text="Manual",
                         variable=b, value=0, cursor="right_ptr",
                         indicatoron=1, command=lambda: [my_scale_frame.pack(padx=0, pady=0,
                                                                             expand=True, fill="both", side=LEFT),
                                                         my_auto_scale_frame.pack_forget()])
    RB1.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    RB1.invoke()

    def a(scale_root_3):
        global ani
        global ani2
        xar = []
        yar = []

        style.use('ggplot')

        fig = plt.figure(figsize=(10, 4.5), dpi=100)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_ylim(-40, 120)
        ax2 = fig.add_subplot(1, 1, 1)
        ax2.set_ylim(-40, 120)
        line, = ax1.plot(xar, yar, 'r', marker='o')
        line2, = ax2.plot(xar, yar, 'b', marker='o')

        def init():
            line.set_ydata(np.ma.array(xar, mask=True))
            return line,

        def init2():
            line2.set_ydata(np.ma.array(xar, mask=True))
            return line2,

        def animate(i):
            yar.append(scale_root_1.get())
            xar.append(i)
            line.set_data(xar, yar)

            if i >= scale_root_2.get():
                a = i - scale_root_2.get()
                ax1.set_xlim(a, i + 1)
                if scale_root_2.get() == 100:
                    ax1.set_xlim(0, i + 1)
            else:
                ax1.set_xlim(0, i + 1)

        def animate2(r):
            yar.append(random.randint(-40, 120))
            xar.append(r)
            line2.set_data(xar, yar)

            if r >= scale_root_2.get():
                a = r - scale_root_2.get()
                ax2.set_xlim(a, r + 1)
                if scale_root_2.get() == 100:
                    ax2.set_xlim(0, r + 1)
            else:
                ax2.set_xlim(0, r + 1)

        plotcanvas = FigureCanvasTkAgg(fig, root)
        plotcanvas.get_tk_widget().grid(column=0, row=0)

        toolbar = NavigationToolbar2Tk(plotcanvas, my_button_frame)
        toolbar.update()

        ani = animation.FuncAnimation(fig, animate, interval=(scale_root_3.get() * 1000), blit=False, init_func=init)
        ani2 = animation.FuncAnimation(fig, animate2, interval=(scale_root_3.get() * 1000), blit=False, init_func=init2)
        return [ani, ani2]

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
