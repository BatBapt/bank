import sqlite3
import sys
from datetime import datetime

from person import Person
from account import Account


class Database:

    name = "mydb.db"

    def __init__(self):
        try:
            self.__conn = sqlite3.connect(Database.name)
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
            FOREIGN KEY(person_id) REFERENCES personn (id)
        );
        """

        try:
            self._cursor.execute(create_table_person)
            self._cursor.execute(create_table_account)
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

        print("Insertion correctement éffectuée. ")

        return self._cursor.lastrowid

    def insert_account(self, account):
        try:
            assert isinstance(account, Account), "[Database:insert_account] Erreur ce n'est pas un compte."
        except AssertionError as e:
            print(e)
            sys.exit(1)

        person_id = account.owner.person_id
        balance = account.balance

        req = '''INSERT INTO account(person_id,balance) VALUES (?, ?)'''

        try:
            self._cursor.execute(req, [person_id, balance])
        except sqlite3.Error as e:
            print(e)
            sys.exit(1)

        self.__conn.commit()

        print("Insertion correctement éffectuée. ")
        return self._cursor.lastrowid


    # Get Person methods

    def display_all_person(self):
        req = 'SELECT * FROM person'
        self._cursor.execute(req)
        return self._cursor.fetchall()

    def display_person_by_email(self, email):
        try:
            assert isinstance(email, str), "[Database:display_person_by_email]: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in email, "[Database:display_person_by_email]: Erreur l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT * FROM person WHERE email=?'
        self._cursor.execute(req, (email,))
        return self._cursor.fetchone()

    def display_person_by_phone(self, phone):
        try:
            assert isinstance(phone, str), "[Database:display_person_by_phone]: Erreur le numéro de téléphone doit être une chaine de caractère"
            assert len(phone) == 10, "[Database:display_person_by_phone]: Erreur le numéro de téléphone est au mauvais format"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT * FROM person WHERE phone_number=?'
        self._cursor.execute(req, (phone,))
        return self._cursor.fetchone()

    def display_person_by_first_name(self, first_name):
        try:
            assert isinstance(first_name, str), "[Personne:display_person_by_first_name]: Erreur le numéro de téléphone doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT * FROM person WHERE first_name=?'
        self._cursor.execute(req, (first_name,))
        return self._cursor.fetchall()

    def display_person_by_last_name(self, last_name):
        try:
            assert isinstance(last_name, str), "[Personne:display_person_by_first_name]: Erreur le numéro de téléphone doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        req = 'SELECT * FROM person WHERE last_name=?'
        self._cursor.execute(req, (last_name,))
        return self._cursor.fetchall()

    # Get Account methods
    def display_all_account(self):
        req = 'SELECT * FROM account'
        self._cursor.execute(req)
        rows = self._cursor.fetchall()
        return rows
