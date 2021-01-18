from datetime import datetime

from account import Account
from person import Person
from database import Database


db = Database()
db.init_db()

p1 = Person()
p1.first_name = "Baptiste"
p1.last_name = "LEROUX"
p1.date_birth = "17/01/2001"
p1.phone_number = "0203040506"
p1.email = "baptiste@gmail.com"
c1 = Account()
c1.owner = p1
c1.balance = 950.0

# db.insert_person(p1)
# db.insert_account(c1)

persons = db.display_all_person()
for person in persons:
    print(person)
    p1 = person

# mrEh64sTah
