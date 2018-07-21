import sqlite3


class FareModel:
    def __init__(self, f_number, _class, fare):
        self.f_number = f_number
        self._class = _class
        self.fare = fare

    def json(self):
        return {
            'f_number': self.f_number,
            '_class': self._class,
            'fare': self.fare
        }

    def insert(self):
        if not FareModel.find_fare(self.f_number, self._class):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            query = 'INSERT INTO base_fare VALUES (?, ?, ?)'
            cursor.execute(query, (self.f_number, self._class.lower(), self.fare))

            connection.commit()
            connection.close()

    def update(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'UPDATE base_fare SET route_id=? WHERE route_id=?'
        cursor.execute(query, (self.f_number, self.f_number))

        query = 'UPDATE base_fare SET _class=? WHERE route_id=?'
        cursor.execute(query, (self._class.lower(), self.f_number))

        query = 'UPDATE base_fare SET fare=? WHERE route_id=?'
        cursor.execute(query, (self.fare, self.f_number))

        connection.commit()
        connection.close()

    @classmethod
    def get_fare(cls, route_id, cursor):
        try:
            query = 'SELECT * FROM base_fare WHERE route_id = ?'
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        result = cursor.execute(query, (route_id,))

        base_fare = {}

        for row in result:
            base_fare.update({row[1]: row[2]})

        return base_fare

    @classmethod
    def find_fare(cls, route_id, _class):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        try:
            query = 'SELECT * FROM base_fare WHERE route_id = ? AND _class = ?'
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        result = cursor.execute(query, (route_id, _class.lower())).fetchone()

        connection.close()

        if result:
            return cls(route_id, _class, result[2])
