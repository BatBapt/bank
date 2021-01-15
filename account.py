#!/usr/bin/env python3

import sys

from random import randint, choice
from person import Person


class Account:
    num_id = 0
    def __init__(self, account_id=None, num_account=None):
        if account_id is None:
            self._account_id = Account.num_id
            Account.num_id += 1

            self._num_account = self.gen_num_account()
            print(self._num_account)
            self._iban = "FR142004301003{}06".format(self._num_account)
        else:
            try:
                assert isinstance(account_id, int), "[Account:init] Erreur le numéro n'est pas un entier"
            except AssertionError as e:
                print(e)
                sys.exit(-1)
            self._account_id = account_id
            self._num_account = ""
            self._iban = ""

        self._owner = ""
        self._balance = 0


    # Getter
    @property
    def account_id(self):
        return self._account_id

    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance

    @property
    def num_account(self):
        return self._num_account

    @property
    def iban(self):
        return self._iban

    # Setter
    @owner.setter
    def owner(self, new_owner):
        try:
            assert isinstance(new_owner, Person), "[Account:owner.setter] Erreur ce n'est pas une personne"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._owner = new_owner
    @balance.setter
    def balance(self, amount):
        try:
            assert isinstance(amount, float), "[Account:balance.setter], Erreur le montant doit être un nombre"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._balance += amount

    @num_account.setter
    def num_account(self, num):
        try:
            assert isinstance(amount, str), "[Account:num_account.setter], Erreur le numéro de compte doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._num_account = num

    @iban.setter
    def iban(self, iban):
        try:
            assert isinstance(iban, str), "[Account:iban.setter], Erreur l'IBAN doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(1)

        self._iban = iban

    # Methods
    def __repr__(self):
        string = "Propriétaire du compte: {}\n".format(self._owner.full_name)
        string += "Solde sur le compte: {} €\n".format(self._balance)
        string += "Numéro de compte: {}\n".format(self._num_account)
        string += "IBAN: {}".format(self._iban)

        return string

    def gen_num_account(self):
        num = ""
        for i in range(7):
            num += str(randint(0, 9))
        num += choice([chr(i) for i in range(65, 91)])
        for i in range(3):
            num += str(randint(0, 9))

        return num

    def instanciate_account_from_bdd(self, param):
        try:
            assert isinstance(param, list), "[Account:instanciate_account_from_bdd] Erreur le paramètre n'est pas une liste"
            assert len(param) == 4, "[Account:instanciate_account_from_bdd] Erreur la liste n'est pas de bonne taille"
        except AssertionError as e:
            print(e)
            sys.exit(-1)

        self._owner = param[0]
        self._balance = param[1]
        self._num_account = param[2]
        self._iban = param[3]

    def transaction(self, account, amount):
        self._balance = self._balance - amount
        account.balance = amount
