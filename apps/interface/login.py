import sys
try:
    import tkinter as tk
    from tkinter import font
    from tkinter.messagebox import showerror
    import re

    import apps.database.database as db

    import apps.interface.signin as signin
    import apps.interface.home as home

except ImportError as e:
    print("Login: {}".format(e))
    sys.exit(1)


class Login(tk.Frame):

    database = db.Database()
    frame_bg_color = "#F0B649"
    btn_bg_color = "#4892F0"

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)

        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.geometry("900x500+500+200")
        self.master.title("Accueil")
        self.master.configure(background="#4892F0")

        btn_font = font.Font(family='Helvetica', name='myFont', size=12, weight='bold')

        self.frame = tk.Frame(self.master, width=900, height=500, bg=Login.frame_bg_color)
        self.frame.pack(pady=(75, 20))
        self.frame.focus_set()

        tk.Label(self.frame, text="Bienvenu(e)\n Veuillez vous connecter pour accéder à vos comptes", bg=Login.frame_bg_color).pack(pady=(30, 0))

        self.email_var = tk.StringVar()
        tk.Label(self.frame, text="Entrez votre email: ", bg=Login.frame_bg_color).pack(pady=(75, 0))
        self.entry_email = tk.Entry(self.frame, textvariable=self.email_var, width=30)
        self.entry_email.insert(0, 'dupont@gmail.com')
        self.entry_email.pack(pady=(0, 20))

        self.password_var = tk.StringVar()
        tk.Label(self.frame, text="Entrez votre mot de passe: ", bg=Login.frame_bg_color).pack(pady=(5, 0))
        self.entry_pwd = tk.Entry(self.frame, textvariable=self.password_var, width=30, show='*')
        self.entry_pwd.pack(pady=(0, 50))

        self.connect_btn = tk.Button(self.frame, text="Se connecter", command=self.connect, bg=Login.btn_bg_color, fg=Login.frame_bg_color, font=btn_font, width=30)
        self.connect_btn.pack(side=tk.LEFT)

        self.signup_btn = tk.Button(self.frame, text="Ouvrir un compte", command=self.signin, bg=Login.btn_bg_color, fg=Login.frame_bg_color, font=btn_font, width=30)
        self.signup_btn.pack(side=tk.RIGHT)

        self.entry_email.bind('<Button-1>', self.clean_entry)
        self.frame.bind_all('<Return>', self.connect)

        self.connect_btn.bind('<Enter>', func=lambda e, button=self.connect_btn: self.hover(button=button, event=e))
        self.connect_btn.bind('<Leave>', func=lambda e, button=self.connect_btn: self.unhover(button=button, event=e))

        self.signup_btn.bind('<Enter>', func=lambda e, button=self.signup_btn: self.hover(button=button, event=e))
        self.signup_btn.bind('<Leave>', func=lambda e, button=self.signup_btn: self.unhover(button=button, event=e))

    def hover(self, button, event):
        button.config(activebackground=Login.frame_bg_color)
        button.config(activeforeground=Login.btn_bg_color)

    def unhover(self, button, event):
        button.config(activebackground=Login.frame_bg_color)
        button.config(activeforeground=Login.btn_bg_color)

    def clean_entry(self, event=None):
        self.entry_email.delete(0, tk.END)

    def valid_email(self, email):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

    def connect(self, event=None):
        email = self.email_var.get()
        pwd = self.password_var.get()
        error_msg = "Attention l'email n'est pas au bon format."

        email_ok = self.valid_email(email)
        if email_ok:
            p = Login.database.check_person_exist(email, pwd)
            if not p:
                showerror("Erreur", "Nous n'avons pas pu trouver votre compte.")
                return
            self.frame = home.Home(self.master, p, Login.database)
        else:
            showerror("Erreur", error_msg)
            self.clean_entry()
            self.entry_pwd.delete(0, tk.END)

    def signin(self):
        signin.SignIn(self.master, Login.database)
