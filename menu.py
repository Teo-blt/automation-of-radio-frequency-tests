#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: April 23 16:00:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
# Imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.colorchooser import askcolor
import data as da


# =============================================================================
# pti test

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        global elcolor
        elcolor = "#E76145"
        global size
        size = "1200x500"
        self.create_widgets()
        self.title("Main menu")
        self.withdraw()

    def oven(self):
        self.geometry(size)
        my_oven_frame = LabelFrame(self, text="Settings of the oven")
        my_oven_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        label2 = Label(my_oven_frame, text="Enter your name:")
        label2.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        name = Entry(my_oven_frame)
        name.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        button4 = Button(my_oven_frame, text="Connect", borderwidth=8, background=elcolor,
                         activebackground="green", disabledforeground="grey",
                         cursor="right_ptr",
                         overrelief="sunken", command=lambda: print("you are " + name.get()))
        button4.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        self.graphique()
        self.scale()
        self.data_managment()
        self.save()

    def data_managment(self):
        my_data_managment_frame = LabelFrame(self, text="Data_managment")
        my_data_managment_frame.grid(row=1, column=0, ipadx=40, ipady=5, padx=0, pady=0)
        label = tk.Label(my_data_managment_frame, text="data.py managment Menu")
        label.pack()
        button6 = tk.Button(my_data_managment_frame, text="Write what you want in the file",
                            borderwidth=8, background=elcolor,
                            activebackground="green", disabledforeground="grey",
                            cursor="right_ptr",
                            overrelief="sunken",
                            command=lambda: da.write_file())
        button6.pack()
        button7 = tk.Button(my_data_managment_frame, text="Read the file",
                            borderwidth=8, background=elcolor,
                            activebackground="green", disabledforeground="grey",
                            cursor="right_ptr",
                            overrelief="sunken", command=lambda: da.read_file())
        button7.pack()
        button5 = tk.Button(my_data_managment_frame, text="Delete file",
                            borderwidth=8, background=elcolor,
                            activebackground="green", disabledforeground="grey",
                            cursor="right_ptr",
                            overrelief="sunken", command=lambda: da.delete_file())
        button5.pack()

    def graphique(self):
        my_graphic_frame = LabelFrame(self, text="Graphic")
        my_graphic_frame.grid(row=0, column=3, ipadx=40, ipady=5, padx=0, pady=0)
        canv = Canvas(my_graphic_frame, bg="white", height=200, width=200)
        canv.pack()
        oval = (0, 0, 200, 200)
        line1 = (0, 0, 200, 200)
        line2 = (0, 200, 200, 0)
        canv.create_oval(oval, outline="red", width=10)
        canv.create_line(line1, fill="black", width=10)
        canv.create_line(line2, fill="black", width=10)

    def lfg(self):
        print("Low frequency generator")
        self.geometry(size)
        my_lfg_frame = LabelFrame(self, text="Settings of the Low frequency generator")
        my_lfg_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        self.graphique()

    def sg(self):
        print("Signal generator")
        self.geometry(size)
        my_sg_frame = LabelFrame(self, text="Settings of the Signal generator")
        my_sg_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        self.graphique()

    def osl(self):
        print("Oscilloscope")
        self.geometry(size)
        my_osl_frame = LabelFrame(self, text="Settings of the Oscilloscope")
        my_osl_frame.grid(row=0, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        self.graphique()

    def interface(self, choice):
        print("your choice is :", choice)
        if choice == -1:
            print("error")
            showerror("Error", "You must select a valid instrument")
        elif choice == 0:
            print("Oven")
            self.clear("Oven")
            self.oven()
        elif choice == 1:
            print("Low frequency generator")
            self.clear("Low frequency generator")
            self.lfg()
        elif choice == 2:
            print("Signal generator")
            self.clear("Signal generator")
            self.sg()
        else:
            print("Oscilloscope")
            self.clear("Oscilloscope")
            self.osl()

    def combo(self, value):  # creation of a combobox
        my_combo_frame = LabelFrame(self, text="Choice of instrument")
        my_combo_frame.grid(row=0, column=0, ipadx=40, ipady=40, padx=0, pady=0)
        labelexample = tk.Label(my_combo_frame, text="Settings", font="arial", fg="black")
        labelexample.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        labeltop = tk.Label(my_combo_frame, text="Choose your measuring tool")
        labeltop.pack(expand=False, fill="none", side=TOP)
        comboexample = ttk.Combobox(my_combo_frame, values=[
            "Oven",
            "Low frequency generator",
            "Signal generator",
            "Oscilloscope"],
                                    state="readonly")
        comboexample.set(value)
        comboexample.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)
        button3 = tk.Button(my_combo_frame, text="validate",
                            borderwidth=8, background=elcolor,
                            activebackground="green", disabledforeground="grey",
                            cursor="right_ptr",
                            overrelief="sunken",
                            command=lambda: [print(comboexample.current(),
                                                   comboexample.get()),
                                             self.interface(comboexample.current())])
        button3.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

    def create_widgets(self):  # creation of a lobby menu
        newwindow = tk.Toplevel(self)
        newwindow.configure(bg="grey")
        newwindow.title("Start menu")
        newwindow.geometry('700x200')
        label = tk.Label(newwindow, text="Menu", )
        label.pack(padx=10, pady=10, expand=True, fill="both", side=TOP)
        button1 = tk.Button(newwindow, text="Start",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [self.combo("--choose your instrument here--"),
                                             self.deiconify(), newwindow.withdraw()])
        button1.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)
        button2 = tk.Button(newwindow, text="Quit",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=newwindow.quit)
        button2.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)
        button_settings = tk.Button(newwindow, text="color", overrelief="sunken", bitmap="info", cursor="right_ptr",
                                    command=lambda: (self.dothewhat(newwindow)))
        button_settings.pack(padx=0, pady=0, expand=False, fill="none", side=LEFT)

    def dothewhat(self, newwindow):
        color = askcolor()
        global elcolor
        elcolor = color[1]
        newwindow.destroy()
        self.create_widgets()

    def scale(self):
        v = IntVar()
        my_scale_frame = LabelFrame(self, text="A scale")
        my_scale_frame.grid(row=0, column=2, ipadx=40, ipady=40, padx=0, pady=0)
        scale1 = Scale(my_scale_frame, orient='vertical', variable=v, troughcolor=elcolor, from_=0, to=100,
                       resolution=1, tickinterval=25, length=100, command=0,
                       label='Power', state="active")
        scale1.pack(side=LEFT)
        power = Entry(my_scale_frame, validate="all", textvariable=v,
                      invalidcommand=lambda: showerror("Error", "Therre is an error"))
        power.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        label4 = tk.Label(my_scale_frame, text="Menu", textvariable=v)
        label4.pack(padx=0, pady=0, expand=True, fill="none", side=TOP)

    def clear(self, get_tilte):
        print("clear")
        self.destroy()
        Tk.__init__(self)
        self.title(get_tilte + " menu")
        self.combo(get_tilte)

    def save(self):
        my_save_frame = LabelFrame(self, text="Save menu")
        my_save_frame.grid(row=1, column=1, ipadx=40, ipady=40, padx=0, pady=0)
        button9 = tk.Button(my_save_frame, text="Save",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=my_save_frame.quit)
        button9.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

        button8 = tk.Button(my_save_frame, text="Quit",
                            borderwidth=8, background=elcolor,
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: (self.leving()))
        button8.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

    def leving(self):
        if askyesno('Warning', 'Are you sure you want to do exit ?'):
            if askyesno('Warning', 'your data is not saved, are you sure you want to continue'):
                self.quit()


"""
if __name__ == "__main__":
    app = Application()
    app.title("Application for the automation of radiofrequency tests")
    app.mainloop()
"""
Application().mainloop()
