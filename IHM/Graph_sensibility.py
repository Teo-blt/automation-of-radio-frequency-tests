#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: June 30 10:00:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# =============================================================================
THE_COLOR = "#E76145"


def draw_graph():
    window_graph_data = Tk()
    window_graph_data.title("Graph data settings")
    #  window_graph_data.geometry("300x300")
    settings_frame = LabelFrame(window_graph_data, text="Settings")
    settings_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    settings_frame.config(background='#fafafa')
    label_top = Label(settings_frame, text="Choose your packet rate")
    label_top.pack(expand=False, fill="none", side=TOP)
    file_name_label = Label(settings_frame, text="File name :")
    file_name_label.pack(expand=False, fill="none", side=TOP),
    file_entry = Entry(settings_frame, cursor="right_ptr")
    file_entry.pack(expand=False, fill="none", side=TOP)
    file_entry.insert(0, 'data.txt')
    import_file_button = Button(settings_frame, text="Import file",
                                borderwidth=8, background=THE_COLOR,
                                activebackground="green", cursor="right_ptr", overrelief="sunken",
                                command=lambda: [uploadaction(file_entry)])
    import_file_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)

    choose_packet_rate_combobox = ttk.Combobox(settings_frame, values=[
        "10%",  # The list of measuring tool
        "20%",
        "30%",
        "40%",
        "50%",
        "60%",
        "70%",
        "80%",
        "90%"
    ], state="readonly")

    def chose(e, i=choose_packet_rate_combobox):
        return validate(e, i)

    def validate(e, bla):
        verification(bla.get(), 1, window_graph_data, file_entry.get())

    def uploadaction(file_entry):
        filename = filedialog.askopenfilename(filetypes=[("text files", ".txt")])
        file_entry.delete(0, 2000)
        file_entry.insert(0, filename)

    choose_packet_rate_combobox.bind("<<ComboboxSelected>>", chose)
    choose_packet_rate_combobox.set("-Choose your packet-")
    temp_label = Label(settings_frame, text="Number of the temperature :")
    temp = Entry(settings_frame, cursor="right_ptr")
    temp.insert(0, 0)
    send_button = Button(settings_frame, text="Send",
                         borderwidth=8, background=THE_COLOR,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [verification(int(temp.get()), 0, window_graph_data, file_entry.get())])

    a = IntVar()
    sensibility_radiobutton = Radiobutton(settings_frame, text="Choose temp",
                                          variable=a, value=0, cursor="right_ptr",
                                          indicatoron=0, command=lambda: [choose_packet_rate_combobox.forget(),
                                                                          temp_label.pack(expand=False, fill="none",
                                                                                          side=TOP),
                                                                          temp.pack(expand=False, fill="none",
                                                                                    side=TOP),
                                                                          send_button.pack(padx=10, pady=10, ipadx=10,
                                                                                           ipady=10, expand=False,
                                                                                           fill="none", side=TOP)],
                                          background=THE_COLOR,
                                          activebackground="green",
                                          bd=8, selectcolor="green", overrelief="sunken")
    sensibility_radiobutton.pack(expand=False, fill="none", side=TOP)
    sensibility_choose_radiobutton = Radiobutton(settings_frame,
                                                 text="Choose sensibility", variable=a, value=1,
                                                 cursor="right_ptr", indicatoron=0,
                                                 command=lambda: [
                                                     choose_packet_rate_combobox.pack(padx=50, pady=0, expand=True,
                                                                                      fill="both", side=TOP),
                                                     temp.forget(), temp_label.forget(), send_button.forget()],
                                                 background=THE_COLOR,
                                                 activebackground="green",
                                                 bd=8, selectcolor="green", overrelief="sunken")
    sensibility_choose_radiobutton.pack(expand=False, fill="none", side=TOP)
    sensibility_choose_radiobutton.invoke()
    b = IntVar()
    radiobutton_sensibility_graph = Radiobutton(settings_frame, text="Sensibility graph",
                                                variable=b, value=0, cursor="right_ptr",
                                                indicatoron=0, command=lambda: [],
                                                background=THE_COLOR,
                                                activebackground="green",
                                                bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_sensibility_graph.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    radiobutton_filter_graph = Radiobutton(settings_frame, text="Filter graph",
                                           variable=b, value=1, cursor="right_ptr",
                                           indicatoron=0, command=lambda: [],
                                           background=THE_COLOR,
                                           activebackground="green",
                                           bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_filter_graph.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)

    window_graph_data.mainloop()


def verification(value, graph_type, window, file_name):
    data = []
    try:
        data = pd.read_csv(file_name, sep='\s+', header=None)
        data = pd.DataFrame(data)
    except:
        logger.critical(f"The file name {file_name} is invalid")

    if graph_type == 1:
        draw_graph_sensibility(value, 1, file_name)
    elif graph_type == 0:
        if value < 0 or value > int(max(data[2])):
            logger.critical(f"Error, there is only {max(data[2])} temperature")
        else:
            draw_graph_sensibility(value, 0, file_name)
    else:
        draw_graph_filter(value, file_name)


def draw_graph_sensibility(value, graph_type, name):
    try:
        plt.close()
    except:
        pass
    color = {0: 'b', 1: 'r', 2: 'g', 3: 'y', 4: 'c', 5: 'lime', 6: 'black', 7: 'pink'}
    freq_step = 0.2

    if graph_type == 1:
        paket_rate = int(value[:2])
    else:
        paket_rate = 0

    file_name = name
    data = pd.read_csv(file_name, sep='\s+', header=None)
    data = pd.DataFrame(data)
    temp = {0: data[4][0]}
    sf = data[5][0]
    bw = data[6][0]
    m = 0
    X = {}
    Y = {}
    numbers_of_channel = max(data[3]) + 1
    number_of_temp = max(data[2]) + 1
    t = 0
    d = 0
    while t != len(data):
        if data[4][t] != temp[d]:
            d += 1
            temp[d] = data[4][t]
        if t != 0:
            t = t + 1
        else:
            for i in range(0, number_of_temp):
                X[i] = {}
                Y[i] = {}
        X[data[2][t]][data[3][t]] = [data[0][t]]
        Y[data[2][t]][data[3][t]] = [data[1][t]]
        try:
            while data[3][t] == data[3][t + 1]:
                X[data[2][t]][data[3][t]] = X[data[2][t]][data[3][t]] + [data[0][t + 1]]
                Y[data[2][t]][data[3][t]] = Y[data[2][t]][data[3][t]] + [data[1][t + 1]]
                t = t + 1
        except:
            break
    if graph_type == 0:
        for m in range(value, value + 1):
            # marker = "$" + str(m) + "$"
            marker = ","
            for n in range(0, numbers_of_channel):
                plt.plot(X[m][n], Y[m][n], color[n], marker=marker)
        plt.xlabel("Power at the entrance of the receiver in dBm")
        plt.ylabel("% of packet lost")
        plt.title(f"Graphical representation of sensitivity test results for temperature of {temp[m]}°C\n"
                  f"Spreading factor: {sf}, Band width: {bw}")
        plt.show()

    G = {}
    for r in range(0, numbers_of_channel):
        G[r] = {}

    for x in range(0, number_of_temp):
        for y in range(0, numbers_of_channel):
            more_than_paket_rate = 0
            try:
                while Y[x][y][more_than_paket_rate] < paket_rate or Y[x][y][more_than_paket_rate + 1] < paket_rate:
                    more_than_paket_rate += 1

                if Y[x][y][more_than_paket_rate] == paket_rate and Y[x][y][more_than_paket_rate + 1] < paket_rate:
                    G[x][y] = X[x][y][more_than_paket_rate]
                else:
                    delta_y = round(abs(X[x][y][more_than_paket_rate - 1] - X[x][y][more_than_paket_rate]), 10)
                    delta_x = abs(Y[x][y][more_than_paket_rate - 1] - Y[x][y][more_than_paket_rate])
                    delta = -(delta_x / delta_y)
                    a = Y[x][y][more_than_paket_rate] - (delta * X[x][y][more_than_paket_rate])
                    value = (50 - a) / delta
                    G[x][y] = value
            except:
                break

    if graph_type == 1:
        j = 0
        for s in range(0, number_of_temp):
            if j > 7:
                j = 0
            freq = ['867.1']
            for r in range(0, len(G[s].values())):
                if r != 0:
                    freq = freq + [str(round(float(freq[r - 1]) + freq_step, 1))]
            plt.plot(freq, G[s].values(), "o-", color=color[j], label=str(temp[s]) + "°C")
            j += 1
        plt.xlabel("Channel frequency")
        plt.ylabel("Power at the entrance of the receiver in dBm")
        plt.title(f"Graphical representation of sensitivity test results for {paket_rate}% of packet lost\n"
                  f"Spreading factor: {sf}, Band width: {bw}")
        plt.legend()
        plt.show()


def draw_graph_filter(value, name):
    try:
        plt.close()
    except:
        pass
    file_name = name
    data = pd.read_csv(file_name, sep='\s+', header=None)
    data = pd.DataFrame(data)
    print(data)
