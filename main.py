from datetime import datetime

from account import Account
from person import Person

bapt_birth = datetime.strptime('23-07-1999', "%d-%m-%Y")
paul_birth = datetime.strptime('17-01-2001', "%d-%m-%Y")

p1 = Person("Baptiste", "LEROUX", "titounne", bapt_birth, "0102030405", "baptiste@gmail.com")
p2 = Person("Paul", "LEROUX", "paulo", paul_birth, "0203040506", "paul@gmail.com")

c1 = Account(p1, 50.0)
c2 = Account(p2, 75.0)

print(c1)
print(c2)
