import sqlite3
from flask_restful import Resource, reqparse

from models.contacts import ContactModel


class Contact(Resource):
    parser = reqparse.RequestParser()
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

    def get(self, passport):
        try:
            contact = ContactModel.find_contact(passport)
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        if contact:
            return contact.json(), 200
        return {'message': "Contact doesn't exists"}, 404

    def put(self, passport):
        data = Contact.parser.parse_args()

        contact = ContactModel.find_contact(passport)
        new_contact = ContactModel(passport,
                                data['dob'],
                                data['phone'],
                                data['email_id'],
                                data['first_name'],
                                data['last_name']
                    )

        if contact:
            try:
                new_contact.update()
            except:
                return {'message': "Couldn't update"}, 500
            return new_contact.json(), 200
        try:
            new_contact.insert()
        except:
            return {'message': "Couldn't insert"}, 500
        return new_contact.json(), 201

    def post(self, passport):
        if ContactModel.find_contact(passport):
            return {'message': 'contact already exist'}, 400

        data = Contact.parser.parse_args()
        contact = ContactModel(passport, data['dob'], data['phone'],
                            data['email_id'], data['first_name'], data['last_name'])

        try:
            contact.insert()
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        return contact.json(), 201

    def delete(self, passport):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = ' DELETE FROM contacts WHERE passport = ?'

        try:
            cursor.execute(query, (passport,))
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        connection.commit()
        connection.close()

        return {'message': 'Contact with {} deleted'.format(passport)}, 200