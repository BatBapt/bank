import sys
try:
    import tkinter as tk
    import tkinter.ttk as ttk

    import apps.interface.home as home

    import apps.util.person as person
    import apps.util.account as account

    import apps.database.database as db
except ImportError as e:
    print("Details: {}".format(e))
    sys.exit(1)


class Details(tk.Frame):

    def __init__(self, master, perso, acc, database):
        try:
            assert isinstance(perso, person.Person), "Erreur"
            assert isinstance(acc, account.Account), "Erreur"
            assert isinstance(database, db.Database), "Erreur"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self.master = master
        self._perso = perso
        self._acc = acc
        self._db = database

        self.master.title("Détail du compte")
        tk.Frame.__init__(self, self.master)

        for widget in self.master.winfo_children():
            widget.destroy()

        self.frame = tk.Frame(self.master, width=900, height=500, bg="red")
        self.frame.pack()

        self.histo_tab = ttk.Treeview(self.frame, columns=("from", "to", "amount", 'date'))

        self.display_all_benef_account()

    def display_all_benef_account(self):

        histo = self._db.display_all_historic(self._acc.account_id)
