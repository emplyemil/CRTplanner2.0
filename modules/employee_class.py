import json

class Employee:
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    def __eq__(self, other):
        return self.email == other.email

    def __hash__(self):
        return hash(self.email)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __repr__(self):
        return f'<{self.firstname} {self.lastname}>'