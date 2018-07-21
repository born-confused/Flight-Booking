from flask_restful import Resource, reqparse

from models.booking import BookingModel
from models.flights import FlightModel
from models.contacts import ContactModel


class ViewBooking(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'pnr',
        type=str,
        required=True,
        help="Field can't be empty"
    )

    def post(self):
        data = ViewBooking.parser.parse_args()

        view_ticket = BookingModel.get_booking(data['pnr'])

        flight = FlightModel.find_by_number(data['route_id'])
        flight_information = flight.json()
        view_ticket.update({
            'destination': flight_information['destination'],
            'source': flight_information['source'],
            'departure_time': flight_information['departure_time'],
            'arrival_time': flight_information['arrival_time']
        })

        view_ticket.update({
            'equipment': 'Boeing 737MAX',
            'class_booked': data['_class']
        })

        contact = ContactModel.find_contact(data['passport'])
        contact_information = contact.json()
        view_ticket.update({
            'date_of_birth': contact_information['dob'],
            'phone': contact_information['phone'],
            'email_id': contact_information['email_id'],
            'first_name': contact_information['first_name'],
            'last_name': contact_information['last_name']
        })

        return view_ticket, 200
