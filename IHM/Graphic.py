#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: April 23 16:15:00 2021
# For Kerlink, all rights reserved
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
from tkinter.messagebox import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from loguru import logger
from IHM_piloting.Climate_chamber import Climate_chamber_script

# =============================================================================
VARIABLE = Climate_chamber_script
FRAME = (-50, 90)
THE_COLOR = "#E76145"


def live_graph(self):  # The function live_graph crate a new window with a graph inside
    # of it, the graph can be modify in real time, I did not use this idea for the simulation graph because the user
    # can too easily break the program (by playing too fast with the cursor for example
    global live_graph_frame
    global first_time
    first_time = 1
    root = tk.Toplevel(self)
    root.wm_title("Embedding in Tk")
    live_graph_scale_frame = LabelFrame(root)
    live_graph_scale_frame.pack()

    def clean():
        global live_graph_frame
        live_graph_frame.destroy()

    def create():
        global live_graph_frame
        live_graph_frame = LabelFrame(root)
        live_graph_frame.pack(side=BOTTOM)
        t = np.arange(0, 3, .01)
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot().plot(t, amplitude_live_graph_scale_frame.get() *
                               np.sin(frequency_live_graph_scale_frame.get() * np.pi * t))
        canvas = FigureCanvasTkAgg(fig, master=live_graph_frame)
        toolbar = NavigationToolbar2Tk(canvas, live_graph_frame, pack_toolbar=False)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        toolbar.pack(side=BOTTOM, fill=X)

    def the_draw():
        global live_graph_frame
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

    amplitude_live_graph_scale_frame = Scale(live_graph_scale_frame, orient='vertical', variable=a, from_=100, to=0,
                                             resolution=1, tickinterval=25, length=100, troughcolor=THE_COLOR,
                                             command=lambda x: the_draw(),
                                             label='Amplitude', state="active")
    amplitude_live_graph_scale_frame.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    amplitude_live_graph_scale_frame.set(1)
    amplitude_entry = Entry(live_graph_scale_frame, validate="all", textvariable=a)
    amplitude_entry.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    frequency_live_graph_scale_frame = Scale(live_graph_scale_frame, orient='vertical', variable=f, from_=10, to=0,
                                             resolution=1, tickinterval=1, length=100, troughcolor=THE_COLOR,
                                             command=lambda x: the_draw(),
                                             label='Frequency', state="active")
    frequency_live_graph_scale_frame.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    frequency_live_graph_scale_frame.set(1)
    frequency_entry = Entry(live_graph_scale_frame, validate="all", textvariable=f)
    frequency_entry.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)
    quit_live_graph_scale_frame_button = Button(master=live_graph_scale_frame, text="Quit", background=THE_COLOR,
                                                command=lambda: root.destroy())
    quit_live_graph_scale_frame_button.pack(side=LEFT)


def main_graphic_climatic_chamber(self, port):
    global color_button

    def state_graph(state):
        global color_button
        if state == 1:
            color_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
            color_button.config(text="The animation in paused")
            color_button.config(bg="red", disabledforeground="black")
        else:
            color_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
            color_button.config(text="The animation in active")
            color_button.config(bg="light green", disabledforeground="black")

    def display():
        style.use('ggplot')
        fig = plt.figure(figsize=(10, 5), dpi=100)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_ylim(-40, 120)
        plot_canvas = FigureCanvasTkAgg(fig, root)
        plot_canvas.get_tk_widget().grid(column=0, row=0)

    def send_verification(x):
        global graph_lunch
        if x:
            graph_lunch = 0
        else:
            graph_lunch = graph_lunch + 1
            if graph_lunch == 1:
                start_button_frame_button.invoke()
            else:
                pass

    def quit_graph():
        global ani
        global ani2
        try:
            ani.pause()
            ani2.pause()
            state_graph(1)
        except:
            start_button_frame_button.invoke()
            ani.pause()
            ani2.pause()
            state_graph(1)

    def verification_temp():
        global high_low
        if temperature_min_scale.get() > temperature_max_scale.get():
            logger.critical(f"Error temperature_min_scale : {temperature_min_scale.get()} "
                            f">  temperature_max_scale : {temperature_max_scale.get()}")
            showerror("Value Error", f"Error temperature_min_scale : {temperature_min_scale.get()} "
                                     f">  temperature_max_scale : {temperature_max_scale.get()}")
        else:
            start_button_frame_button.invoke()
            VARIABLE.Thread(port, temperature_min_scale.get(), temperature_max_scale.get(),
                            temperature_min_duration_h_scale.get(),
                            temperature_max_duration_h_scale.get(),
                            number_of_cycles_scale.get(), 0, auto_scale_frame, high_low, 0,
                            0, 0, ani, ani2, state_graph).start()
            state_graph(0)

    global ani
    global ani2
    global first_time
    global graph_lunch
    global high_low
    global stair_cycle
    graph_lunch = 0
    first_time = 1

    a = IntVar()
    b = IntVar()
    c = IntVar()

    new_window_main_graphic = Tk()
    new_window_main_graphic.title("Climatic chamber settings")
    new_window_main_graphic.config(background='#fafafa')

    root = Tk()
    root.title('Graph window')
    root.config(background='#fafafa')

    display()

    settings_frame = LabelFrame(new_window_main_graphic, text="Settings")
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

    rb_frame_automatic_selection = LabelFrame(settings_frame, bd=0)  # , text="Choice"
    rb_frame_automatic_selection.pack(padx=0, pady=0, expand=True, fill="both", side=RIGHT)
    rb_frame_automatic_selection.config(background='#fafafa')

    rb_frame_mode_selection = LabelFrame(settings_frame, bd=0)  # , text="Choice"
    rb_frame_mode_selection.pack(padx=0, pady=0, expand=True, fill="both", side=RIGHT)
    rb_frame_mode_selection.config(background='#fafafa')

    cyclic_label = tk.Label(auto_scale_frame, text="Cyclic automating", bg="white", font="arial",
                            fg="black", relief="groove")
    cyclic_label.grid(row=0, column=0, ipadx=20, ipady=20, padx=0, pady=0)
    step_label = tk.Label(auto_stair_scale_frame, text="Automation by step", bg="white", font="arial",
                          fg="black", relief="groove")
    step_label.grid(row=0, column=0, ipadx=20, ipady=20, padx=0, pady=0)

    start_button = tk.Button(auto_scale_frame, text="Start", borderwidth=8, background=THE_COLOR,
                             activebackground="green", cursor="right_ptr", overrelief="sunken",
                             command=lambda: [verification_temp()])
    start_button.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)

    off_auto_scale_frame_button = tk.Button(auto_scale_frame, text="Stop",
                                            borderwidth=8, background=THE_COLOR,
                                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                                            command=lambda: [quit_graph(),
                                                             VARIABLE.off(port)])
    off_auto_scale_frame_button.grid(row=0, column=2, ipadx=40, ipady=20, padx=0, pady=0)

    temperature_min_scale = Scale(auto_scale_frame, orient='vertical', troughcolor=THE_COLOR, from_=80, to=-40,
                                  resolution=1, tickinterval=20, length=100, command=lambda x: [create_cycle()],
                                  label='Temperature min (°C)', state="active")
    temperature_min_scale.grid(row=2, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    temperature_min_scale.set(-1)

    temperature_max_scale = Scale(auto_scale_frame, orient='vertical', troughcolor=THE_COLOR, from_=80, to=-40,
                                  resolution=1, tickinterval=20, length=100, command=lambda x: [create_cycle()],
                                  label='Temperature max (°C)', state="active")
    temperature_max_scale.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    temperature_max_scale.set(1)
    temperature_min_duration_h_scale = Scale(auto_scale_frame, orient='horizontal', troughcolor=THE_COLOR, from_=1,
                                             to=20,
                                             resolution=1, tickinterval=4, length=100,
                                             command=lambda x: [create_cycle()],
                                             label='Temperature min duration (H)', state="active")
    temperature_min_duration_h_scale.grid(row=2, column=1, ipadx=35, ipady=0, padx=0, pady=0)
    temperature_min_duration_h_scale.set(1)
    temperature_max_duration_h_scale = Scale(auto_scale_frame, orient='horizontal', troughcolor=THE_COLOR, from_=1,
                                             to=20,
                                             resolution=1, tickinterval=4, length=100,
                                             command=lambda x: [create_cycle()],
                                             label='Temperature max duration (H)', state="active")
    temperature_max_duration_h_scale.grid(row=1, column=1, ipadx=35, ipady=0, padx=0, pady=0)
    temperature_max_duration_h_scale.set(1)
    number_of_cycles_scale = Scale(auto_scale_frame, orient='horizontal', troughcolor=THE_COLOR, from_=1, to=21,
                                   resolution=1, tickinterval=5, length=100,
                                   command=lambda x: [create_cycle()],
                                   label='Number of cycles', state="active", relief="flat")
    number_of_cycles_scale.grid(row=2, column=2, ipadx=30, ipady=0, padx=0, pady=0)
    number_of_cycles_scale.set(1)
    request_scale_frame_button = tk.Button(scale_frame, text="Request",
                                           borderwidth=8, background=THE_COLOR,
                                           activebackground="green", cursor="right_ptr", overrelief="sunken",
                                           command=lambda: [logger.info("The actual temperature is : {}".format
                                                                        (VARIABLE.Thread.read(self, port)[0])),
                                                            logger.info("The actual order is : {}".format
                                                                        (VARIABLE.Thread.read(self, port)[1]))])

    request_scale_frame_button.pack(padx=0, pady=0, ipadx=10, ipady=10, expand=False, fill="none", side=RIGHT)
    order_scale = Scale(scale_frame, orient='vertical', troughcolor=THE_COLOR, from_=80, to=-40,
                        resolution=1, tickinterval=20, length=100,
                        label='Order (°C)', command=lambda x: [], state="active")
    order_scale.pack(padx=10, pady=10, ipadx=0, ipady=0, expand=True, fill="both", side=LEFT)
    send_button = tk.Button(scale_frame, text="Send",
                            borderwidth=8, background=THE_COLOR,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [send_verification(0),
                                             VARIABLE.Thread.order(self, order_scale.get())])
    send_button.pack(padx=10, pady=10, ipadx=10, ipady=10, expand=False, fill="none", side=RIGHT)
    off_scale_frame_button = tk.Button(scale_frame, text="Stop",
                                       borderwidth=8, background=THE_COLOR,
                                       activebackground="green", cursor="right_ptr", overrelief="sunken",
                                       command=lambda: [quit_graph(), send_verification(1),
                                                        VARIABLE.off(port)])
    off_scale_frame_button.pack(padx=0, pady=0, ipadx=10, ipady=10, expand=False, fill="none", side=RIGHT)
    graphic_settings_label = tk.Label(button_frame, text="Graphic settings", bg="white", font="arial",
                                      fg="black", relief="groove")
    graphic_settings_label.pack_forget()
    start_button_frame_button = tk.Button(button_frame, text="Start",
                                          borderwidth=8, background=THE_COLOR,
                                          activebackground="green", cursor="right_ptr", overrelief="sunken",
                                          command=lambda: [dot_animation()[0].resume(), dot_animation()[1].resume(),
                                                           graphic_settings_label.pack(padx=1, pady=1, expand=True,
                                                                                       fill="both", side=TOP),
                                                           stop_button_frame_button.pack(padx=1, pady=1, expand=True,
                                                                                         fill="both",
                                                                                         side=TOP),
                                                           resume_button_frame_button.pack(padx=1, pady=1, expand=True,
                                                                                           fill="both",
                                                                                           side=TOP)
                                                           ])
    stop_button_frame_button = tk.Button(button_frame, text="Stop",
                                         borderwidth=8, background=THE_COLOR,
                                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                                         command=lambda: [ani.pause(), ani2.pause(), state_graph(1)])
    stop_button_frame_button.pack_forget()
    resume_button_frame_button = tk.Button(button_frame, text="Resume",
                                           borderwidth=8, background=THE_COLOR,
                                           activebackground="green", cursor="right_ptr", overrelief="sunken",
                                           command=lambda: [ani.resume(), ani2.resume(), state_graph(0)])
    resume_button_frame_button.pack_forget()
    color_button = Button(button_frame, state="disabled")
    color_button.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
    color_button.pack_forget()
    radiobutton_automatic = tk.Radiobutton(rb_frame_mode_selection, text="Automatic",
                                           variable=b, value=1, cursor="right_ptr",
                                           indicatoron=1, font=('Helvetica', '16'),
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
                                                            radiobutton_cycle.invoke(),
                                                            radiobutton_start_with_low_temp.invoke()])
    radiobutton_automatic.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    radiobutton_manual = tk.Radiobutton(rb_frame_mode_selection, text="Manual",
                                        variable=b, value=0, cursor="right_ptr", font=('Helvetica', '16'),
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
                                                      indicatoron=0, command=lambda: [change(0), create_cycle()],
                                                      background=THE_COLOR,
                                                      activebackground="green",
                                                      bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_start_with_high_temp.grid(row=1, column=2, ipadx=10, ipady=10, padx=0, pady=0)
    radiobutton_start_with_low_temp = tk.Radiobutton(auto_scale_frame, text="Start with low temp",
                                                     variable=a, value=1, cursor="right_ptr",
                                                     indicatoron=0, command=lambda: [change(1), create_cycle()],
                                                     background=THE_COLOR,
                                                     activebackground="green",
                                                     bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_start_with_low_temp.grid(row=1, column=3, ipadx=10, ipady=10, padx=0, pady=0)
    radiobutton_stair = tk.Radiobutton(rb_frame_automatic_selection, text="Stair", font=('Helvetica', '16'),
                                       variable=c, value=1, cursor="right_ptr",
                                       indicatoron=1, command=lambda: [auto_scale_frame.pack_forget(),
                                                                       auto_stair_scale_frame.pack(padx=0, pady=0,
                                                                                                   expand=True,
                                                                                                   fill="both",
                                                                                                   side=LEFT),
                                                                       create_stair(), change_2(1)])
    radiobutton_stair.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    radiobutton_cycle = tk.Radiobutton(rb_frame_automatic_selection, text="Cycle",
                                       variable=c, value=0, cursor="right_ptr", font=('Helvetica', '16'),
                                       indicatoron=1, command=lambda: [auto_scale_frame.pack(padx=0, pady=0,
                                                                                             expand=True, fill="both",
                                                                                             side=LEFT),
                                                                       auto_stair_scale_frame.pack_forget(),
                                                                       change_2(0)])
    radiobutton_cycle.pack(padx=0, pady=0, expand=False, fill="none", side=BOTTOM)
    start_auto_stair_scale_frame_button = tk.Button(auto_stair_scale_frame, text="Start",
                                                    borderwidth=8, background=THE_COLOR,
                                                    activebackground="green", cursor="right_ptr", overrelief="sunken",
                                                    command=lambda: [start_button_frame_button.invoke(),
                                                                     VARIABLE.Thread(
                                                                         port,
                                                                         temperature_start_stair_scale.get(),
                                                                         temperature_start_stair_scale.get(),
                                                                         temperature_duration_h_stair_scale.get(),
                                                                         temperature_duration_h_stair_scale.get(),
                                                                         0, 0, auto_scale_frame, 0,
                                                                         stair_cycle,
                                                                         step_auto_stair_scale_frame_scale.get(),
                                                                         temperature_end_auto_stair.get(),
                                                                         ani,
                                                                         ani2, state_graph).start(), state_graph(0)])
    start_auto_stair_scale_frame_button.grid(row=0, column=1, ipadx=40, ipady=20, padx=0, pady=0)
    off_auto_stair_scale_frame_button = tk.Button(auto_stair_scale_frame, text="Stop",
                                                  borderwidth=8, background=THE_COLOR,
                                                  activebackground="green", cursor="right_ptr", overrelief="sunken",
                                                  command=lambda: [quit_graph(), VARIABLE.off(port)])
    off_auto_stair_scale_frame_button.grid(row=0, column=2, ipadx=40, ipady=20, padx=20, pady=20)
    step_auto_stair_scale_frame_scale = Scale(auto_stair_scale_frame, orient='vertical', troughcolor=THE_COLOR,
                                              from_=120, to=1,
                                              resolution=1, tickinterval=20, length=100,
                                              label='Step (°C)', state="active",
                                              command=lambda x: [create_stair()])
    step_auto_stair_scale_frame_scale.grid(row=1, column=0, ipadx=10, ipady=10, padx=30, pady=0)
    step_auto_stair_scale_frame_scale.set(1)
    temperature_start_stair_scale = Scale(auto_stair_scale_frame, orient='vertical',
                                          troughcolor=THE_COLOR, from_=80, to=-40,
                                          resolution=1, tickinterval=20, length=100,
                                          command=lambda x: [create_stair()],
                                          label='Temperature start (°c)', state="active")
    temperature_start_stair_scale.grid(row=1, column=1, ipadx=10, ipady=10, padx=30, pady=0)
    temperature_start_stair_scale.set(-1)
    temperature_duration_h_stair_scale = Scale(auto_stair_scale_frame, orient='horizontal',
                                               troughcolor=THE_COLOR, from_=1, to=20,
                                               resolution=1, tickinterval=4, length=100,
                                               command=lambda x: [create_stair()],
                                               label='Duration of the plateau (H)', state="active")
    temperature_duration_h_stair_scale.grid(row=1, column=2, ipadx=30, ipady=10, padx=30, pady=0)
    temperature_duration_h_stair_scale.set(1)
    temperature_end_auto_stair = Scale(auto_stair_scale_frame, orient='vertical',
                                       troughcolor=THE_COLOR, from_=80, to=-40,
                                       resolution=1, tickinterval=20, length=100,
                                       command=lambda x: [create_stair()],
                                       label='Temperature end (°C)', state="active", relief="flat")
    temperature_end_auto_stair.grid(row=1, column=3, ipadx=10, ipady=10, padx=30, pady=0)
    temperature_end_auto_stair.set(1)

    def create_stair():
        simulation_graphic_stair(
            step_auto_stair_scale_frame_scale.get(),
            temperature_start_stair_scale.get(),
            temperature_end_auto_stair.get(),
            temperature_duration_h_stair_scale.get(),
            auto_stair_scale_frame)

    def create_cycle():
        simulation_graphic_cycle(temperature_min_scale.get(),
                                 temperature_max_scale.get(),
                                 number_of_cycles_scale.get(),
                                 temperature_min_duration_h_scale.get(),
                                 temperature_max_duration_h_scale.get(),
                                 high_low, auto_scale_frame)

    def change(high_low_value):
        global high_low
        high_low = high_low_value

    def change_2(stair_cycle_value):
        global stair_cycle
        stair_cycle = stair_cycle_value

    def dot_animation() -> [FuncAnimation, FuncAnimation]:
        global ani
        global ani2
        global first_time
        global toolbar
        xar = []
        yar = []

        xar2 = []
        yar2 = []

        style.use('ggplot')
        fig = plt.figure(figsize=(10, 5), dpi=100)

        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_ylim(FRAME)

        line, = ax1.plot(xar, yar, 'r', marker=",")
        line2, = ax1.plot(xar2, yar2, 'b', marker=",")

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
            value = VARIABLE.Thread.read(self, port)
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

        fig.legend(["order C°/min", "actual temperature C°/min"])
        state_graph(0)
        ani = animation.FuncAnimation(fig, animate, interval=5000, blit=False, init_func=init)
        ani2 = animation.FuncAnimation(fig, animate2, interval=5000, blit=False, init_func=init2)

        return [ani, ani2]

    root.mainloop()


def simulation_graphic_cycle(temperature_min, temperature_max,
                             number_of_cycles, temperature_min_duration_h, temperature_max_duration_h, min_max, window):
    if temperature_min > temperature_max:
        logger.critical(f"Error temperature_min_scale : {temperature_min} "
                        f">=  temperature_max_scale : {temperature_max}")
    else:
        root = LabelFrame(window, bd=0)
        root.grid(column=0, row=4, columnspan=6, rowspan=4)
        my_draw_6_frame_2 = LabelFrame(root)
        my_draw_6_frame_2.pack()
        my_draw_6_frame_1 = LabelFrame(root)
        my_draw_6_frame_1.pack(side=BOTTOM)
        temperature_max_duration_h = temperature_max_duration_h + 1
        temperature_min_duration_h = temperature_min_duration_h + 1
        var = 0
        if min_max:  # We swap the min/max
            var_storage_temp = temperature_max
            temperature_max = temperature_min
            temperature_min = var_storage_temp
            var_storage_time = temperature_max_duration_h
            temperature_max_duration_h = temperature_min_duration_h
            temperature_min_duration_h = var_storage_time
        data = {0: temperature_max}
        if number_of_cycles != 21:
            for p in range(0, number_of_cycles):
                for i in range(var, temperature_max_duration_h + var):
                    data[i] = temperature_max
                for i in range(temperature_max_duration_h + var,
                               temperature_max_duration_h + temperature_min_duration_h +
                               var):
                    data[i] = temperature_min
                var = var + temperature_max_duration_h + temperature_min_duration_h
        else:
            for p in range(0, 100000):
                for i in range(var, temperature_max_duration_h + var):
                    data[i] = temperature_max
                for i in range(temperature_max_duration_h + var,
                               temperature_max_duration_h + temperature_min_duration_h +
                               var):
                    data[i] = temperature_min
                var = var + temperature_max_duration_h + temperature_min_duration_h
        names = list(data.keys())
        values = list(data.values())
        fig = Figure(figsize=(5, 3), dpi=100)
        fig.add_subplot().plot(names, values, label='test')
        if number_of_cycles == 21:
            fig.legend(["∞ Infinite Mode ∞"])
        else:
            fig.legend(["°C/hour"])
        canvas = FigureCanvasTkAgg(fig, master=my_draw_6_frame_1)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


def simulation_graphic_stair(step, temp_start, temp_end, temp_duration, window):
    root = LabelFrame(window, bd=0)
    root.grid(column=0, row=2, columnspan=6, rowspan=4)
    my_draw_7_frame_2 = LabelFrame(root)
    my_draw_7_frame_2.pack()
    my_draw_7_frame_1 = LabelFrame(root)
    my_draw_7_frame_1.pack(side=BOTTOM)
    data = {0: 0}
    var = 0
    temp_duration = temp_duration + 1
    if temp_start == temp_end:
        for i in range(0, temp_duration):
            data[i] = temp_start
    else:
        if temp_end < temp_start:
            step = -step
        while abs(temp_start - temp_end) >= abs(step):
            for i in range(var, temp_duration + var):
                data[i] = temp_start
            var = var + temp_duration
            temp_start = temp_start + step
        for i in range(var, temp_duration + var):
            data[i] = temp_start
        if temp_start == temp_end:
            pass
        else:
            var = var + temp_duration
            for i in range(var, temp_duration + var):
                data[i] = temp_end

    names = list(data.keys())
    values = list(data.values())
    fig = Figure(figsize=(5, 3), dpi=100)
    fig.add_subplot().plot(names, values)
    fig.legend(["°C/hour"])
    canvas = FigureCanvasTkAgg(fig, master=my_draw_7_frame_1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
