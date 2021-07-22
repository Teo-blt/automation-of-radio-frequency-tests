#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Bulteau Téo
# Created Date: April 23 16:00:00 2021
# For Kerlink, all rights reserved
# =============================================================================
"""The Module Has Been Build for the automation of radio frequency tests"""
# =============================================================================
# Imports
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from IHM_redirect import Menu_Climatic_chamber

# ============================================================================

LOBBY_WINDOW_SIZE = "700x200"
WINDOW_SIZE = "1200x500"
THE_COLOR = "blue"#"#E76145"


class Application(Tk):
    def __init__(self):
        Tk.__init__(self)  # Initialisation of the first window
        self._port = 'COM11'
        self._gpib_port = "25"
        self._ip_address = "192.168.4.228"
        self.status = 0
        self.interface(1)
        self._carte_ip_address = "192.168.4.183"

    def create_choose_measuring_tool_combobox(self, value: str):
        """
        creation of a combobox, this combobox allow user to choose a measuring tool in a list
        :param value: value of the combobox
        """
        instrument_choose_combobox = LabelFrame(self, text="Choice of instrument")
        instrument_choose_combobox.grid(row=0, column=0, ipadx=40, ipady=20, padx=0, pady=0)

        settings_label = Label(instrument_choose_combobox, text="Settings", font="arial", fg="black")
        settings_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)

        label_top = Label(instrument_choose_combobox, text="Choose your measuring tool")
        label_top.pack(expand=False, fill="none", side=TOP)

        choose_measuring_tool_combobox = ttk.Combobox(instrument_choose_combobox, values=[
            "Climatic chamber",  # The list of measuring tool
            "IBTS",
            "Izepto"
        ], state="readonly")

        def chose(e, i=choose_measuring_tool_combobox):
            return validate(e, i)

        def validate(e, choose_measuring_tool_combobox):
            self.interface(choose_measuring_tool_combobox.current())

        choose_measuring_tool_combobox.bind("<<ComboboxSelected>>", chose)
        choose_measuring_tool_combobox.set(value)
        choose_measuring_tool_combobox.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)

    def create_choose_scenario_combobox(self, value: str):
        """
        creation of a combobox, this combobox allow user to choose a measuring tool in a list
        :param value: value of the combobox
        """
        scenario_choose_combobox = LabelFrame(self, text="Choice of scenario")
        scenario_choose_combobox.grid(row=1, column=0, ipadx=40, ipady=20, padx=0, pady=0)

        settings_label = Label(scenario_choose_combobox, text="Settings", font="arial", fg="black")
        settings_label.pack(padx=0, pady=0, expand=False, fill="none", side=TOP)

        label_top = Label(scenario_choose_combobox, text="Choose your scenario")
        label_top.pack(expand=False, fill="none", side=TOP)

        choose_scenario_combobox = ttk.Combobox(scenario_choose_combobox, values=[
            "Sensibility test",
            "Filter test"
        ], state="readonly")  # The list of measuring tool

        def chose(e, i=choose_scenario_combobox):
            return validate(e, i)

        def validate(e, choose_scenario_combobox):
            self.interface_2(choose_scenario_combobox.current())

        choose_scenario_combobox.bind("<<ComboboxSelected>>", chose)
        choose_scenario_combobox.set(value)
        choose_scenario_combobox.pack(padx=50, pady=0, expand=False, fill="x", side=TOP)

    def configuration_menu(self):
        from Order_files import Configuration_file_management
        configuration_menu_button = Button(self, text="Order file", borderwidth=8, background=THE_COLOR,
                                           cursor="right_ptr",
                                           overrelief="sunken",
                                           command=lambda: [Configuration_file_management.menu()])
        configuration_menu_button.grid(row=4, column=4, ipadx=0, ipady=0, padx=0, pady=0)

    def interface(self, choice):  # This function open other functions after the choice of the user
        if choice == -1:
            showerror("Error", "You must select a valid instrument")
        elif choice == 0:
            self.create_new_window("Climatic chamber")  # Call the clear function to clean all the window
            self.climatic_chamber_widget()  # Open Climatic chamber
        elif choice == 1:
            self.create_new_window("IBTS")  # Call the clear function to clean all the window
            self.ibts()  # Open generator
        elif choice == 2:
            self.create_new_window("Izepto")  # Call the clear function to clean all the window
            self.carte_izepto()  # Open generator
        """
        elif choice == 1:
            self.create_new_window("SMIQ")  # Call the clear function to clean all the window
            self.sg()  # Open generator
        """


    def interface_2(self, choice):  # This function open other functions after the choice of the user
        if choice == -1:
            showerror("Error", "You must select a valid instrument")
        elif choice == 0:
            self.create_new_window("Sensibility test")  # Call the clear function to clean all the window
            self.sensibility_test()  # Open generator
        elif choice == 1:
            self.create_new_window("Filter test")  # Call the clear function to clean all the window
            self.filter_test()  # Open generator

    def create_new_window(self, window_title: str):
        """
        Clear function, destroy all the windows and create a new window after the choice of the user
        :param window_title:
        """
        self.destroy()
        Tk.__init__(self)
        self.title(window_title + " menu")
        self.create_choose_measuring_tool_combobox(window_title)
        self.create_choose_scenario_combobox(window_title)
        self.configuration_menu()
        #  Sequencer.sequencer(self) not use anymore

    def sg(self):  # The signal generator menu
        from IHM_redirect import Menu_SMIQ
        self.geometry(WINDOW_SIZE)  # set window size
        Menu_SMIQ.sg_menu(self, self._gpib_port)

    def ibts(self):  # The IBTS menu
        from IHM_redirect import Menu_IBTS
        self.geometry(WINDOW_SIZE)  # set window size
        Menu_IBTS.ibts_menu(self, self._ip_address)

    def climatic_chamber_widget(self):  # The climatic chamber menu
        self.geometry(WINDOW_SIZE)  # set window size
        Menu_Climatic_chamber.start_climatic_chamber(self, self._port)

    def carte_izepto(self):  # The Izepto menu
        from IHM_redirect import Menu_Izepto
        self.geometry(WINDOW_SIZE)  # set window size
        Menu_Izepto.izepto_menu(self, self._carte_ip_address)

    def sensibility_test(self):  # The Sensibility test menu
        from IHM_redirect import Menu_Sensibility_test
        self.geometry(WINDOW_SIZE)  # set window size
        Menu_Sensibility_test.sensibility_test_menu(self, self._port, self._ip_address, self._carte_ip_address)

    def filter_test(self):  # The Sensibility test menu
        from IHM_redirect import Menu_Filter_test
        self.geometry(WINDOW_SIZE)  # set window size
        Menu_Filter_test.filter_test_menu(self, self._carte_ip_address, self._ip_address, self._port)


Application().mainloop()
