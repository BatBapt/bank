#!/usr/bin/env python3
import sys
from random import choice, randint
from datetime import datetime


class Person:
    num_id = 0
    def __init__(self, first_name, last_name, date_birth, phone_number, email):
        try:
            assert isinstance(first_name, str), "[Personne:init]: Erreur le prénom le doit être une chaine de caractère"
            assert isinstance(last_name, str), "[Personne:init]: Erreur le nom de famille doit être une chaine de caractère"
            assert isinstance(date_birth, str), "[Personne:init]: Erreur la date de naissance n'est pas une date"
            assert isinstance(phone_number, str), "[Personne:init]: Erreur le numéro de téléphone doit être une chaine de caractère"
            assert len(phone_number) == 10, "[Personne:init]: Erreur le numéro de téléphone est au mauvais format"
            assert isinstance(email, str), "[Personne:init]: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in email, "[Personne:init]: Erreur l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self._person_id = Person.num_id

        self._first_name = first_name
        self._last_name = last_name
        self._password = self.gen_password_random()
        self._date_birth = date_birth
        self._phone_number = phone_number
        self._email = email

        Person.num_id += 1



    # Getter
    @property
    def person_id(self):
        return self._person_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def password(self):
        return self._password

    @property
    def date_birth(self):
        return self._date_birth

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def email(self):
        return self._email

    # Setter
    @password.setter
    def password(self, new_pwd):
        try:
            assert isinstance(new_pwd, str), "[Personne:password.setter] Erreur le mot de passe doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self._password = new_pwd


    @phone_number.setter
    def phone_number(self, new_phone):
        try:
            assert isinstance(phone_number, str), "[Personne:phone:setter]: Erreur le numéro de téléphone doit être une chaine de caractère"
            assert len(phone_number) == 10, "[Personne:phone:setter]: Erreur le numéro de téléphone est au mauvais format"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self._phone_number = new_phone

    @email.setter
    def email(self, new_email):
        try:
            assert isinstance(email, str), "[Personne:email:setter]: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in email, "[Personne:email:setter] l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self._email = new_email

    # Methods
    def __repr__(self):
        string = "{} {} né(e) le {}.\nNuméro de téléphone: {}. Adresse mail: {}".format(
            self._last_name,
            self._first_name,
            self._date_birth,
            self._phone_number,
            self._email
        )
        return string

    @property
    def full_name(self):
        return self._last_name + " " + self._first_name



    def gen_password_random(self):
        alphabet_min = [ chr(i) for i in range(97,123) ]
        alphabet_maj = [ chr(i) for i in range(65,91) ]
        chiffres = [ chr(i) for i in range(48,58) ]
        caracteres_speciaux = ['%', '_', '-', '!', '$', '^', '&', '#', '(', ')', '[', ']', '=', '@']

        alphabet = {0: alphabet_min, 1: alphabet_maj, 2: chiffres}
        password = ""
        for i in range(15):
            key = randint(0, 2)
            password += choice(alphabet[key])
        return password
