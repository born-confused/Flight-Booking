import sqlite3
from flask_restful import Resource


class Classes(Resource):
    def get(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM classes'
        list_of_class = []
        result = cursor.execute(query)
        for row in result:
            list_of_class.append({
                'class': row[0],
                'seats': row[1],
                'check_in': row[2],
                'hand_luggage': row[3]
            })

        connection.close()
        return {'classes': list_of_class}, 200