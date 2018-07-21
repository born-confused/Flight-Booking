import sqlite3


class ContactModel:
    def __init__(self, passport, dob, phone, email_id, first_name, last_name):
        self.passport = passport
        self.dob = dob
        self.phone = phone
        self.email_id = email_id
        self.first_name = first_name
        self.last_name = last_name

    def json(self):
        return {
            'passport': self.passport,
            'date_of_birth': self.dob,
            'phone': self.phone,
            'email_id': self.email_id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def update(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'UPDATE contacts SET first_name=? WHERE passport=?'
        cursor.execute(query, (self.first_name.lower(), self.passport.lower()))

        query = 'UPDATE contacts SET last_name=? WHERE passport=?'
        cursor.execute(query, (self.last_name.lower(), self.passport.lower()))

        connection.commit()
        connection.close()

    def insert(self):
        if not ContactModel.find_contact(self.passport):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            query = 'INSERT INTO contacts VALUES (?, ?, ?, ?, ?, ?)'

            try:
                cursor.execute(query, (self.passport.lower(), self.dob, self.phone,
                                       self.email_id.lower(), self.first_name.lower(), self.last_name.lower()))
            except:
                return {'message': 'Unfortunate error occurred'}, 500

            connection.commit()
            connection.close()

    @classmethod
    def find_contact(cls, passport):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM contacts WHERE passport = ?'

        try:
            result = cursor.execute(query, (passport.lower(),)).fetchone()
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        connection.close()

        if result:
            return cls(result[0], result[1], result[2], result[3], result[4], result[5])
