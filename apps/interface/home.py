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
    import apps.interface.details as details
except ImportError as e:
    print("Home: {}".format(e))
    sys.exit(1)

class Home(tk.Frame):

    frame_bg_color = "#F0B649"
    btn_bg_color = "#4892F0"

    def __init__(self, master, perso, database):
        try:
            assert isinstance(perso, person.Person), "Erreur"
            assert isinstance(database, db.Database), "Erreur"
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
        self.frame.pack(side=tk.TOP)

        tk.Label(self.frame, text="Bienvenu {}".format(self._person.full_name), bg=Home.frame_bg_color).pack(anchor=tk.NW)
        tk.Label(self.frame, text="Voilà vos comptes: ", bg=Home.frame_bg_color).pack(anchor=tk.NW, pady=(5,0))

        deco_btn = tk.Button(self.frame, text="Se déconnecter", font=btn_font, command=self.deconnect)
        deco_btn.pack(anchor=tk.NE)

        self.account_frame = tk.Frame(self.frame, width=450, height=475, bg="blue")
        self.account_frame.pack(side=tk.TOP, pady=(10, 0))

        self.benef_frame = tk.Frame(self.frame, width=450, height=475, bg="red")
        self.benef_frame.pack(side=tk.BOTTOM, pady=(10, 0))

        self.account_tab = ttk.Treeview(self.account_frame, columns=('iban', 'name', 'solde'))

        self.benef_tab = ttk.Treeview(self.benef_frame, columns=('iban'))

        self.display_all_personnal_informations()

        self.account_tab.bind("<Double-1>", self.details)

    def details(self, event):
        item_id = self.account_tab.focus()
        item = self.account_tab.item(item_id)
        acc_iban = item['values'][0]
        acc = self.db.get_account_by_iban(acc_iban)
        details.Details(self.master, self._person, acc, self.db)

    def menu_widget(self):
        self.add_menu.add_command(label="Compte", command=self.new_account)

        self.add.configure(menu=self.add_menu)

    def deconnect(self, event=None):
        deco = askquestion("Déconnection", "Voulez vous vraiement vous déconnecter? ")
        if deco == "yes":
            login.Login(self.master)

    def display_all_personnal_informations(self):
        self.account_tab.heading('iban', text='IBAN du compte')
        self.account_tab.column('iban', width=250, stretch=tk.NO)
        self.account_tab.heading('name', text="Nom du compte")
        self.account_tab.heading('solde', text='Solde')
        self.account_tab.column('solde', width=75, stretch=tk.NO)
        self.account_tab['show'] = 'headings'
        self.account_tab.pack(pady=(10, 0))

        self.benef_tab.heading('iban', text='IBAN du compte bénéficiaire')
        self.benef_tab.column('iban', width=250, stretch=tk.NO)
        self.benef_tab['show'] = 'headings'
        self.benef_tab.pack(pady=(10, 0))


        accounts = self.db.display_perso_account(self._person.person_id)
        for acc in accounts:
            print(acc)
            self.account_tab.insert('', 'end', iid=acc.account_id, values=(acc.iban, acc.account_name, "{} €".format(acc.balance)))
            benefs = self.db.display_all_beneficiaire(acc.account_id)
            print(acc.account_id)
            print(benefs)
            for benef in benefs:
                self.benef_tab.insert('', 'end', iid=benef[0], values=(benef[2]))

    def display_all_benef_account(self):

        accounts = self.db.display_perso_account(self._person.person_id)

    def add_row_to_account_tab(self, acc):
        self.account_tab.insert('', 'end', iid=acc.account_id, values=(acc.iban, acc.account_name, "{} €".format(acc.balance), 'click on me'))

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

        self.db.insert_beneficiaire(new_account, self._person, new_account.iban)

        benefs = self.db.display_all_beneficiaire(self._person.person_id)

        print(benefs)

        top.destroy()
