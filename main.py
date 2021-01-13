from datetime import datetime

from account import Account
from person import Person
from database import Database


db = Database()
db.init_db()

"""
p1 = Person("Paul", "LEROUX", "17-01-2001", "0203040506", "paul@gmail.com")
c1 = Account(p1, 75.0)
db.insert_person(p1)
db.insert_account(c1)

p2 = Person("Baptiste", "LEROUX", "23-07-1999", "0102030405", "baptiste@gmail.com")
c2 = Account(p2, 75.0)
db.insert_person(p2)
db.insert_account(c2)
"""

persons = db.display_all_person()
for person in persons:
    print(person)
    print("\n")
