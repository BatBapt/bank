from datetime import datetime

from account import Account
from person import Person
from database import Database


db = Database()
db.init_db()

p1 = Person()
p1.first_name = "Paul"
p1.last_name = "LEROUX"
p1.date_birth = "17/01/2001"
p1.phone_number = "0203040506"
p1.email = "paul@gmail.com"
c1 = Account()
c1.owner = p1
c1.balance = 950.0

persons = db.display_all_person()
for person in persons:
    print("*"*40)
    print(person)

print()

accounts = db.display_all_account()
for account in accounts:
    print("*"*40)
    print(account)
print()
account1 = accounts[0]
account2 = accounts[1]

db.transaction(account1, account2, 75.0)

historics = db.display_all_historic(account1.account_id)
for histo in historics:
    print(histo)
