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
import os
from tkinter.messagebox import *
# =============================================================================


def file():
    # text to implement in a file
    print("I am in the file")
    presentation = "My name is Teo.\nI have 20 year old"
    # open a new file
    with open("data.py.txt", "w+") as file:
        file.write(presentation)  # I write in the file
        file.seek(0)  # Replace cursor at start of file
        print(file.read())  # read all the file
        file.seek(3)  # replace the cursor at the 4th byte of the file
        print(file.read(9))  # read 9 character from 4th
        file.seek(0)  # Replace cursor at start of file
        print(file.readline())  # read a line of the file


def delete_file():
    try :
        os.remove("data.py.txt")
        print("File successfully deleted")
        showinfo("info", "File successfully deleted")
    except:
        print("The file does not exist")
        showerror("Error", "The file does not exist")


def write_file():
    text = input("What do you want to write ?")
    with open("data.py.txt", "w") as file:
        file.write(text)


def read_file():
    try:
        file = open("data.py.txt", "r")
        print(file.read())
    except:
        print("The file does not exist")
        showerror("Error", "The file does not exist")
    finally:
        print("The program has been correctly ended")
        showinfo("info","The program has been correctly ended")
