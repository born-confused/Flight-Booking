import sqlite3


class AircraftModel:
    def __init__(self, reg_code, equipment, number_of_seats):
        self.reg_code = reg_code
        self.equipment = equipment
        self.number_of_seats = number_of_seats

    def json(self):
        return {
            'aircraft_registration': self.reg_code.upper(),
            'equipment': self.equipment,
            'total_seats': self.number_of_seats
        }

    @classmethod
    def find_aircraft(cls, reg_code):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM aircrafts WHERE reg_code = ?'
        try:
            result = cursor.execute(query, (reg_code.lower(),)).fetchone()
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        connection.close()

        if result:
            return cls(result[0], result[1], result[2])

    def insert(self):
        if not AircraftModel.find_aircraft(self.reg_code):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            query = 'INSERT INTO aircrafts VALUES (?, ?, ?)'
            cursor.execute(query, (self.reg_code.lower(), self.equipment.lower(), self.number_of_seats))

            connection.commit()
            connection.close()

    '''
    @classmethod
    def get_discount(cls, promocode):
        try:
            query = 'SELECT * FROM discounts WHERE promocode = ?'
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        result = cursor.execute(query, (promocode,)).fetchone()

        return {result[0]: result[1]}
    '''
