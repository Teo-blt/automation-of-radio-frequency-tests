#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: April 23 16:15:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
# Imports
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk  # ("""FigureCanvasTkAgg,""")
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Climate_chamber_control import Climate_chamber_V2

# =============================================================================
VARIABLE = Climate_chamber_V2  # Climate_chamber
FRAME = (-50, 90)


def draw_4(self, elcolor):
    global my_scale_frame_1
    global first_time
    first_time = 1
    root = tk.Toplevel(self)
    root.wm_title("Embedding in Tk")
    my_scale_frame_2 = LabelFrame(root)
    my_scale_frame_2.pack()

    def clean():
        global my_scale_frame_1
        my_scale_frame_1.destroy()

    def create():
        global my_scale_frame_1
        my_scale_frame_1 = LabelFrame(root)
        my_scale_frame_1.pack(side=BOTTOM)
        t = np.arange(0, 3, .01)
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot().plot(t, scale1.get() * np.sin(scale2.get() * np.pi * t))
        canvas = FigureCanvasTkAgg(fig, master=my_scale_frame_1)
        toolbar = NavigationToolbar2Tk(canvas, my_scale_frame_1, pack_toolbar=False)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar.pack(side=BOTTOM, fill=X)

    def eldraw():
        global my_scale_frame_1
        global first_time
        if first_time == 1:
            create()
            first_time = 2
        else:
            clean()
            create()

    def enter(event):
        eldraw()
        print("a")

    a = IntVar()
    f = IntVar()
    root.bind("<Return>", enter)

    scale1 = Scale(my_scale_frame_2, orient='vertical', variable=a, from_=100, to=0,
                   resolution=1, tickinterval=25, length=100, troughcolor=elcolor,
                   command=lambda x: eldraw(),
                   label='amplitude', state="active")
    scale1.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale1.set(1)
    amplitude = Entry(my_scale_frame_2, validate="all", textvariable=a)
    amplitude.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale2 = Scale(my_scale_frame_2, orient='vertical', variable=f, from_=10, to=0,
                   resolution=1, tickinterval=1, length=100, troughcolor=elcolor,
                   command=lambda x: eldraw(),
                   label='frequency', state="active")
    scale2.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale2.set(1)
    frequency = Entry(my_scale_frame_2, validate="all", textvariable=f)
    frequency.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    button1 = Button(master=my_scale_frame_2, text="Quit", background=elcolor, command=lambda: root.destroy())
    button1.pack(side=LEFT)


def draw_5(self, elcolor):
    def display():
        style.use('ggplot')
        fig = plt.figure(figsize=(10, 3), dpi=100)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_ylim(-40, 120)
        plotcanvas = FigureCanvasTkAgg(fig, root)
        plotcanvas.get_tk_widget().grid(column=0, row=0)

    global ani
    global ani2
    global first_time
    first_time = 1
    b = IntVar()
    root = tk.Toplevel(self)
    root.title('Draw window')
    root.config(background='#fafafa')
    my_settings_frame = LabelFrame(root, text="Settings")
    my_settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    my_settings_frame.config(background='#fafafa')
    my_scale_frame = LabelFrame(my_settings_frame, bd=0)  # , text="Scales"
    my_scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    my_scale_frame.config(background='#fafafa')
    my_auto_scale_frame = LabelFrame(my_settings_frame, bd=0)  # , text="my_auto_scale_frame"
    my_auto_scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    my_auto_scale_frame.config(background='#fafafa')
    my_button_frame = LabelFrame(my_settings_frame, bd=0)  # , text="Buttons"
    my_button_frame.pack(padx=0, pady=0, expand=True, fill="both", side=RIGHT)
    my_button_frame.config(background='#fafafa')
    my_rb_frame = LabelFrame(my_settings_frame, bd=0)  # , text="Choice"
    my_rb_frame.pack(padx=0, pady=0, expand=True, fill="both", side=RIGHT)
    my_rb_frame.config(background='#fafafa')
    display()
    label = tk.Label(my_auto_scale_frame, text="Settings_chamber", bg="white", font="arial",
                     fg="black", relief="groove")
    label.grid(row=0, column=0, ipadx=20, ipady=20, padx=0, pady=0)
    button16 = tk.Button(my_auto_scale_frame, text="Start",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [VARIABLE.Mythread(scale1.get(), scale2.get(),
                                                            scale4.get(), scale5.get(),
                                                            scale3.get(), 0, my_auto_scale_frame).start()])
    button16.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
    button17 = tk.Button(my_auto_scale_frame, text="Quit",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [root.destroy()])
    button17.grid(row=0, column=2, ipadx=40, ipady=20, padx=0, pady=0)
    button18 = tk.Button(my_auto_scale_frame, text="Off",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [VARIABLE.Mythread.off(self)])
    button18.grid(row=0, column=3, ipadx=40, ipady=20, padx=0, pady=0)
    button19 = tk.Button(my_auto_scale_frame, text="Simulation",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [draw_6(self, elcolor, scale1.get(), scale2.get(),
                                                 scale3.get(), scale4.get(), scale5.get())])
    button19.grid(row=1, column=3, ipadx=40, ipady=20, padx=0, pady=0)
    button20 = tk.Button(my_auto_scale_frame, text="request",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [
                             print("The actual themperature is : {}".format(VARIABLE.Mythread.read(self)[0])),
                             print("The actual order is : {}".format(VARIABLE.Mythread.read(self)[1]))])
    button20.grid(row=2, column=3, ipadx=40, ipady=20, padx=0, pady=0)
    scale1 = Scale(my_auto_scale_frame, orient='vertical', troughcolor=elcolor, from_=120, to=-40,
                   resolution=1, tickinterval=20, length=100, command=0,
                   label='temperature_min', state="active")
    scale1.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    scale1.set(-1)
    scale2 = Scale(my_auto_scale_frame, orient='vertical', troughcolor=elcolor, from_=120, to=-40,
                   resolution=1, tickinterval=20, length=100, command=0,
                   label='temperature_max', state="active")
    scale2.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    scale2.set(1)
    scale4 = Scale(my_auto_scale_frame, orient='horizontal', troughcolor=elcolor, from_=0, to=20,
                   resolution=1, tickinterval=20, length=100, command=0,
                   label='temperature_min_duration_h', state="active")
    scale4.grid(row=2, column=1, ipadx=30, ipady=0, padx=0, pady=0)
    scale4.set(1)
    scale5 = Scale(my_auto_scale_frame, orient='horizontal', troughcolor=elcolor, from_=0, to=20,
                   resolution=1, tickinterval=20, length=100, command=0,
                   label='temperature_max_duration_h', state="active")
    scale5.grid(row=1, column=1, ipadx=30, ipady=0, padx=0, pady=0)
    scale5.set(1)
    scale3 = Scale(my_auto_scale_frame, orient='horizontal', troughcolor=elcolor, from_=1, to=20,
                   resolution=1, tickinterval=5, length=100, command=0,
                   label='number_of_cycles', state="active", relief="flat")
    scale3.grid(row=2, column=2, ipadx=30, ipady=0, padx=0, pady=0)
    scale3.set(1)
    button12 = tk.Button(my_scale_frame, text="Request",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: print("The actual temperature is : {}\nThe actual order is : {}".format
                                               (VARIABLE.Mythread.read(self)[0], VARIABLE.Mythread.read(self)[1])))

    button12.pack(padx=1, pady=1, expand=True, fill="both", side=LEFT)
    scale_root_1 = Scale(my_scale_frame, orient='vertical', troughcolor=elcolor, from_=80, to=-40,
                         resolution=1, tickinterval=20, length=100,
                         label='Order', command=lambda x: [VARIABLE.Mythread.order(self, scale_root_1)], state="active")
    scale_root_1.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    scale_root_3 = Scale(my_scale_frame, orient='vertical', troughcolor=elcolor, from_=10, to=0.1,
                         resolution=0.1, tickinterval=1, length=100, command=0,
                         label='delay in second', state="active")
    scale_root_3.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    scale_root_3.set(5)
    button13 = tk.Button(my_button_frame, text="Start",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [eldraw2(scale_root_3)[0].resume(), eldraw2(scale_root_3)[1].resume(),
                                          button14.pack(padx=1, pady=1, expand=True, fill="both", side=TOP),
                                          button15.pack(padx=1, pady=1, expand=True, fill="both", side=TOP),
                                          ])
    button13.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    button14 = tk.Button(my_button_frame, text="Stop",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [ani.pause(), ani2.pause()])
    button14.pack_forget()
    button15 = tk.Button(my_button_frame, text="Resume",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [ani.resume(), ani2.resume()])
    button15.pack_forget()
    button11 = tk.Button(my_button_frame, text="Quit",
                         borderwidth=8, background=elcolor,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [root.destroy(), root.quit()])
    button11.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    rb2 = tk.Radiobutton(my_rb_frame, text="Automatic",
                         variable=b, value=1, cursor="right_ptr",
                         indicatoron=1, command=lambda: [my_scale_frame.pack_forget(),
                                                         my_auto_scale_frame.pack(padx=0, pady=0,
                                                                                  expand=True, fill="both", side=LEFT),
                                                         my_button_frame.pack_forget(), display()])
    rb2.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    rb1 = tk.Radiobutton(my_rb_frame, text="Manual",
                         variable=b, value=0, cursor="right_ptr",
                         indicatoron=1, command=lambda: [my_scale_frame.pack(padx=0, pady=0,
                                                                             expand=True, fill="both", side=LEFT),
                                                         my_auto_scale_frame.pack_forget(),
                                                         my_button_frame.pack(padx=0, pady=0,
                                                                              expand=True, fill="both", side=RIGHT)])
    rb1.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    rb1.invoke()

    def eldraw2(scale_root_3):
        global ani
        global ani2
        global first_time
        global toolbar
        xar = []
        yar = []

        xar2 = []
        yar2 = []

        style.use('ggplot')
        fig = plt.figure(figsize=(10, 3), dpi=100)

        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_ylim(FRAME)
        line, = ax1.plot(xar, yar, 'r', marker='o')
        line2, = ax1.plot(xar2, yar2, 'b', marker='o')

        def clean():
            global toolbar
            toolbar.pack_forget()

        def init():
            line.set_ydata(np.ma.array(xar, mask=True))
            return line,

        def init2():
            line2.set_ydata(np.ma.array(xar2, mask=True))
            return line2,

        def animate(i):
            yar.append(scale_root_1.get())
            xar.append(i)
            line.set_data(xar, yar)
            ax1.set_xlim(0, i + 1)

        def animate2(r):
            value = VARIABLE.Mythread.read(self)[0]
            yar2.append(value)
            xar2.append(r)
            line2.set_data(xar2, yar2)
            ax1.set_xlim(0, r + 1)

        plotcanvas = FigureCanvasTkAgg(fig, root)
        plotcanvas.get_tk_widget().grid(column=0, row=0)

        if first_time == 1:
            first_time = first_time + 1
        elif (first_time % 2) == 0:
            toolbar = NavigationToolbar2Tk(plotcanvas, my_button_frame)
            toolbar.update()
            toolbar.pack(side=BOTTOM, fill=X)
            first_time = first_time + 1
        else:
            clean()
            first_time = first_time + 1

        ani = animation.FuncAnimation(fig, animate, interval=(scale_root_3.get() * 1000), blit=False, init_func=init)
        ani2 = animation.FuncAnimation(fig, animate2, interval=(scale_root_3.get() * 1000), blit=False, init_func=init2)
        return [ani, ani2]

    root.mainloop()


def draw_6(self, elcolor, temperature_min, temperature_max,
           number_of_cycles, temperature_min_duration_h, temperature_max_duration_h):
    root = tk.Toplevel(self)
    root.wm_title("simulation graph")
    my_draw_6_frame_2 = LabelFrame(root)
    my_draw_6_frame_2.pack()
    my_draw_6_frame_1 = LabelFrame(root)
    my_draw_6_frame_1.pack(side=BOTTOM)
    data = {}
    data[0] = 0
    temperature_max_duration_h = temperature_max_duration_h + 1
    temperature_min_duration_h = temperature_min_duration_h + 1
    var = 1
    for p in range(0, number_of_cycles):
        for i in range(var, temperature_max_duration_h + var):
            data[i] = temperature_max
        for i in range(temperature_max_duration_h + var,
                       temperature_max_duration_h + temperature_min_duration_h +
                       var):
            data[i] = temperature_min
        var = var + temperature_max_duration_h + temperature_min_duration_h

    print(data)
    names = list(data.keys())
    values = list(data.values())
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot().plot(names, values)
    canvas = FigureCanvasTkAgg(fig, master=my_draw_6_frame_1)
    toolbar = NavigationToolbar2Tk(canvas, my_draw_6_frame_1, pack_toolbar=False)
    toolbar.update()
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar.pack(side=BOTTOM, fill=X)
    button1 = Button(master=my_draw_6_frame_2, text="Quit", background=elcolor,
                     cursor="right_ptr", borderwidth=5, activebackground="green",
                     overrelief="sunken", command=lambda: root.destroy())
    button1.pack(side=RIGHT)
    label = tk.Label(my_draw_6_frame_2, text="The value of the time duration of "
                                             "the transition between two level of temperature "
                                             "was arbitrarly fixed to one hour", bg="white", font="arial",
                     fg="black", relief="groove")
    label.pack()


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
    ====================================================================
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
