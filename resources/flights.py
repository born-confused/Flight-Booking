import sqlite3
from flask_restful import Resource, reqparse

from models.flights import FlightModel
from models.fares import FareModel
from models.discounts import DiscountModel


class Flight(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'source',
        type=str,
        required=True,
        help="Can't be empty"
    )
    parser.add_argument(
        'destination',
        type=str,
        required=True,
        help="Can't be empty"
    )
    parser.add_argument(
        'departure_time',
        type=str,
        required=True,
        help="Can't be empty",
        dest='d_time'
    )
    parser.add_argument(
        'arrival_time',
        type=str,
        required=True,
        help="Can't be empty",
        dest='a_time'
    )

    def put(self, route_id):
        data = Flight.parser.parse_args()

        route = FlightModel.find_by_number(route_id)
        new_route = FlightModel(route_id,
                                data['source'],
                                data['destination'],
                                data['d_time'],
                                data['a_time']
                    )

        if route:
            try:
                new_route.update()
            except:
                return {'message': "Couldn't update"}, 500
            return new_route.json(), 200
        try:
            new_route.insert()
        except:
            return {'message': "Couldn't insert"}, 500
        return new_route.json(), 201

    def delete(self, route_id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'DELETE FROM f_routes WHERE route_id = ?'
        cursor.execute(query, (route_id,))

        connection.commit()
        connection.close()

        return {'message': "Route {} is deleted".format(route_id)}, 200

    def get(self, route_id):
        try:
            route = FlightModel.find_by_number(route_id)
        except:
            return {'message': 'Unfortunate error occurred'}, 500
        if route:
            return route.json(), 200
        return {'message': "route doesn't exist"}, 404

    def post(self, route_id):
        if FlightModel.find_by_number(route_id):
            return {'message': 'route already exist'}, 400

        data = Flight.parser.parse_args()
        route = FlightModel(route_id, data['source'], data['destination'],
                            data['d_time'], data['a_time'])

        try:
            route.insert()
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        return route.json(), 201


class FlightList(Resource):
    def get(self, source, destination):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query1 = 'SELECT * FROM f_routes WHERE source = ? AND destination = ?'
        query2 = 'SELECT * FROM base_fare WHERE route_id = ?'

        flights_list = []

        flight_result = cursor.execute(query1, (source.lower(), destination.lower()))

        for f_result in flight_result:
            '''try:
                fare_result = cursor.execute(query2, (f_result[0],))
            except:
                return {'message': 'Unfortunate error occurred'}, 500

            b_fare = {}

            for fare in fare_result:
                b_fare.update({fare[1]: fare[2]})

            b_fare = FareModel.get_fare(f_result[0], cursor)'''

            flights_list.append({
                'flight_number': f_result[0],
                'source': f_result[1],
                'destination': f_result[2],
                'departure_time': f_result[3],
                'arrival_time': f_result[4],
                'equipment': 'Boeing 737MAX'
            })

        for flight in flights_list:
            b_fare = FareModel.get_fare(flight['flight_number'], cursor)
            flight.update({
                'first_class': b_fare['first'],
                'business_class': b_fare['business'],
                'economy_class': b_fare['economy'],
            })
        connection.close()
        return {'flight_routes': flights_list}, 200


class FlightResult(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'source',
        type=str,
        required=True,
        help="Field can't be empty"
    )
    parser.add_argument(
        'destination',
        type=str,
        required=True,
        help="Field can't be empty"
    )
    parser.add_argument(
        'doj',
        type=str,
        required=True,
        help="Field can't be empty"
    )
    parser.add_argument(
        'promocode',
        type=str,
        help="Field can't be empty"
    )

    def get_detailed_ticket(self):
        data = FlightResult.parser.parse_args()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query1 = 'SELECT * FROM f_routes WHERE source = ? AND destination = ?'

        flights_list = []

        flight_result = cursor.execute(query1, (data['source'].lower(), data['destination'].lower()))

        for f_result in flight_result:
            flights_list.append({
                'flight_number': f_result[0],
                'source': f_result[1],
                'destination': f_result[2],
                'doj': data['doj'],
                'departure_time': f_result[3],
                'arrival_time': f_result[4],
                'equipment': 'Boeing 737MAX'
            })
        discount = {}
        if data['promocode']:
            discount = DiscountModel.get_discount(data['promocode'], cursor)

        for flight in flights_list:
            b_fare = FareModel.get_fare(flight['flight_number'], cursor)

            first_fare = b_fare['first']
            business_fare = b_fare['business']
            economy_fare = b_fare['economy']

            if discount:
                first_fare = first_fare * (1.0 - (discount['percentage'] / 100))
                business_fare = business_fare * (1.0 - (discount['percentage'] / 100))
                economy_fare = economy_fare * (1.0 - (discount['percentage'] / 100))

            flight.update({
                'first_class': first_fare,
                'business_class': business_fare,
                'economy_class': economy_fare,
            })

        connection.close()
        return {'flight_routes': flights_list}

    def post(self):
        data = FlightResult.parser.parse_args()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query1 = 'SELECT * FROM f_routes WHERE source = ? AND destination = ?'

        flights_list = []

        flight_result = cursor.execute(query1, (data['source'].lower(), data['destination'].lower()))

        for f_result in flight_result:
            flights_list.append({
                'flight_number': f_result[0],
                'source': f_result[1],
                'destination': f_result[2],
                'doj': data['doj'],
                'departure_time': f_result[3],
                'arrival_time': f_result[4],
                'equipment': 'Boeing 737MAX'
            })
        discount = {}
        if data['promocode']:
            discount = DiscountModel.get_discount(data['promocode'], cursor)

        for flight in flights_list:
            b_fare = FareModel.get_fare(flight['flight_number'], cursor)

            first_fare = b_fare['first']
            business_fare = b_fare['business']
            economy_fare = b_fare['economy']

            if discount:
                first_fare = first_fare * (1.0 - (discount['percentage']/100))
                business_fare = business_fare * (1.0 - (discount['percentage']/100))
                economy_fare = economy_fare * (1.0 - (discount['percentage']/100))

            flight.update({
                'first_class': first_fare,
                'business_class': business_fare,
                'economy_class': economy_fare,
            })

        connection.close()
        return {'flight_routes': flights_list}, 200

