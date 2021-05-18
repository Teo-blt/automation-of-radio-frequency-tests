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
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import tkinter as tk
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from Climate_chamber_control import Climate_chamber_V2
from Coroutines_experiment import Coroutines_with_asyncio_V2
from loguru import logger

# =============================================================================
VARIABLE = Coroutines_with_asyncio_V2
FRAME = (-50, 90)


def draw_4(self, the_color):  # The function draw_4 crate a new window with a graph inside
    # of it, the graph can be modify in real time, I did not use this idea for the simulation graph because the user
    # can too easily break the program (by playing too fast with the cursor for example
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

    def the_draw():
        global my_scale_frame_1
        global first_time
        if first_time == 1:
            create()
            first_time = 2
        else:
            clean()
            create()

    def enter(event):
        the_draw()

    a = IntVar()
    f = IntVar()
    root.bind("<Return>", enter)

    scale1 = Scale(my_scale_frame_2, orient='vertical', variable=a, from_=100, to=0,
                   resolution=1, tickinterval=25, length=100, troughcolor=the_color,
                   command=lambda x: the_draw(),
                   label='amplitude', state="active")
    scale1.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale1.set(1)
    amplitude = Entry(my_scale_frame_2, validate="all", textvariable=a)
    amplitude.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale2 = Scale(my_scale_frame_2, orient='vertical', variable=f, from_=10, to=0,
                   resolution=1, tickinterval=1, length=100, troughcolor=the_color,
                   command=lambda x: the_draw(),
                   label='frequency', state="active")
    scale2.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    scale2.set(1)
    frequency = Entry(my_scale_frame_2, validate="all", textvariable=f)
    frequency.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    button1 = Button(master=my_scale_frame_2, text="Quit", background=the_color, command=lambda: root.destroy())
    button1.pack(side=LEFT)


def draw_5(self, the_color, port):
    def display():
        style.use('ggplot')
        fig = plt.figure(figsize=(9, 4), dpi=100)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_ylim(-40, 120)
        plot_canvas = FigureCanvasTkAgg(fig, root)
        plot_canvas.get_tk_widget().grid(column=0, row=0)

    def verification_temp():
        if temperature_min_scale.get() >= temperature_max_scale.get():
            logger.critical(f"Error temperature_min_scale : {temperature_min_scale.get()} "
                            f">=  temperature_max_scale : {temperature_max_scale.get()}")
        else:
            VARIABLE.Thread(port, temperature_min_scale.get(), temperature_max_scale.get(),
                            temperature_min_duration_h_scale.get(),
                            temperature_max_duration_h_scale.get(),
                            number_of_cycles_scale.get(), 0, auto_scale_frame, a.get(), 0,
                            0, 0).start()

    global ani
    global ani2
    global first_time
    first_time = 1
    a = IntVar()
    b = IntVar()
    c = IntVar()
    root = tk.Toplevel(self)
    root.title('Draw window')
    root.config(background='#fafafa')

    settings_frame = LabelFrame(root, text="Settings")
    settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    settings_frame.config(background='#fafafa')

    scale_frame = LabelFrame(settings_frame, bd=0)  # , text="Scales"
    scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    scale_frame.config(background='#fafafa')

    auto_scale_frame = LabelFrame(settings_frame, bd=0)  # , text="auto_scale_frame"
    auto_scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    auto_scale_frame.config(background='#fafafa')

    auto_stair_scale_frame = LabelFrame(settings_frame, bd=0)  # , text="auto_scale_frame"
    auto_stair_scale_frame.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    auto_stair_scale_frame.config(background='#fafafa')

    button_frame = LabelFrame(root, bd=0)  # , text="Buttons"
    button_frame.grid(column=1, row=0)
    button_frame.config(background='#fafafa')

    rb_frame_mode_selection = LabelFrame(settings_frame, bd=0)  # , text="Choice"
    rb_frame_mode_selection.pack(padx=0, pady=0, expand=True, fill="both", side=RIGHT)
    rb_frame_mode_selection.config(background='#fafafa')

    rb_frame_automatic_selection = LabelFrame(settings_frame, bd=0)  # , text="Choice"
    rb_frame_automatic_selection.pack(padx=0, pady=0, expand=True, fill="both", side=RIGHT)
    rb_frame_automatic_selection.config(background='#fafafa')

    display()
    cyclic_label = tk.Label(auto_scale_frame, text="Cyclic automating", bg="white", font="arial",
                            fg="black", relief="groove")
    cyclic_label.grid(row=0, column=0, ipadx=20, ipady=20, padx=0, pady=0)
    step_label = tk.Label(auto_stair_scale_frame, text="Automation by step", bg="white", font="arial",
                          fg="black", relief="groove")
    step_label.grid(row=0, column=0, ipadx=20, ipady=20, padx=0, pady=0)
    start_button = tk.Button(
        auto_scale_frame,
        text="Start",
        borderwidth=8,
        background=the_color,
        activebackground="green",
        cursor="right_ptr",
        overrelief="sunken",
        command=lambda: [verification_temp()])
    start_button.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)

    off_auto_scale_frame_button = tk.Button(auto_scale_frame, text="Off",
                                            borderwidth=8, background=the_color,
                                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                                            command=lambda: [VARIABLE.off()])
    off_auto_scale_frame_button.grid(row=0, column=2, ipadx=40, ipady=20, padx=0, pady=0)
    simulation_auto_scale_frame_button = tk.Button(auto_scale_frame, text="Simulation",
                                                   borderwidth=8, background=the_color,
                                                   activebackground="green", cursor="right_ptr", overrelief="sunken",
                                                   command=lambda: [draw_6(self, the_color, temperature_min_scale.get(),
                                                                           temperature_max_scale.get(),
                                                                           number_of_cycles_scale.get(),
                                                                           temperature_min_duration_h_scale.get(),
                                                                           temperature_max_duration_h_scale.get(),
                                                                           a.get())])
    simulation_auto_scale_frame_button.grid(row=2, column=3, ipadx=40, ipady=20, padx=0, pady=0)
    request_auto_scale_frame_button = tk.Button(auto_scale_frame, text="request",
                                                borderwidth=8, background=the_color,
                                                activebackground="green", cursor="right_ptr", overrelief="sunken",
                                                command=lambda: [
                                                    logger.info("The actual temperature is : {}".format(
                                                        VARIABLE.Thread.read(self)[0])),
                                                    logger.info("The actual order is : {}".format(
                                                        VARIABLE.Thread.read(self)[1]))])
    request_auto_scale_frame_button.grid(row=0, column=3, ipadx=40, ipady=20, padx=0, pady=0)

    temperature_min_scale = Scale(auto_scale_frame, orient='vertical', troughcolor=the_color, from_=80, to=-40,
                                  resolution=1, tickinterval=20, length=100, command=0,
                                  label='Temperature min', state="active")
    temperature_min_scale.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    temperature_min_scale.set(-1)

    temperature_max_scale = Scale(auto_scale_frame, orient='vertical', troughcolor=the_color, from_=80, to=-40,
                                  resolution=1, tickinterval=20, length=100, command=0,
                                  label='Temperature max', state="active")
    temperature_max_scale.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    temperature_max_scale.set(1)
    temperature_min_duration_h_scale = Scale(auto_scale_frame, orient='horizontal', troughcolor=the_color, from_=0,
                                             to=20,
                                             resolution=1, tickinterval=20, length=100, command=0,
                                             label='Temperature min duration h', state="active")
    temperature_min_duration_h_scale.grid(row=2, column=1, ipadx=30, ipady=0, padx=0, pady=0)
    temperature_min_duration_h_scale.set(1)
    temperature_max_duration_h_scale = Scale(auto_scale_frame, orient='horizontal', troughcolor=the_color, from_=0,
                                             to=20,
                                             resolution=1, tickinterval=20, length=100, command=0,
                                             label='Temperature max duration h', state="active")
    temperature_max_duration_h_scale.grid(row=1, column=1, ipadx=30, ipady=0, padx=0, pady=0)
    temperature_max_duration_h_scale.set(1)
    number_of_cycles_scale = Scale(auto_scale_frame, orient='horizontal', troughcolor=the_color, from_=1, to=20,
                                   resolution=1, tickinterval=5, length=100, command=0,
                                   label='Number of cycles', state="active", relief="flat")
    number_of_cycles_scale.grid(row=2, column=2, ipadx=30, ipady=0, padx=0, pady=0)
    number_of_cycles_scale.set(1)
    request_scale_frame_button = tk.Button(scale_frame, text="Request",
                                           borderwidth=8, background=the_color,
                                           activebackground="green", cursor="right_ptr", overrelief="sunken",
                                           command=lambda: [logger.info("The actual temperature is : {}".format
                                                                        (VARIABLE.Thread.read(self)[0])),
                                                            logger.info("The actual order is : {}".format
                                                                        (VARIABLE.Thread.read(self)[1]))])

    request_scale_frame_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    order_scale = Scale(scale_frame, orient='vertical', troughcolor=the_color, from_=80, to=-40,
                        resolution=1, tickinterval=20, length=100,
                        label='Order', command=lambda x: [], state="active")
    order_scale.pack(padx=0, pady=0, expand=True, fill="both", side=LEFT)
    send_button = tk.Button(scale_frame, text="Send",
                            borderwidth=8, background=the_color,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [VARIABLE.Thread.order(self, order_scale.get())])
    send_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    off_scale_frame_button = tk.Button(scale_frame, text="Off",
                                       borderwidth=8, background=the_color,
                                       activebackground="green", cursor="right_ptr", overrelief="sunken",
                                       command=lambda: [VARIABLE.off()])
    off_scale_frame_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    graphic_settings_label = tk.Label(button_frame, text="Graphic settings", bg="white", font="arial",
                                      fg="black", relief="groove")
    graphic_settings_label.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    start_button_frame_button = tk.Button(button_frame, text="Start",
                                          borderwidth=8, background=the_color,
                                          activebackground="green", cursor="right_ptr", overrelief="sunken",
                                          command=lambda: [the_draw2()[0].resume(), the_draw2()[1].resume(),
                                                           stop_button_frame_button.pack(padx=1, pady=1, expand=True,
                                                                                         fill="both",
                                                                                         side=TOP),
                                                           resume_button_frame_button.pack(padx=1, pady=1, expand=True,
                                                                                           fill="both",
                                                                                           side=TOP),
                                                           ])
    start_button_frame_button.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    stop_button_frame_button = tk.Button(button_frame, text="Stop",
                                         borderwidth=8, background=the_color,
                                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                                         command=lambda: [ani.pause(), ani2.pause()])
    stop_button_frame_button.pack_forget()
    resume_button_frame_button = tk.Button(button_frame, text="Resume",
                                           borderwidth=8, background=the_color,
                                           activebackground="green", cursor="right_ptr", overrelief="sunken",
                                           command=lambda: [ani.resume(), ani2.resume()])
    resume_button_frame_button.pack_forget()
    quit_button_frame_button = tk.Button(button_frame, text="Quit",
                                         borderwidth=8, background=the_color,
                                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                                         command=lambda: [root.destroy(), root.quit()])
    quit_button_frame_button.pack(padx=1, pady=1, expand=True, fill="both", side=TOP)
    radiobutton_automatic = tk.Radiobutton(rb_frame_mode_selection, text="Automatic",
                                           variable=b, value=1, cursor="right_ptr",
                                           indicatoron=1,
                                           command=lambda: [scale_frame.pack_forget(),
                                                            auto_scale_frame.pack(padx=0, pady=0,
                                                                                  expand=True,
                                                                                  fill="both",
                                                                                  side=LEFT),
                                                            button_frame.pack_forget(),
                                                            rb_frame_automatic_selection.pack(padx=0,
                                                                                              pady=0,
                                                                                              expand=True,
                                                                                              fill="both",
                                                                                              side=RIGHT),
                                                            radiobutton_cycle.invoke()])
    radiobutton_automatic.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    radiobutton_manual = tk.Radiobutton(rb_frame_mode_selection, text="Manual",
                                        variable=b, value=0, cursor="right_ptr",
                                        indicatoron=1, command=lambda: [scale_frame.pack(padx=0, pady=0,
                                                                                         expand=True, fill="both",
                                                                                         side=LEFT),
                                                                        auto_scale_frame.pack_forget(),
                                                                        button_frame.grid(column=1, row=0),
                                                                        rb_frame_automatic_selection.pack_forget(),
                                                                        auto_stair_scale_frame.pack_forget()])
    radiobutton_manual.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    radiobutton_manual.invoke()
    radiobutton_start_with_high_temp = tk.Radiobutton(auto_scale_frame, text="Start with high temp",
                                                      variable=a, value=0, cursor="right_ptr",
                                                      indicatoron=0, command=lambda: [], background=the_color,
                                                      activebackground="green",
                                                      bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_start_with_high_temp.grid(row=1, column=2, ipadx=10, ipady=10, padx=0, pady=0)
    radiobutton_start_with_low_temp = tk.Radiobutton(auto_scale_frame, text="Start with low temp",
                                                     variable=a, value=1, cursor="right_ptr",
                                                     indicatoron=0, command=lambda: [], background=the_color,
                                                     activebackground="green",
                                                     bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_start_with_low_temp.grid(row=1, column=3, ipadx=10, ipady=10, padx=0, pady=0)
    radiobutton_start_with_low_temp.invoke()
    radiobutton_stair = tk.Radiobutton(rb_frame_automatic_selection, text="Stair",
                                       variable=c, value=1, cursor="right_ptr",
                                       indicatoron=1, command=lambda: [auto_scale_frame.pack_forget(),
                                                                       auto_stair_scale_frame.pack(padx=0, pady=0,
                                                                                                   expand=True,
                                                                                                   fill="both",
                                                                                                   side=LEFT)])
    radiobutton_stair.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    radiobutton_cycle = tk.Radiobutton(rb_frame_automatic_selection, text="Cycle",
                                       variable=c, value=0, cursor="right_ptr",
                                       indicatoron=1, command=lambda: [auto_scale_frame.pack(padx=0, pady=0,
                                                                                             expand=True, fill="both",
                                                                                             side=LEFT),
                                                                       auto_stair_scale_frame.pack_forget()])
    radiobutton_cycle.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    start_auto_stair_scale_frame_button = tk.Button(auto_stair_scale_frame, text="Start",
                                                    borderwidth=8, background=the_color,
                                                    activebackground="green", cursor="right_ptr", overrelief="sunken",
                                                    command=lambda: [VARIABLE.Thread(
                                                        port,
                                                        temperature_start_auto_stair_scale_frame_scale.get(),
                                                        temperature_start_auto_stair_scale_frame_scale.get(),
                                                        temperature_duration_h_auto_stair_scale_frame_scale.get(),
                                                        temperature_duration_h_auto_stair_scale_frame_scale.get(),
                                                        0, 0, auto_scale_frame, 0,
                                                        c.get(),
                                                        step_auto_stair_scale_frame_scale.get(),
                                                        temperature_end_auto_stair_scale_frame_scale.get()).start()])
    start_auto_stair_scale_frame_button.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
    off_auto_stair_scale_frame_button = tk.Button(auto_stair_scale_frame, text="Off",
                                                  borderwidth=8, background=the_color,
                                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                                  command=lambda: [VARIABLE.off()])
    off_auto_stair_scale_frame_button.grid(row=0, column=2, ipadx=40, ipady=20, padx=20, pady=20)
    simulation_auto_stair_scale_frame_button = tk.Button(auto_stair_scale_frame, text="Simulation",
                                                         borderwidth=8, background=the_color,
                                                         activebackground="green", cursor="right_ptr",
                                                         overrelief="sunken",
                                                         command=lambda:
                                                         [draw_7(
                                                             self,
                                                             the_color,
                                                             step_auto_stair_scale_frame_scale.get(),
                                                             temperature_start_auto_stair_scale_frame_scale.get(),
                                                             temperature_end_auto_stair_scale_frame_scale.get(),
                                                             temperature_duration_h_auto_stair_scale_frame_scale.get())])
    simulation_auto_stair_scale_frame_button.grid(row=1, column=3, ipadx=40, ipady=20, padx=0, pady=0)
    request_auto_stair_scale_frame_button = tk.Button(auto_stair_scale_frame, text="Request",
                                                      borderwidth=8, background=the_color,
                                                      activebackground="green", cursor="right_ptr", overrelief="sunken",
                                                      command=lambda: [
                                                          logger.info("The actual temperature is : {}".format(
                                                              VARIABLE.Thread.read(self)[0])),
                                                          logger.info("The actual order is : {}".format(
                                                              VARIABLE.Thread.read(self)[1]))])
    request_auto_stair_scale_frame_button.grid(row=0, column=3, ipadx=40, ipady=20, padx=0, pady=0)
    step_auto_stair_scale_frame_scale = Scale(auto_stair_scale_frame, orient='vertical', troughcolor=the_color,
                                              from_=120, to=1,
                                              resolution=1, tickinterval=20, length=100, command=0,
                                              label='Step', state="active")
    step_auto_stair_scale_frame_scale.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    step_auto_stair_scale_frame_scale.set(1)
    temperature_start_auto_stair_scale_frame_scale = Scale(auto_stair_scale_frame, orient='vertical',
                                                           troughcolor=the_color, from_=80, to=-40,
                                                           resolution=1, tickinterval=20, length=100, command=0,
                                                           label='Temperature start', state="active")
    temperature_start_auto_stair_scale_frame_scale.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    temperature_duration_h_auto_stair_scale_frame_scale = Scale(auto_stair_scale_frame, orient='horizontal',
                                                                troughcolor=the_color, from_=1, to=20,
                                                                resolution=1, tickinterval=20, length=100, command=0,
                                                                label='Temperature duration h', state="active")
    temperature_duration_h_auto_stair_scale_frame_scale.grid(row=1, column=1, ipadx=30, ipady=0, padx=0, pady=0)
    temperature_duration_h_auto_stair_scale_frame_scale.set(1)
    temperature_end_auto_stair_scale_frame_scale = Scale(auto_stair_scale_frame, orient='vertical',
                                                         troughcolor=the_color, from_=80, to=-40,
                                                         resolution=1, tickinterval=20, length=100, command=0,
                                                         label='Temperature end', state="active", relief="flat")
    temperature_end_auto_stair_scale_frame_scale.grid(row=2, column=1, ipadx=30, ipady=0, padx=0, pady=0)

    def the_draw2() -> [FuncAnimation, FuncAnimation]:
        global ani
        global ani2
        global first_time
        global toolbar
        xar = []
        yar = []

        xar2 = []
        yar2 = []

        style.use('ggplot')
        fig = plt.figure(figsize=(9, 4), dpi=100)

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
            global value
            value = VARIABLE.Thread.read(self)
            yar.append(value[1])
            xar.append(i * (1 / 12))
            line.set_data(xar, yar)
            ax1.set_xlim(0, i * (1 / 12) + 1)

        def animate2(r):
            global m, M, value
            yar2.append(value[0])
            xar2.append(r * (1 / 12))
            line2.set_data(xar2, yar2)
            ax1.set_xlim(0, r * (1 / 12) + 1)
            if r == 0:
                m = min(value)
                M = max(value)
            if min(value) < m:
                m = min(value)
            if max(value) > M:
                M = max(value)
            ax1.set_ylim(m - 1, M + 1)

        plot_canvas = FigureCanvasTkAgg(fig, root)
        plot_canvas.get_tk_widget().grid(column=0, row=0)

        if first_time == 1:
            first_time = first_time + 1
        elif (first_time % 2) == 0:
            toolbar = NavigationToolbar2Tk(plot_canvas, button_frame)
            toolbar.update()
            toolbar.pack(side=BOTTOM, fill=X)
            first_time = first_time + 1
        else:
            clean()
            first_time = first_time + 1

        ani = animation.FuncAnimation(fig, animate, interval=5000, blit=False, init_func=init)
        ani2 = animation.FuncAnimation(fig, animate2, interval=5000, blit=False, init_func=init2)

        return [ani, ani2]

    root.mainloop()


def draw_6(self, the_color, temperature_min, temperature_max,
           number_of_cycles, temperature_min_duration_h, temperature_max_duration_h, min_max):

    if temperature_min >= temperature_max:
        logger.critical(f"Error temperature_min_scale : {temperature_min} "
                        f">=  temperature_max_scale : {temperature_max}")
    else:
        root = tk.Toplevel(self)
        root.wm_title("simulation graph")
        my_draw_6_frame_2 = LabelFrame(root)
        my_draw_6_frame_2.pack()
        my_draw_6_frame_1 = LabelFrame(root)
        my_draw_6_frame_1.pack(side=BOTTOM)
        data = {0: 0}
        temperature_max_duration_h = temperature_max_duration_h + 1
        temperature_min_duration_h = temperature_min_duration_h + 1
        var = 1
        if min_max:
            var_storage = temperature_max
            temperature_max = temperature_min
            temperature_min = var_storage
        for p in range(0, number_of_cycles):
            for i in range(var, temperature_max_duration_h + var):
                data[i] = temperature_max
            for i in range(temperature_max_duration_h + var,
                           temperature_max_duration_h + temperature_min_duration_h +
                           var):
                data[i] = temperature_min
            var = var + temperature_max_duration_h + temperature_min_duration_h

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
        button1 = Button(master=my_draw_6_frame_2, text="Quit", background=the_color,
                         cursor="right_ptr", borderwidth=5, activebackground="green",
                         overrelief="sunken", command=lambda: root.destroy())
        button1.pack(side=RIGHT)
        label = tk.Label(my_draw_6_frame_2, text="The value of the time duration of "
                                                 "the transition between two level of temperature "
                                                 "was arbitrarily fixed to one hour", bg="white", font="arial",
                         fg="black", relief="groove")
        label.pack()


def draw_7(self, the_color, step, temp_start, temp_end, temp_duration):
    root = tk.Toplevel(self)
    root.wm_title("simulation graph")
    my_draw_7_frame_2 = LabelFrame(root)
    my_draw_7_frame_2.pack()
    my_draw_7_frame_1 = LabelFrame(root)
    my_draw_7_frame_1.pack(side=BOTTOM)
    data = {0: 0}
    var = 0
    temp_duration = temp_duration + 1
    if temp_start >= step:
        step = -step
    while abs(temp_start - temp_end) != 0:
        for i in range(var, temp_duration + var):
            data[i] = temp_start
        var = var + temp_duration
        temp_start = temp_start + step
    for i in range(var, temp_duration + var):
        data[i] = temp_start
    names = list(data.keys())
    values = list(data.values())
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.add_subplot().plot(names, values)
    canvas = FigureCanvasTkAgg(fig, master=my_draw_7_frame_1)
    toolbar = NavigationToolbar2Tk(canvas, my_draw_7_frame_1, pack_toolbar=False)
    toolbar.update()
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar.pack(side=BOTTOM, fill=X)
    button1 = Button(master=my_draw_7_frame_2, text="Quit", background=the_color,
                     cursor="right_ptr", borderwidth=5, activebackground="green",
                     overrelief="sunken", command=lambda: root.destroy())
    button1.pack(side=RIGHT)
    label = tk.Label(my_draw_7_frame_2, text="The value of the time duration of "
                                             "the transition between two level of temperature "
                                             "was arbitrarily fixed to one hour", bg="white", font="arial",
                     fg="black", relief="groove")
    label.pack()
