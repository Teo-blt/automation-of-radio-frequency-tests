#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: April 18 16:00:00 2021
# For Kerlik, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
# Imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
# =============================================================================


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.creer_widgets()
        self.title("Main menu")
        self.withdraw()

    def oven(self):
        print("Oven")
        label2 = Label(self, text="Enter your name:")
        label2.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        name = Entry(self)
        name.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        button4 = Button(self, text="Connect!", command=lambda: print("you are"))
        button4.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)

    def lfg(self):
        print("Low frequency generator")

    def sg(self):
        print("Signal generator")

    def osl(self):
        print("Oscilloscope")

    def interface(self, valeur_choix):
        print("la valeur_choix est :", valeur_choix)
        if valeur_choix == -1:
            print("error")
            showerror("Error", "You must select a valid instrument")
        elif valeur_choix == 0:
            print("Oven")
            self.oven()
        elif valeur_choix == 1:
            print("Low frequency generator")
            self.lfg()
        elif valeur_choix == 2:
            print("Signal generator")
            self.sg()
        else:
            print("Oscilloscope")
            self.sol()

    def combo(self):  #creation of a combobox
        self.geometry("300x200")
        labelexample = tk.Label(self, text="Settings", font="arial", fg="black")
        labelexample.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)
        labeltop = tk.Label(self, text="Choose your measuring tool")
        labeltop.pack(expand=False, fill="none", side=TOP)
        comboexample = ttk.Combobox(self, values=[
                                     "Oven",
                                     "Low frequency generator",
                                     "Signal generator",
                                     "Oscilloscope"],
                                    state="readonly")
        comboexample.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)
        button3 = tk.Button(self, text="validate",
                            borderwidth=8, background="#E76145",
                            activebackground="green", disabledforeground="grey",
                            overrelief="sunken",
                            command=lambda: [print(comboexample.current(),
                                                   comboexample.get()), self.interface(comboexample.current())])
        button3.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)

    def creer_widgets(self):  #creation of a lobby menu
        newwindow = tk.Toplevel(self)
        newwindow.configure(bg="grey")
        newwindow.title("Start menu")
        newwindow.geometry('700x200')
        label = tk.Label(newwindow, text="Menu",)
        label.pack(padx=10, pady=10, expand=True, fill="both", side=TOP)
        button1 = tk.Button(newwindow, text="Start",
                            borderwidth=8, background="#E76145",
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=lambda: [self.combo(), self.deiconify(), newwindow.withdraw()])
        button1.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)
        button2 = tk.Button(newwindow, text="Quit",
                            borderwidth=8, background="#E76145",
                            activebackground="green", cursor="right_ptr", overrelief="sunken",
                            command=newwindow.quit)
        button2.pack(padx=30, pady=10, expand=True, fill="both", side=TOP)


"""
if __name__ == "__main__":
    app = Application()
    app.title("Application for the automation of radiofrequency tests")
    app.mainloop()
"""
Application().mainloop()
