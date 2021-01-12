#!/usr/bin/env python3
import sys


class Person:
    person_id = 0

    def __init__(self, first_name, last_name, date_birth, phone_number, email):
        try:
            assert isinstance(first_name, str), "{Personne:init}: Erreur le prénom le doit être une chaine de caractère"
            assert isinstance(last_name, str), "{Personne:init}: Erreur le nom de famille doit être une chaine de caractère"
            assert isinstance(date_birth, str), "{Personne:init}: Erreur la date de naissance doit être une chaine de caractère"
            assert len(date_birth) == 10, "{Personne:init}: Erreur la date de naissance est au mauvais format"
            assert isinstance(phone_number, str), "{Personne:init}: Erreur le numéro de téléphone doit être une chaine de caractère"
            assert len(phone_number) == 10, "{Personne:init}: Erreur le numéro de téléphone est au mauvais format"
            assert isinstance(email, str), "{Personne:init}: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in email, "{Personne:init}: Erreur l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self.__person_id = Person.person_id
        self._first_name = first_name
        self._last_name = last_name
        self._date_birth = date_birth
        self._phone_number = phone_number
        self._email = email

        Person.person_id += 1

    # Getter

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def bate_birth(self):
        return self._date_birth

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def email(self):
        return self._email

    # Setter

    @phone_number.setter
    def phone_number(self, new_phone):
        try:
            assert isinstance(phone_number, str), "{Personne:phone:setter}: Erreur le numéro de téléphone doit être une chaine de caractère"
            assert len(phone_number) == 10, "{Personne:phone:setter}: Erreur le numéro de téléphone est au mauvais format"
        except AssertionError as e:
            print(e)
            sys.exit(1)

    def email(self, new_email):
        try:
            assert isinstance(email, str), "{Personne:email:setter}: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in email, "{Personne}: Personne:email:setter l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(1)

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
