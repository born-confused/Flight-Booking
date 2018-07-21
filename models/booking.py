import sqlite3


class BookingModel:

    available_pnr = [
        'M7YDNR',
        'IED16X',
        'P6STSV',
        'F94T8A',
        'JQ5FI1',
        'HWQLET',
        'PVFZKU',
        'LQVTVC',
        'HLGNKV',
        'ZGEVBS',
        'BBHTVN'
    ]

    def __init__(self, pnr, doj, final_fare, passport, bank_name, card, route_id):
        self.pnr = pnr
        self.doj = doj
        self.final_fare = final_fare
        self.passport = passport
        self.bank_name = bank_name
        self.card = card
        self.route_id = route_id

    def json(self):
        return {
            'pnr': self.pnr.upper(),
            'doj': self.doj,
            'final_fare': self.final_fare,
            'passport': self.passport,
            'bank_name': self.bank_name,
            'card': self.card,
            'route_id': self.route_id
        }

    @classmethod
    def find_booking(cls, pnr):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM booked_passengers WHERE pnr = ?'
        try:
            result = cursor.execute(query, (pnr.lower(),)).fetchone()
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        connection.close()

        if result:
            return cls(result[0], result[1], result[2], result[3], result[4], result[5], result[6])

    def insert(self):
        if not BookingModel.find_booking(self.pnr):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            query = 'INSERT INTO booked_passengers VALUES (?, ?, ?, ?, ?, ?, ?)'
            try:
                cursor.execute(query, (self.pnr.lower(), self.doj, self.final_fare,
                                   self.passport.lower(), self.bank_name.lower(), self.card, self.route_id))
            except:
                return {'message': 'Unfortunate error occurred'}, 500

            connection.commit()
            connection.close()

    def new_pnr(self):
        new_pnr = BookingModel.available_pnr[0]
        BookingModel.available_pnr.remove(new_pnr)
        return new_pnr.lower()


    @classmethod
    def get_booking(cls, pnr):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        try:
            query = 'SELECT * FROM booked_passengers WHERE pnr = ?'
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        result = cursor.execute(query, (pnr.lower(),)).fetchone()

        return {
            'pnr': result[0],
            'doj': result[1],
            'final_fare': result[2],
            'passport': result[3],
            'bank_name': result[4],
            'card': result[5],
            'route_id': result[6]
        }

