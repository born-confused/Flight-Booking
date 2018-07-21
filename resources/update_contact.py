from flask_restful import Resource, reqparse

from models.contacts import ContactModel

class UpdateContact(Resource):
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
        'dob',
        type=str,
        required=True,
        help="Can't be empty"
    )
    parser.add_argument(
        'phone',
        type=str,
        required=True,
        help="Can't be empty"
    )
    parser.add_argument(
        'email_id',
        type=str,
        required=True,
        help="Can't be empty"
    )
    parser.add_argument(
        'first_name',
        type=str,
        required=True,
        help="Can't be empty"
    )
    parser.add_argument(
        'last_name',
        type=str,
        required=True,
        help="Can't be empty"
    )
    parser.add_argument(
        'passport',
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
        data = UpdateContact.parser.parse_args()
        new_contact = ContactModel(data['passport'], data['dob'], data['phone'], data['email_id'],
                                    data['first_name'], data['last_name'])

        try:
            new_contact.insert()
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        return {
            'route_id': data['route_id'],
            'final_fare': data['fare'],
            'doj': data['doj'],
            'class_booked': data['_class'],
            'passport': data['passport']
        }, 201
