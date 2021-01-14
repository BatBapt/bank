import sqlite3
import sys
from datetime import datetime

from person import Person
from account import Account


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
            account_id INTEGER NOT NULL,
            iban VARCHAR(27) NOT NULL UNIQUE,
            FOREIGN KEY(account_id) REFERENCES account (id)
        );
        """

        try:
            self._cursor.execute(create_table_person)
            self._cursor.execute(create_table_account)
            self._cursor.execute(create_table_beneficiaire)
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

    # Insert methods
    def insert_person(self, owner):
        try:
            assert isinstance(owner, Person), "[Datebase:insert_person]: Erreur le propriétaire n'est pas une personne"
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
            print("Erreur cet email existe déjà.")
            return -1
        if self.check_phone_exists(phone_number) is not None:
            print("Erreur ce numéro de téléphone existe déjà.")
            return -1


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

        # print("Insertion de {} correctement éffectuée.".format(owner.full_name))

        return self._cursor.lastrowid

    def insert_account(self, account):
        try:
            assert isinstance(account, Account), "[Database:insert_account] Erreur ce n'est pas un compte."
        except AssertionError as e:
            print(e)
            sys.exit(1)

        person_id = self.get_id_by_email(account.owner.email)
        balance = account.balance
        num_account = account.num_account
        iban = account.iban

        num_account = self.check_num_account(account)

        req = '''
        INSERT INTO account(
            person_id,
            balance,
            num_account,
            iban
            ) VALUES (?, ?, ?, ?)
        '''

        try:
            self._cursor.execute(req, [person_id, balance, num_account, iban])
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

        self.__conn.commit()

        # print("Insertion du nouveau compte correctement éffectuée.")
        return self._cursor.lastrowid

    def insert_beneficiaire(self, account, iban):
        try:
            assert isinstance(account, Account), "[Database:insert_beneficiaire] Erreur ce n'est pas un compte."
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

    # Get Person methods
    def display_all_person(self):
        req = 'SELECT * FROM person'
        self._cursor.execute(req)
        rows = self._cursor.fetchall()
        list_person = []
        for row in rows:
            row = list(row)
            p = Person(row[0])
            p.instanciate_perso_from_bdd(list(row[1:]))
            list_person.append(p)
        return list_person

    def select_person_by_id(self, person_id):
        req = 'SELECT * FROM person WHERE id=?'
        self._cursor.execute(req, (person_id, ))
        row = self._cursor.fetchone()
        row = list(row)
        p = Person(row[0])
        p.instanciate_perso_from_bdd(row[1:])
        return p

    def display_person_by_email(self, email):
        try:
            assert isinstance(email, str), "[Database:display_person_by_email]: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in email, "[Database:display_person_by_email]: Erreur l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT * FROM person WHERE email=?'
        self._cursor.execute(req, (email,))
        row = self._cursor.fetchone()
        row = list(row)
        p = Person(row[0])
        p.instanciate_perso_from_bdd(row[1:])
        return p

    def display_person_by_phone(self, phone):
        try:
            assert isinstance(phone, str), "[Database:display_person_by_phone]: Erreur le numéro de téléphone doit être une chaine de caractère"
            assert len(phone) == 10, "[Database:display_person_by_phone]: Erreur le numéro de téléphone est au mauvais format"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT * FROM person WHERE phone_number=?'
        self._cursor.execute(req, (phone,))
        rrow = self._cursor.fetchone()
        row = list(row)
        p = Person(row[0])
        p.instanciate_perso_from_bdd(row[1:])
        return p

    def display_person_by_first_name(self, first_name):
        try:
            assert isinstance(first_name, str), "[Personne:display_person_by_first_name]: Erreur le numéro de téléphone doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT * FROM person WHERE first_name=?'
        self._cursor.execute(req, (first_name,))
        rows = self._cursor.fetchall()
        list_person = []
        for row in rows:
            row = list(row)
            p = Person(row[0])
            p.instanciate_perso_from_bdd(list(row[1:]))
            list_person.append(p)
        return list_person

    def display_person_by_last_name(self, last_name):
        try:
            assert isinstance(last_name, str), "[Personne:display_person_by_first_name]: Erreur le numéro de téléphone doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT * FROM person WHERE last_name=?'
        self._cursor.execute(req, (last_name,))
        rows = self._cursor.fetchall()
        list_person = []
        for row in rows:
            row = list(row)
            p = Person(row[0])
            p.instanciate_perso_from_bdd(list(row[1:]))
            list_person.append(p)
        return list_person

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

    # Get Account methods
    def display_all_account(self):
        req = 'SELECT * FROM account'
        self._cursor.execute(req)
        rows = self._cursor.fetchall()
        list_account = []
        for row in rows:
            row = list(row)
            row[1] = self.select_person_by_id(row[0])
            c = Account(row[0])
            c.instanciate_account_from_bdd(row[1:])
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

    # Get beneficiaire methods
    def display_all_beneficiaire(self, account_id):
        req = 'SELECT * FROM beneficiaire WHERE account_id=?'
        self._cursor.execute(req, (account_id, ))
        return self._cursor.fetchall()

    def check_iban_exist(self, table, id, iban):
        req = 'SELECT iban FROM {} WHERE iban=? AND id=?'.format(table)
        self._cursor.execute(req, (iban, id, ))
        return self._cursor.fetchone()
