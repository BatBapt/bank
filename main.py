from datetime import datetime

from account import Account
from person import Person
from database import Database


db = Database()
db.init_db()

p1 = Person()
p1.first_name = "Patrick"
p1.last_name = "LEROUX"
p1.date_birth = "04/05/1970"
p1.phone_number = "0304050607"
p1.email = "patrick@gmail.com"
c1 = Account()
c1.owner = p1
c1.balance = 950.0
"""
good = db.insert_person(p1)
if good > -1:
    db.insert_account(c1)

persons = db.display_all_person()
for person in persons:
    print("*"*40)
    print(person)

print("\n")
"""
accounts = db.display_all_account()
for account in accounts:
    print("*"*40)
    print(account)

account1 = accounts[0]
account2 = accounts[1]

virement_ok = db.transaction(account1, account2, 50.0)
if virement_ok:
    print("Virement de {}€ effectué vers le compte {}".format(50, account1.num_account))
