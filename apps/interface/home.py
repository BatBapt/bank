import sys
try:
    import tkinter as tk
    import tkinter.ttk as ttk

    import apps.util.person as person
    import apps.database.database as db
except ImportError as e:
    print("Home: {}".format(e))
    sys.exit(1)

class Home(tk.Frame):

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

        menu_frame = tk.Frame(self.master, width=900, height=25, bg="red")
        menu_frame.pack(side=tk.TOP, anchor=tk.W)

        self.add = tk.Menubutton(menu_frame, text="Ajouter un..", width=20, borderwidth=2)
        self.add.pack(side=tk.LEFT, fill=tk.X)

        self.add_menu = tk.Menu(self.add, tearoff=0)

        self.menu_widget()

        self.frame = tk.Frame(self.master, width=900, height=475)
        self.frame.pack()

        self.welcome()

        self.account_tab = ttk.Treeview(self.frame, columns=('numeroCompte', 'solde', 'informations'))

        self.benef_tab = ttk.Treeview(self.frame, columns=('beneficiaire', 'iban', 'virement'))


        self.display_all_personnal_account()

    def menu_widget(self):
        self.add_menu.add_command(label="Compte")
        self.add_menu.add_command(label="Bénéficiaire")

        self.add.configure(menu=self.add_menu)

    def welcome(self):
        tk.Label(self.frame, text="Bienvenu {}".format(self._person.full_name)).pack()
        tk.Label(self.frame, text="Voilà vos comptes: ").pack()

    def display_all_personnal_account(self):
        self.account_tab.heading('numeroCompte', text='Numéro du compte')
        self.account_tab.heading('solde', text='Solde')
        self.account_tab.heading('informations', text="Informations")
        self.account_tab['show'] = 'headings'
        self.account_tab.pack(pady=(5, 5))
        accounts = self.db.display_perso_account(self._person.person_id)
        for account in accounts:
            self.account_tab.insert('', 'end', iid=account.account_id, values=(account.num_account, "{} €".format(account.balance), 'click on me'))

    def display_all_benef_account(self):
        # benef = self.db.display_all_beneficiaire(self.)
        pass

if __name__ == '__main__':
    db = Database()
    p = db.select_person_by_id(1)

    app = tk.Tk()
    app.geometry("900x500+500+200")
    home = Home(app, p, db)
    app.mainloop()
