from flask_restful import Resource, reqparse

from models.booking import BookingModel
from models.flights import FlightModel
from models.contacts import ContactModel


class Booking(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'route_id',
        required=True,
        type=int,
        help="Field can't be empty"
    )
    parser.add_argument(
        'fare',
        required=True,
        type=float,
        help="Field can't be empty"
    )
    parser.add_argument(
        'doj',
        required=True,
        type=str,
        help="Field can't be empty"
    )
    parser.add_argument(
        'passport',
        required=True,
        type=str,
        help="Field can't be empty"
    )
    parser.add_argument(
        'bank_name',
        required=True,
        type=str,
        help="Field can't be empty"
    )
    parser.add_argument(
        'card',
        required=True,
        type=str,
        help="Field can't be empty"
    )
    parser.add_argument(
        '_class',
        required=True,
        type=str,
        help="Field can't be empty"
    )

    def post(self):
        data = Booking.parser.parse_args()
        new_pnr = BookingModel.new_pnr()

        new_ticket = BookingModel(new_pnr, data['doj'], data['fare'], data['passport'], data['bank_name'],
                                  data['card'], data['route_id'])

        try:
            new_ticket.insert()
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        flight = FlightModel.find_by_number(data['route_id'])
        flight_information = flight.json()
        flight_information.update({
            'equipment': 'Boeing 737MAX',
            'fare': flight_information['fare'],
            'bank_name': flight_information['bank_name'],
            'card': flight_information['card'],
            'class_booked': flight_information['_class']
        })

        contact = ContactModel.find_contact(data['passport'])
        contact_information = contact.json()
        flight_information.update({
            'passport': contact_information['passport'],
            'date_of_birth': contact_information['dob'],
            'phone': contact_information['phone'],
            'email_id': contact_information['email_id'],
            'first_name': contact_information['first_name'],
            'last_name': contact_information['last_name']
        })

        return flight_information, 201
