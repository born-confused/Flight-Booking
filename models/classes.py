import sqlite3

class ClassModel:
    def __init__(self, _class, seats, check_in, hand_luggage):
        self._class = _class
        self.seats = seats
        self.check_in = check_in
        self.hand_luggage = hand_luggage

    def insert(self):
        if not ClassModel.find_class(self._class):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            query = 'INSERT INTO classes VALUES (? ,?, ?, ?)'
            cursor.execute(query, (self._class.lower(), self.seats, self.check_in, self.hand_luggage))

            connection.commit()
            connection.close()

    @classmethod
    def find_class(cls, _class):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM classes WHERE _class = ?'
        result = cursor.execute(query, (_class,)).fetchone()

        connection.close()

        if result:
            return cls(result[0], result[1], result[2], result[3])
