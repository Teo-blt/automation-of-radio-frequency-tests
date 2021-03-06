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
import matplotlib.patches as mpatches

# =============================================================================
THE_COLOR = "#E76145"


def draw_graph(self):
    window_graph_data = Toplevel(self)
    window_graph_data.grab_set()
    window_graph_data.focus_set()
    window_graph_data.title("Graph data settings")
    verification_frame = LabelFrame(window_graph_data)
    verification_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    menu_frame = LabelFrame(verification_frame, text="Menu")
    menu_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
    choice_frame = LabelFrame(verification_frame, text="Choice")
    mode_sensibility_graph = LabelFrame(verification_frame, text="Mode sensibility graph")
    mode_filter_graph = LabelFrame(verification_frame, text="Mode filter graph")
    info_selection = LabelFrame(verification_frame, text="Info selection")
    label_top = Label(menu_frame, text="Choose your data file")
    label_top.pack(expand=False, fill="none", side=TOP)
    file_name_label = Label(menu_frame, text="File name :")
    file_name_label.pack(expand=False, fill="none", side=TOP),
    file_entry = Entry(menu_frame, cursor="right_ptr")
    file_entry.pack(expand=False, fill="none", side=TOP)
    file_entry.insert(0, 'Select data file')
    import_file_button = Button(menu_frame, text="Import file",
                                borderwidth=8, background=THE_COLOR,
                                activebackground="green", cursor="right_ptr", overrelief="sunken",
                                command=lambda: [uploadaction(file_entry)])
    import_file_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)

    choose_packet_rate_combobox = ttk.Combobox(mode_sensibility_graph, values=[
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
        redirection(bla.get(), 1, file_entry.get())

    def uploadaction(file_entry):
        filename = filedialog.askopenfilename(filetypes=[("text files", ".txt")])
        file_entry.delete(0, 2000)
        file_entry.insert(0, filename)

    choose_packet_rate_combobox.bind("<<ComboboxSelected>>", chose)
    choose_packet_rate_combobox.set("-Choose your packet-")

    choose_temp_combobox = ttk.Combobox(mode_sensibility_graph, values=["1", "2"], state="readonly")

    def temp_chose(e, i=choose_temp_combobox):
        return temp_validate(e, i)

    def temp_validate(e, bla):
        redirection(bla.get(), 0, file_entry.get())

    choose_temp_combobox.bind("<<ComboboxSelected>>", temp_chose)
    choose_temp_combobox.set("-Choose your temperature-")

    temp_label = Label(mode_sensibility_graph, text="Number of the temperature :")
    sensi_label = Label(mode_sensibility_graph, text="Sensibility value :")

    def change_value_temp():
        data = pd.read_csv(file_entry.get(), sep='\s+', header=None)
        data = pd.DataFrame(data)
        new_values = [str(data[4][0])]
        for i in range(1, len(data[4])):
            if data[4][i - 1] != data[4][i]:
                new_values.append(str(data[4][i]))
        choose_temp_combobox.config(values=new_values)

    a = IntVar()
    sensibility_radiobutton = Radiobutton(mode_sensibility_graph, text="Choose temp",
                                          variable=a, value=0, cursor="right_ptr",
                                          indicatoron=0, command=lambda: [choose_packet_rate_combobox.forget(),
                                                                          temp_label.pack(expand=False, fill="none",
                                                                                          side=TOP),
                                                                          choose_temp_combobox.pack(expand=False,
                                                                                                    fill="none",
                                                                                                    side=TOP),
                                                                          change_value_temp(), sensi_label.forget()],
                                          background=THE_COLOR,
                                          activebackground="green",
                                          bd=8, selectcolor="green", overrelief="sunken")
    sensibility_radiobutton.pack(expand=False, fill="none", side=TOP)
    sensibility_choose_radiobutton = Radiobutton(mode_sensibility_graph,
                                                 text="Choose sensibility", variable=a, value=1,
                                                 cursor="right_ptr", indicatoron=0,
                                                 command=lambda: [sensi_label.pack(expand=False, fill="none",
                                                                                   side=TOP),
                                                                  choose_packet_rate_combobox.pack(padx=50, pady=0,
                                                                                                   expand=True,
                                                                                                   fill="both",
                                                                                                   side=TOP),
                                                                  choose_temp_combobox.forget(), temp_label.forget(),
                                                                  ],
                                                 background=THE_COLOR,
                                                 activebackground="green",
                                                 bd=8, selectcolor="green", overrelief="sunken")
    sensibility_choose_radiobutton.pack(expand=False, fill="none", side=TOP)

    b = IntVar()
    radiobutton_sensibility_graph = Radiobutton(choice_frame, text="Sensibility graph",
                                                variable=b, value=0, cursor="right_ptr",
                                                indicatoron=0, command=lambda:
        [mode_sensibility_graph.grid(row=1, column=2, ipadx=0, ipady=0, padx=0, pady=0),
         mode_filter_graph.grid_forget(), filter_choose_packet_rate_combobox.forget(), filter_label.forget()],
                                                background=THE_COLOR,
                                                activebackground="green",
                                                bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_sensibility_graph.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    radiobutton_filter_graph = Radiobutton(choice_frame, text="Filter graph",
                                           variable=b, value=1, cursor="right_ptr",
                                           indicatoron=0, command=lambda:
        [mode_filter_graph.grid(row=1, column=2, ipadx=0, ipady=0, padx=0, pady=0),
         mode_sensibility_graph.grid_forget(), filter_choose_packet_rate_combobox.pack(padx=50, pady=0, expand=True,
                                                                                       fill="both", side=BOTTOM),
         filter_label.pack(expand=False, fill="none", side=TOP)],
                                           background=THE_COLOR,
                                           activebackground="green",
                                           bd=8, selectcolor="green", overrelief="sunken")
    radiobutton_filter_graph.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)

    info_file_name_label = Label(info_selection, text="Actual file :")
    info_file_name_label.pack(expand=False, fill="none", side=TOP)
    info_label = Label(info_selection, text="")
    info_label.pack(expand=False, fill="none", side=TOP)
    back_button = Button(info_selection, text="Back",
                         borderwidth=8, background=THE_COLOR,
                         activebackground="green", cursor="right_ptr", overrelief="sunken",
                         command=lambda: [go_back()])
    back_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)
    filter_label = Label(mode_filter_graph, text="filter graph mode", font="arial")

    filter_choose_packet_rate_combobox = ttk.Combobox(mode_filter_graph, values=[
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

    def filter_chose(e, i=filter_choose_packet_rate_combobox):
        return filter_validate(e, i)

    def filter_validate(e, bla):
        redirection(bla.get(), 2, file_entry.get())

    filter_choose_packet_rate_combobox.bind("<<ComboboxSelected>>", filter_chose)
    filter_choose_packet_rate_combobox.set("-Choose your packet-")

    def verification(file_name):
        data = []
        try:
            data = pd.read_csv(file_name, sep='\s+', header=None)
            data = pd.DataFrame(data)
            menu_frame.grid_forget()
            info_selection.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
            info_label.config(text=file_name.split("/")[-1])
            if data[7][0] == "filter":
                radiobutton_filter_graph.invoke()
            elif data[7][0] == "sensibility":
                radiobutton_sensibility_graph.invoke()
                sensibility_choose_radiobutton.invoke()
            else:
                logger.critical(f"The file name {file_name} is invalid")

        except:
            logger.critical(f"The file name {file_name} is invalid")

    check_button = Button(menu_frame, text="Check file",
                          borderwidth=8, background=THE_COLOR,
                          activebackground="green", cursor="right_ptr", overrelief="sunken",
                          command=lambda: [verification(file_entry.get())])
    check_button.pack(padx=1, pady=1, ipadx=40, ipady=20, expand=False, fill="none", side=RIGHT)

    def go_back():
        choice_frame.grid_forget()
        mode_sensibility_graph.grid_forget()
        menu_frame.grid(row=1, column=0, ipadx=0, ipady=0, padx=0, pady=0)
        info_selection.grid_forget()
        mode_filter_graph.grid_forget()

    window_graph_data.mainloop()


def redirection(value, graph_type, file_name):
    data = []
    try:
        data = pd.read_csv(file_name, sep='\s+', header=None)
        data = pd.DataFrame(data)
    except:
        logger.critical(f"The file name {file_name} is invalid")
    if graph_type == 1:
        draw_graph_sensibility(value, 1, file_name)
    elif graph_type == 0:
        draw_graph_sensibility(int(value), 0, file_name)
    else:
        draw_graph_filter(file_name, value)


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
        l = 0
        while data[4][l] != value:
            l += 1
        value = data[2][l]
        for m in range(value, value + 1):
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


def draw_graph_filter(name, value):
    try:
        plt.close()
    except:
        pass
    file_name = name
    data = pd.read_csv(file_name, sep='\s+', header=None)
    data = pd.DataFrame(data)
    paket_rate = int(value[:2])
    color = {0: 'b', 1: 'r', 2: 'g', 3: 'y', 4: 'c', 5: 'lime', 6: 'black', 7: 'pink'}
    sf = data[5][0]
    bw = data[5][0]
    i = 0
    p = 0
    X = {}
    Y = {}
    Z = {}
    G = {}
    H = {}
    while i < len(data[0]):
        X[p] = data[0][i]
        Y[p] = data[1][i]
        Z[p] = data[6][i]
        i += 1
        p += 1
    more_than_paket_rate = 0
    t = 0
    i = 1
    j = 1
    number_of_frequency = {0: min(data[6])}
    temp = [min(data[3])]
    while i < len(data[0]):
        if data[3][i] > max(temp):
            temp.append(data[3][i])
        if data[6][i] != data[6][i - 1]:
            number_of_frequency[j] = data[6][i]
            j += 1
            i += 1
        else:
            i += 1
    b = 0
    k = 0
    while b < len(number_of_frequency):
        if b == 0:
            pass
        else:
            while data[6][k] != number_of_frequency[b]:
                k += 1
            more_than_paket_rate = k
        try:
            while Y[more_than_paket_rate] < paket_rate:
                more_than_paket_rate += 1
            if Y[more_than_paket_rate] == paket_rate:
                G[t] = X[more_than_paket_rate]
                H[t] = Z[more_than_paket_rate]
                more_than_paket_rate += 1
                t += 1
                b += 1
            else:
                delta_y = round(abs(X[more_than_paket_rate - 1] - X[more_than_paket_rate]), 10)
                if delta_y != 1:
                    more_than_paket_rate += 1
                    b += 1
                else:
                    delta_x = abs(Y[more_than_paket_rate - 1] - Y[more_than_paket_rate])
                    delta = -(delta_x / delta_y)
                    a = Y[more_than_paket_rate] - (delta * X[more_than_paket_rate])
                    value = (50 - a) / delta
                    G[t] = value
                    H[t] = Z[more_than_paket_rate]
                    more_than_paket_rate += 1
                    t += 1
                    b += 1
        except:
            break
    a = -1
    frequency_min = H[0]
    for w in range(0, len(G)):
        if H[w] == frequency_min:
            a += 1
            if a == 8:
                a = 0
        plt.plot(H[w], G[w], "o-", color=color[a])
    plt.xlabel("Channel frequency Hz")
    plt.ylabel("Power at the entrance of the receiver in dBm")
    plt.title(f"Graphical representation of sensitivity test results for {paket_rate}% of packet lost\n"
              f"Spreading factor: {sf}, Band width: {bw}")
    graph_color = []
    for t in range(0, len(temp)):
        a = t
        if a == 8:
            a = t - 8
        graph_color.append(mpatches.Patch(color=color[a], label=str(temp[t]) + "°C"))
    plt.legend(handles=graph_color)
    plt.show()
