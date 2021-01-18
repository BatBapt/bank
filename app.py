#!/usr/bin/env python3
import tkinter as tk
from tkinter.messagebox import showerror
import re

from database import Database

from home import Home


class App(tk.Tk):

    database = Database()

    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry("900x500+500+200")

        self.frame = tk.Frame(self, width=900, height=475)
        self.frame.pack()
        self.frame.focus_set()

        tk.Label(self.frame, text="Bienvenu(e)\n Veuillez vous connecter pour accéder à vos comptes").pack(pady=(30, 0))

        self.email_var = tk.StringVar()
        tk.Label(self.frame, text="Entrez votre email: ").pack(pady=(100, 0))
        self.entry_email = tk.Entry(self.frame, textvariable=self.email_var, width=30)
        self.entry_email.insert(0, 'dupont@gmail.com')
        self.entry_email.pack(pady=(0, 20))

        self.password_var = tk.StringVar()
        tk.Label(self.frame, text="Entrez votre mot de passe: ").pack(pady=(5, 0))
        self.entry_pwd = tk.Entry(self.frame, textvariable=self.password_var, width=30, show='*')
        self.entry_pwd.pack(pady=(0, 50))

        connect_btn = tk.Button(self.frame, text="Se connecter", command=self.connect)
        connect_btn.pack(side=tk.LEFT)

        signup_btn = tk.Button(self.frame, text="Ouvrir un compte")
        signup_btn.pack(side=tk.RIGHT)

        self.entry_email.bind('<Button-1>', self.clean_entry)
        self.frame.bind('<Return>', self.connect)

    def clean_entry(self, event=None):
        self.entry_email.delete(0, tk.END)

    def valid_email(self, email):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

    def connect(self, event=None):
        email = self.email_var.get()
        pwd = self.password_var.get()
        error_msg = "Attention l'email n'est pas au bon format"

        email_ok = self.valid_email(email)
        if email_ok:
            p = App.database.check_person_exist(email, pwd)
            if not p:
                showerror("Erreur", "Nous n'avons pas pu trouver votre compte.")
                return
            Home(self.frame, p, App.database)
        else:
            showerror("Erreur", error_msg)
            self.clean_entry()
            self.entry_pwd.delete(0, tk.END)


if __name__ == '__main__':
    app = App()
    app.mainloop()
    exit(0)
