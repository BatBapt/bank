#!/usr/bin/env python3


class Account:
    account_id = 0

    def __init__(self, owner, initial_depo):
        self.__account_id = Account.account_id
        self.owner = owner
        self.__solde = initial_depo

        Account.account_id += 1

    @property
    def solde(self):
        return self.__solde

    @solde.setter
    def solde(self, amount):
        self.__solde += amount


c1 = Account("Baptiste", 50)
