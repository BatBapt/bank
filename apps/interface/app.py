#!/usr/bin/env python3
import sys
try:
    import tkinter as tk

    import apps.interface.login as login
except ImportError as e:
    print("App: {}".format(e))
    sys.exit(1)


class App(tk.Tk):

    def __init__(self,):
        tk.Tk.__init__(self)

        login.Login(self)
