from account import Account
from person import Person


p1 = Person("Baptiste", "LEROUX", "23/01/1999", "0102030405", "baptiste@gmail.com")
c1 = Account(p1, 50.0)

p2 = Person("Paul", "LEROUX", "17/01/2001", "0203040506", "paul@gmail.com")
c2 = Account(p2, 75.0)

print(c1)
print(c2)
