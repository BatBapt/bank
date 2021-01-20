import sys
try:
    from tkinter import font
    from tkinter.messagebox import askquestion
    import tkinter as tk
    import tkinter.ttk as ttk


    import apps.util.person as person
    import apps.util.account as account

    import apps.database.database as db

    import apps.interface.login as login
except ImportError as e:
    print("Home: {}".format(e))
    sys.exit(1)

class Home(tk.Frame):

    frame_bg_color = "#F0B649"
    btn_bg_color = "#4892F0"

    def __init__(self, master, perso, database):

        try:
            assert isinstance(perso, person.Person), "Erreur"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self.master = master
        self._person = perso
        self.db = database
        self.master.title("Vos comptes")
        tk.Frame.__init__(self, self.master)

        for widget in self.master.winfo_children():
            widget.destroy()

        btn_font = font.Font(family='Helvetica', name='myFont', size=12, weight='bold')

        menu_frame = tk.Frame(self.master, width=850, height=25)
        menu_frame.pack(side=tk.TOP, anchor=tk.W)

        self.add = tk.Menubutton(menu_frame, text="Ajouter un..", font=btn_font, width=20, borderwidth=2)
        self.add.pack(side=tk.LEFT, fill=tk.X)

        self.add_menu = tk.Menu(self.add, tearoff=0)

        self.menu_widget()

        self.frame = tk.Frame(self.master, width=900, height=475, bg=Home.frame_bg_color)
        self.frame.pack(pady=(10, 0))

        self.welcome()

        self.account_tab = ttk.Treeview(self.frame, columns=('numeroCompte', 'name', 'solde', 'informations'))

        self.display_all_personnal_account()

        deco_btn = tk.Button(self.frame, text="Se déconnecter", font=btn_font, command=self.deconnect)
        deco_btn.pack(pady=(20, 20))

    def menu_widget(self):
        self.add_menu.add_command(label="Compte", command=self.new_account)

        self.add.configure(menu=self.add_menu)

    def welcome(self):
        tk.Label(self.frame, text="Bienvenu {}".format(self._person.full_name), bg=Home.frame_bg_color).pack()
        tk.Label(self.frame, text="Voilà vos comptes: ", bg=Home.frame_bg_color).pack(pady=(5,5))

    def deconnect(self, event=None):
        deco = askquestion("Déconnection", "Voulez vous vraiement vous déconnecter? ")
        if deco == "yes":
            login.Login(self.master)

    def display_all_personnal_account(self):
        self.account_tab.heading('numeroCompte', text='Numéro du compte')
        self.account_tab.heading('name', text="Nom du compte")
        self.account_tab.heading('solde', text='Solde')
        self.account_tab.heading('informations', text="Informations")
        self.account_tab['show'] = 'headings'
        self.account_tab.pack(pady=(10, 0))
        accounts = self.db.display_perso_account(self._person.person_id)
        for acc in accounts:
            self.account_tab.insert('', 'end', iid=acc.account_id, values=(acc.num_account, acc.account_name, "{} €".format(acc.balance), 'click on me'))

    def add_row_to_account_tab(self, acc):
        self.account_tab.insert('', 'end', iid=acc.account_id, values=(acc.num_account, acc.account_name, "{} €".format(acc.balance), 'click on me'))

    def new_account(self, event=None):
        top = tk.Toplevel(self.master)
        top.title("Ouverture d'un nouveau compte")
        top.geometry("400x200+400+400")
        top.configure(background="#4892F0")

        top_frame = tk.Frame(top, width=400, height=500, bg=Home.frame_bg_color)
        top_frame.pack()

        tk.Label(top_frame, text="Nom du compte: ", bg=Home.frame_bg_color).pack()
        name_var = tk.StringVar()
        name_entry = tk.Entry(top_frame, textvariable=name_var, width=30)
        name_entry.pack()

        tk.Label(top_frame, text="Premier apport sur le compte: ", bg=Home.frame_bg_color).pack()
        balance_var = tk.DoubleVar()
        balance_entry = tk.Entry(top_frame, textvariable=balance_var, width=30)
        balance_entry.pack()

        error_lab = tk.Label(top_frame, bg=Home.frame_bg_color)
        error_lab.pack()

        create_btn = tk.Button(top_frame, text="Créer le compte", command=lambda name=name_var,
            balance=balance_var, top_lvl=top, error_lab=error_lab: self.create_account(name=name, balance=balance, error_lab=error_lab, top_lvl=top_lvl))

        create_btn.pack()

    def create_account(self, **kwargs):
        try:
            name = kwargs['name'].get()
            balance = kwargs['balance'].get()
            error_lab = kwargs['error_lab']
            top = kwargs['top_lvl']
        except KeyError as e:
            error_lab['text'] = "Il manque un champ"
            return

        if len(name) == 0:
            error_lab['text'] = "Erreur: le nom du compte ne peut pas être vide."
            return

        if balance <= 0:
            error_lab['text'] = "Erreur: le premier apport ne peut pas être négatif ou nul."
            return

        new_account = account.Account(balance, name)
        new_account.owner = self._person
        self.db.insert_account(new_account)
        self.add_row_to_account_tab(new_account)

        top.destroy()
