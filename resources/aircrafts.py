import sqlite3
from flask_restful import Resource

from models.aircrafts import AircraftModel


class Aircraft(Resource):
    def get(self, reg_code):
        try:
            aircraft = AircraftModel.find_aircraft(reg_code)
        except:
            return {'message': "Unfortunate error occurred"}, 500

        if aircraft:
            return aircraft.json(), 200
        return {'message': 'Aircraft not found'}, 404

    def delete(self, reg_code):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'DELETE FROM aircrafts WHERE reg_code = ?'
        cursor.execute(query, (reg_code,))

        connection.commit()
        connection.close()

        return {'message': "Aircraft deleted"}, 200