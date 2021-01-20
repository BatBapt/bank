import sys
try:
    from random import choice, randint
    from datetime import datetime
except ImportError as e:
    print("Person: {}".format(e))
    sys.exit(1)


class Person:
    num_id = 0
    def __init__(self, person_id=None):

        if person_id is None:
            self._person_id = Person.num_id
            self._password = self.gen_password_random()
            Person.num_id += 1
        else:
            try:
                assert isinstance(person_id, int), "[Person:init] Erreur le numéro n'est pas un entier"
            except AssertionError as e:
                print(e)
                sys.exit(-1)
            self._person_id = person_id
            self._password = ""

        self._first_name = ""
        self._last_name = ""
        self._date_birth = ""
        self._phone_number = ""
        self._email = ""

    # Getter
    @property
    def person_id(self):
        return self._person_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def password(self):
        return self._password

    @property
    def date_birth(self):
        return self._date_birth

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def email(self):
        return self._email

    # Setter
    @person_id.setter
    def person_id(self, new_id):
        try:
            assert isinstance(person_id, int), "[Person:person_id] Erreur le numéro n'est pas un entier"
        except AssertionError as e:
            print(e)
            sys.exit(-1)
        self._person_id = new_id

    @first_name.setter
    def first_name(self, first_name):
        try:
            assert isinstance(first_name, str), "[Personne:first_name.setter] Erreur le prénom doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._first_name = first_name

    @last_name.setter
    def last_name(self, last_name):
        try:
            assert isinstance(last_name, str), "[Personne:last_name.setter] Erreur le nom de famille doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._last_name = last_name

    @password.setter
    def password(self, new_pwd):
        try:
            assert isinstance(new_pwd, str), "[Personne:password.setter] Erreur le mot de passe doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._password = new_pwd

    @date_birth.setter
    def date_birth(self, date_birth):
        try:
            assert isinstance(date_birth, str), "[Personne:date_birth.setter] Erreur la date de naissance doit être une chaine de caractère"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._date_birth = date_birth

    @phone_number.setter
    def phone_number(self, new_phone):
        try:
            assert isinstance(new_phone, str), "[Personne:phone:setter]: Erreur le numéro de téléphone doit être une chaine de caractère"
            assert len(new_phone) == 10, "[Personne:phone:setter]: Erreur le numéro de téléphone est au mauvais format"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._phone_number = new_phone

    @email.setter
    def email(self, new_email):
        try:
            assert isinstance(new_email, str), "[Personne:email:setter]: Erreur l'adresse mail doit être une chaine de caractère"
            assert "@" in new_email, "[Personne:email:setter] l'adresse mail n'est pas au bon format"
        except AssertionError as e:
            print(e)
            sys.exit(1)
        self._email = new_email

    # Methods
    def __repr__(self):
        string = "{} {} né(e) le {}.\nNuméro de téléphone: {}. Adresse mail: {}".format(
            self._last_name,
            self._first_name,
            self._date_birth,
            self._phone_number,
            self._email
        )
        return string

    @property
    def full_name(self):
        return self._last_name + " " + self._first_name


    def gen_password_random(self):
        alphabet_min = [ chr(i) for i in range(97,123) ]
        alphabet_maj = [ chr(i) for i in range(65,91) ]
        chiffres = [ chr(i) for i in range(48,58) ]
        caracteres_speciaux = ['%', '_', '-', '!', '$', '^', '&', '#', '(', ')', '[', ']', '=', '@']

        alphabet = {0: alphabet_min, 1: alphabet_maj, 2: chiffres}
        password = ""
        for i in range(10):
            key = randint(0, 2)
            password += choice(alphabet[key])
        return password

    def instanciate_perso_from_bdd(self, param):
        try:
            assert isinstance(param, list), "[Personn:instanciate_perso_from_bdd] Erreur le paramètre n'est pas une liste"
            assert len(param) == 6, "[Personn:instanciate_perso_from_bdd] Erreur la liste n'est pas de bonne taille"
        except AssertionError as e:
            print(e)
            sys.exit(-1)

        self._last_name = param[0]
        self._first_name = param[1]
        self._password = param[2]
        self._date_birth = param[3]
        self._phone_number = param[4]
        self._email = param[5]
