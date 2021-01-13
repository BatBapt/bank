#!/usr/bin/env python3

import sys

from person import Person


class Account:

    def __init__(self, owner, initial_depo):
        try:
            assert isinstance(owner, Person), "{Accout:init}: Erreur le propriétaire n'est pas une personne"
            assert isinstance(initial_depo, float), "{Account:init} Erreur le premier versement doit être un nombre"
            assert initial_depo >= 0, "{Account:init} Erreur le nombre doit être positif ou nul"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self._owner = owner
        self._balance = initial_depo


    # Getter

    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance


    @property
    def password(self):
        return self._password

    # Setter

    @balance.setter
    def balance(self, amount):
        try:
            assert isinstance(amount, float), "{Account:solde.setter}, Erreur le montant doit être un nombre"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._balance += amount

    # Methods

    def __repr__(self):
        string = "Propriétaire du compte: {}\n".format(self._owner.full_name)
        string += "Solde sur le compte: {} €".format(self._solde)

        return string
