import sqlite3
from flask_restful import Resource, reqparse

from models.fares import FareModel


class Fare(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'fare',
        required=True,
        type=float,
        help="This field can't be empty"
    )

    def get(self, route_id, _class):
        try:
            fare = FareModel.find_fare(route_id, _class)
        except:
            return {'message': "Unfortunate error occurred"}, 500

        if fare:
            return fare.json(), 200
        return {'message': 'Fare not found'}, 404

    def put(self, route_id, _class):
        data = Fare.parser.parse_args()

        fare = FareModel.find_fare(route_id, _class)
        new_fare = FareModel(route_id, _class, data['fare'])

        if fare:
            try:
                new_fare.update()
            except:
                return {'message': "Couldn't update"}, 500
            return new_fare.json(), 200
        try:
            new_fare.insert()
        except:
            return {'message': "Couldn't insert"}, 500
        return new_fare.json(), 201

    def post(self, route_id, _class):
        if FareModel.find_fare(route_id, _class):
            return {'message': 'Fare already exist'}, 400

        data = Fare.parser.parse_args()
        fare = FareModel(route_id, _class, data['fare'])

        try:
            fare.insert()
        except:
            return {'message': "Unfortunate error occurred"}, 500

        return fare.json(), 201

    def delete(self, route_id, _class):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'DELETE FROM base_fare WHERE route_id = ? AND _class = ?'
        cursor.execute(query, (route_id, _class))

        connection.commit()
        connection.close()

        return {'message': "Fare for route {} and class {} is deleted".format(route_id, _class)}, 200