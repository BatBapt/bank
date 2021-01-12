#!/usr/bin/env python3

import sys

from person import Person


class Account:
    account_id = 0

    def __init__(self, owner, initial_depo):
        try:
            assert isinstance(owner, Person), "{Accout:init}: Erreur le propriétaire n'est pas une personne"
            assert isinstance(initial_depo, float), "{Account:init} Erreur le premier versement doit être un nombre"
            assert initial_depo >= 0, "{Account:init} Erreur le nombre doit être positif ou nul"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self.__account_id = Account.account_id
        self.owner = owner
        self._solde = initial_depo

        Account.account_id += 1

    @property
    def solde(self):
        return self._solde

    @solde.setter
    def solde(self, amount):
        try:
            assert isinstance(amount, float), "{Account:solde.setter}, Erreur le montant doit être un nombre"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._solde += amount

    def __repr__(self):
        string = "Propriétaire du compte {}: {}\n".format(self.__account_id, self.owner.full_name)
        string += "Solde sur le compte: {} €".format(self._solde)

        return string
