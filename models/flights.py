import sqlite3


class FlightModel:
    def __init__(self, f_number, source, destination, d_time, a_time):
        self.f_number = f_number
        self.source = source
        self.destination = destination
        self.d_time = d_time
        self.a_time = a_time

    def json(self):
        return {
            'flight_number': self.f_number,
            'source': self.source,
            'destination': self.destination,
            'departure_time': self.d_time,
            'arrival_time': self.a_time
        }

    @classmethod
    def find_by_number(cls, number):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM f_routes WHERE route_id = ?'
        try:
            result = cursor.execute(query, (number,)).fetchone()
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        connection.close()

        if result:
            return cls(result[0], result[1], result[2], result[3], result[4])

    def insert(self):
        if not FlightModel.find_by_number(self.f_number):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            query = 'INSERT INTO f_routes VALUES (?, ?, ?, ?, ?)'
            cursor.execute(query, (self.f_number, self.source.lower(), self.destination.lower(), self.d_time, self.a_time))

            connection.commit()
            connection.close()

    def update(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'UPDATE f_routes SET source=? WHERE route_id=?'
        cursor.execute(query, (self.source.lower(), self.f_number))

        query = 'UPDATE f_routes SET destination=? WHERE route_id=?'
        cursor.execute(query, (self.destination.lower(), self.f_number))

        query = 'UPDATE f_routes SET d_time=? WHERE route_id=?'
        cursor.execute(query, (self.d_time, self.f_number))

        query = 'UPDATE f_routes SET a_time=? WHERE route_id=?'
        cursor.execute(query, (self.a_time, self.f_number))

        connection.commit()
        connection.close()
