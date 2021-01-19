import sys
try:
    import tkinter as tk
    from tkinter import font
    from tkinter.messagebox import showerror, showinfo
    from tkcalendar import Calendar, DateEntry
    from datetime import datetime
    import re

    import apps.interface.login as login
    import apps.util.person as person
    import apps.database.database as db
except ImportError as e:
    print("Signin: {}".format(e))
    sys.exit(1)


class SignIn(tk.Frame):

    frame_bg_color = "#F0B649"
    btn_bg_color = "#4892F0"

    def __init__(self, master, database):
        self.master = master
        self.master.title("Enregistrement")
        self.database = database
        tk.Frame.__init__(self, self.master)

        btn_font = font.Font(family='Helvetica', name='myFont', size=12, weight='bold')

        for widget in self.master.winfo_children():
            widget.destroy()

        self.frame = tk.Frame(self.master, width=900, height=800, bg=SignIn.frame_bg_color)
        self.frame.pack(pady=(25, 25))
        self.frame.focus_set()

        tk.Label(self.frame, text="Création d'un compte", bg=SignIn.frame_bg_color).pack(pady=(20, 20))

        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.date_birth = ""
        self.phone_number = tk.StringVar()
        self.email = tk.StringVar()

        tk.Label(self.frame, text="Entrez votre prénom: ", bg=SignIn.frame_bg_color).pack()
        self.first_name_entry = tk.Entry(self.frame, textvariable=self.first_name, width=30)
        self.first_name_entry.insert(0, 'Dupont')
        self.first_name_entry.pack(pady=(0, 20))

        tk.Label(self.frame, text="Entrez votre nom de famille: ", bg=SignIn.frame_bg_color).pack()
        self.last_name_entry = tk.Entry(self.frame, textvariable=self.last_name, width=30)
        self.last_name_entry.insert(0, 'DUPONT')
        self.last_name_entry.pack(pady=(0, 20))

        self.date_birth_btn = tk.Button(self.frame, text="Vous êtes né(e) le:", command=self.choose_date_birth, bg=SignIn.btn_bg_color, font=btn_font)
        self.date_birth_btn.pack()
        self.date_label = tk.Label(self.frame, bg=SignIn.frame_bg_color)
        self.date_label.pack(pady=(0, 20))

        tk.Label(self.frame, text="Entrez votre numéro de téléphone: ", bg=SignIn.frame_bg_color).pack()
        self.phone_number_entry = tk.Entry(self.frame, textvariable=self.phone_number, width=30)
        self.phone_number_entry.insert(0, '0102030405')
        self.phone_number_entry.pack(pady=(0, 20))

        tk.Label(self.frame, text="Entrez votre email: ", bg=SignIn.frame_bg_color).pack()
        self.email_entry = tk.Entry(self.frame, textvariable=self.email, width=30)
        self.email_entry.insert(0, 'dupont@gmail.com')
        self.email_entry.pack(pady=(0, 20))

        self.siginin_btn = tk.Button(self.frame, text="S'inscrire", command=self.signin, font=btn_font, bg=SignIn.btn_bg_color, width=30)
        self.siginin_btn.pack()

        self.date_birth_btn.bind('<Enter>', func=lambda e, button=self.date_birth_btn: self.hover(button=button, event=e))
        self.date_birth_btn.bind('<Leave>', func=lambda e, button=self.date_birth_btn: self.unhover(button=button, event=e))

        self.siginin_btn.bind('<Enter>', func=lambda e, button=self.siginin_btn: self.hover(button=button, event=e))
        self.siginin_btn.bind('<Leave>', func=lambda e, button=self.siginin_btn: self.unhover(button=button, event=e))

    def hover(self, button, event):
        button.config(activebackground=SignIn.frame_bg_color)
        button.config(activeforeground=SignIn.btn_bg_color)

    def unhover(self, button, event):
        button.config(activebackground=SignIn.frame_bg_color)
        button.config(activeforeground=SignIn.btn_bg_color)

    def has_number(self, string):
        return bool(re.search(r"\d", string))

    def valid_email(self, email):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

    def choose_date_birth(self):
        top = tk.Toplevel(self.master)

        tk.Label(top, text="Sélectionnez votre date de naissance: ").pack()

        cal = Calendar(top, width=12)
        cal.pack()

        date_btn = tk.Button(top, text='Valider la saisie', command=lambda date=cal, top_lvl=top:
            self.pick_date(date=date, top_lvl=top_lvl))
        date_btn.pack()

    def pick_date(self, **kwargs):
        top_lvl = kwargs['top_lvl']
        date = kwargs['date'].selection_get()
        date_now = datetime.now()
        year_min = date_now.year - 18
        if date.year >= year_min:
            showerror("Erreur", "Vous n'avez pas l'âge requis pour ouvrir un compte")
        else:
            date = date.strftime("%d/%m/%Y")
            self.date_birth = date
            top_lvl.destroy()
            self.date_label['text'] = "Date de naissance: {}".format(date)

    def signin(self, event=None):
        first_name = self.first_name.get().capitalize()
        last_name = self.last_name.get().upper()
        date_birth = self.date_birth
        phone = self.phone_number.get()
        email = self.email.get()

        if len(first_name) == 0:
            showerror("Erreur", "Le prénom n'est pas bon.")
            return
        first_name_has_number = self.has_number(first_name)
        if first_name_has_number:
            showerror("Erreur", "Le prénom contient des chiffres.")
            return

        if len(last_name) == 0:
            showerror("Erreur", "Le prénom n'est pas bon.")
            return
        last_name_has_number = self.has_number(last_name)
        if last_name_has_number:
            showerror("Erreur", "Le nom de famille contient des chiffres.")
            return

        aux_phone = phone
        if len(phone) != 10:
            showerror("Erreur", "Le numéro de téléphone n'est pas bon.")
            return
        else:
            try:
                phone = int(phone)
            except ValueError:
                showerror("Erreur", "Le numéro de téléphone n'est pas bon.")
                return
        phone = aux_phone

        email_ok = self.valid_email(email)
        if not email_ok:
            showerror("Erreur", "L'email n'est pas au bon format.")

        perso = person.Person()
        perso.first_name = first_name
        perso.last_name = last_name
        perso.date_birth = date_birth
        perso.phone_number = phone
        perso.email = email
        print(perso.password)

        insert = self.database.insert_person(perso)
        if insert[0]:
            showinfo("Succès", insert[1])
            login.Login(self.master)
        else:
            showerror("Erreur", insert[1])
