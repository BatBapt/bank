import sys
try:
    import sqlite3
    import datetime
    import apps.util.person as person
    import apps.util.account as account
except ImportError as e:
    print("Database: {}".format(e))
    sys.exit(1)


class Database:
    __name = "mydb.db"
    def __init__(self):
        try:
            self.__conn = sqlite3.connect(Database.__name)
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

        self._cursor = self.__conn.cursor()

    def init_db(self):
        create_table_person = """
        CREATE TABLE IF NOT EXISTS person(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name VARCHAR(100) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            date_birth DATE NOT NULL,
            phone_number VARCHAR(10) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE
        );
        """

        create_table_account = """
        CREATE TABLE IF NOT EXISTS account(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            person_id INTEGER NOT NULL,
            balance REAL NOT NULL,
            num_account CHAR(11) NOT NULL UNIQUE,
            iban VARCHAR(27) NOT NULL UNIQUE,
            FOREIGN KEY(person_id) REFERENCES personn (id)
        );
        """

        create_table_beneficiaire = """
        CREATE TABLE IF NOT EXISTS beneficiaire(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            iban VARCHAR(27) NOT NULL UNIQUE,
            FOREIGN KEY(person_id) REFERENCES person (id)
        );
        """

        create_table_historic = """
        CREATE TABLE IF NOT EXISTS historic(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_from_id INTEGER NOT NULL,
            account_to_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date DATETIME NOT NULL,
            FOREIGN KEY(account_from_id) REFERENCES account (id),
            FOREIGN KEY(account_to_id) REFERENCES account (id)
        );
        """

        try:
            self._cursor.execute(create_table_person)
            self._cursor.execute(create_table_account)
            self._cursor.execute(create_table_beneficiaire)
            self._cursor.execute(create_table_historic)
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

    # Insert methods
    def insert_person(self, owner):
        try:
            assert isinstance(owner, person.Person), "[Datebase:insert_person]: Erreur le propriétaire n'est pas une personne"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        first_name = owner.first_name
        last_name = owner.last_name
        password = owner.password
        date_birth = owner.date_birth
        phone_number = owner.phone_number
        email = owner.email



        if self.check_email_exists(email) is not None:
            error_msg = "Erreur cet email existe déjà."
            return False, error_msg

        if self.check_phone_exists(phone_number) is not None:
            error_msg = "Erreur ce numéro de téléphone existe déjà"
            return False, error_msg


        req = '''
        INSERT INTO person(
            last_name,
            first_name,
            password,
            date_birth,
            phone_number,
            email)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        try:
            self._cursor.execute(req, [
                last_name,
                first_name,
                password,
                date_birth,
                phone_number,
                email
            ])
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

        self.__conn.commit()

        success_msg = "Votre profil a bien été ajouté. Veuillez vous connecter maintenant."
        return True, success_msg

    def insert_account(self, acc):
        try:
            assert isinstance(acc, account.Account), "[Database:insert_account] Erreur ce n'est pas un compte."
        except AssertionError as e:
            print(e)
            sys.exit(1)

        person_id = self.get_id_by_email(acc.owner.email)
        balance = acc.balance
        num_account = acc.num_account
        iban = acc.iban
        name = acc.account_name

        num_account = self.check_num_account(acc)

        req = '''
        INSERT INTO account(
            person_id,
            name,
            balance,
            num_account,
            iban
            ) VALUES (?, ?, ?, ?, ?)
        '''

        try:
            self._cursor.execute(req, [person_id, name, balance, num_account, iban])
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

        self.__conn.commit()

        return self._cursor.lastrowid

    def insert_beneficiaire(self, account, iban):
        try:
            assert isinstance(account, account.Account), "[Database:insert_beneficiaire] Erreur ce n'est pas un compte."
            assert isinstance(iban, str), "[Database:insert_beneficiaire] Erreur l'IBAN n'est pas une chaine de caractère"
            assert len(iban) == 27, "[Database:insert_beneficiaire] Erreur l'IBAN est au mauvais format"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        account_id = account.account_id
        if self.check_iban_exist("beneficiaire", account_id, iban) is not None:
            print("Erreur ce bénéficiaire est déjà présent")
            return -1

        req = '''
        INSERT INTO beneficiaire(
            account_id,
            iban
            ) VALUES (?, ?)
        '''

        try:
            self._cursor.execute(req, (account_id, iban, ))
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

        self.__conn.commit()

        print("Bénéficiaire ajouté")
        return self._cursor.lastrowid

    def insert_historic(self, acc_from_id, acc_to_id, amount):
        try:
            assert isinstance(acc_from_id, int), "[Database:insert_historic] Erreur le compte d'origine n'est pas un entier"
            assert isinstance(acc_to_id, int), "[Database:insert_historic] Erreur le compte bénéficiaire n'est pas un entier"
            assert isinstance(amount, float), "[Database:insert_historic] Erreur le montant n'est pas un réel"
        except AssertionError as e:
            print(e)
            sys.exit(1)


        req = '''
        INSERT INTO historic (account_from_id, account_to_id, amount, date)
        VALUES (?, ?, ?, ?)
        '''

        date = datetime.datetime.now()
        try:
            self._cursor.execute(req, (acc_from_id, acc_to_id, amount, date))
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

        self.__conn.commit()

        return self._cursor.lastrowid


    # Person methods
    def display_all_person(self):
        req = 'SELECT * FROM person'
        self._cursor.execute(req)
        rows = self._cursor.fetchall()
        list_person = []
        for row in rows:
            row = list(row)
            p = person.Person(row[0])
            p.instanciate_perso_from_bdd(row[1:])
            list_person.append(p)
        return list_person

    def check_person_exist(self, email, pwd):
        req = '''
        SELECT *
        FROM person
        WHERE email = ? AND password = ?
        '''
        self._cursor.execute(req, (email, pwd, ))
        row = self._cursor.fetchone()
        if row is None:
            return False
        row = list(row)
        p = person.Person(row[0])
        p.instanciate_perso_from_bdd(row[1:])
        return p

    def select_person_by_id(self, person_id):
        req = 'SELECT * FROM person WHERE id=?'
        self._cursor.execute(req, (person_id, ))
        row = self._cursor.fetchone()
        if row is None:
            return False
        row = list(row)
        p = person.Person(row[0])
        p.instanciate_perso_from_bdd(row[1:])
        return p

    def display_person_by_iban(self, iban):
        req = '''
        SELECT last_name, first_name
        FROM person
        INNER JOIN account
        ON account.person_id = person.id
        WHERE iban = ?
        '''
        self._cursor.execute(req, (iban, ))
        return self._cursor.fetchone()

    def check_email_exists(self, email):
        try:
            assert isinstance(email, str), "[Database:display_person_by_email]: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in email, "[Database:display_person_by_email]: Erreur l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT email FROM person WHERE email=?'
        self._cursor.execute(req, (email, ))
        return self._cursor.fetchone()

    def check_phone_exists(self, phone):
        try:
            assert isinstance(phone, str), "[Database:display_person_by_phone]: Erreur le numéro de téléphone doit être une chaine de caractère"
            assert len(phone) == 10, "[Database:display_person_by_phone]: Erreur le numéro de téléphone est au mauvais format"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT phone_number FROM person WHERE phone_number=?'
        self._cursor.execute(req, (phone, ))
        return self._cursor.fetchone()

    def get_id_by_email(self, email):
        try:
            assert isinstance(email, str), "[Database:display_person_by_email]: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in email, "[Database:display_person_by_email]: Erreur l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT id FROM person WHERE email=?'
        self._cursor.execute(req, (email, ))
        row = self._cursor.fetchone()
        return row[0]

    # Account methods

    def display_perso_account(self, person_id):
        req = '''
        SELECT *
        FROM account
        WHERE person_id = ?
        '''
        self._cursor.execute(req, (person_id, ))
        rows = self._cursor.fetchall()
        list_account = []
        for row in rows:
            row = list(row)
            row[2] = self.select_person_by_id(row[0])
            c = account.Account(row[0], row[1])
            c.instanciate_account_from_bdd(row[2:])
            list_account.append(c)
        return list_account

    def get_all_num_account(self):
        req = 'SELECT num_account FROM account'
        self._cursor.execute(req)
        return self._cursor.fetchall()

    def get_all_iban(self):
        req = 'SELECT iban FROM account'
        self._cursor.execute(req)
        return self._cursor.fetchall()

    def check_num_account(self, account):
        nums = self.get_all_num_account()
        for num in nums:
            if account.num_account in num:
                account.num_account = account.gen_num_account()

        num_account = account.num_account
        return num_account

    def get_account_by_iban(self, iban):
        req = '''
        SELECT *
        FROM account
        WHERE iban=?
        '''
        self._cursor.execute(req, (iban, ))
        row = list(self._cursor.fetchone())
        c = account.Account(row[0])
        row[1] = self.select_person_by_id(row[1])
        c.instanciate_account_from_bdd(row[1:])
        return c

    def transaction(self, account1, account2, amount):
        iban_account1 = account1.iban
        account_from = self.get_account_by_iban(iban_account1)

        iban_account2 = account2.iban
        iban_in_bene = self.check_iban_exist("beneficiaire", account_from.account_id, iban_account2)
        if iban_in_bene is None:
            print("Virement impossible car le bénéficiaire n'est pas dans votre liste")
            return False
        account_to = self.get_account_by_iban(iban_account2)
        account_from.transaction(account_to, amount)
        self.update_balance(account_from.balance, iban_account1)
        self.update_balance(account_to.balance, iban_account2)


        self.insert_historic(account_from.account_id, account_to.account_id, amount)

        return True

    def update_balance(self, amount, iban):
        req = '''
        UPDATE  account
        SET balance = ?
        WHERE iban = ?
        '''
        self._cursor.execute(req, (amount, iban))
        self.__conn.commit()

    # Beneficiaire methods
    def display_all_beneficiaire(self, account_id):
        req = 'SELECT * FROM beneficiaire WHERE person_id=?'
        self._cursor.execute(req, (account_id, ))
        return self._cursor.fetchall()

    def check_iban_exist(self, table, id, iban):
        req = 'SELECT iban FROM {} WHERE iban=? AND id=?'.format(table)
        self._cursor.execute(req, (iban, id, ))
        return self._cursor.fetchone()

    # Historic methods

    def display_all_historic(self, account_id):
        req = 'SELECT * FROM historic WHERE account_from_id=?'
        self._cursor.execute(req, (account_id, ))
        return self._cursor.fetchall()
