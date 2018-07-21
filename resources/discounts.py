import sqlite3
from flask_restful import Resource, reqparse

from models.discounts import DiscountModel


class Discount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'discount_per',
        required=True,
        type=float,
        help="This field can't be empty"
    )

    def get(self, promocode):
        try:
            discount = DiscountModel.find_discount(promocode)
        except:
            return {'message': "Unfortunate error occurred"}, 500

        if discount:
            return discount.json(), 200
        return {'message': 'Discount not found'}, 404

    def post(self, promocode):
        if DiscountModel.find_discount(promocode):
            return {'message': 'Fare already exist'}, 400

        data = Discount.parser.parse_args()
        discount = DiscountModel(promocode, data['discount_per'])

        try:
            discount.insert()
        except:
            return {'message': "Unfortunate error occurred"}, 500

        return discount.json(), 201

    def delete(self, promocode):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = 'DELETE FROM discounts WHERE promocode = ?'
        cursor.execute(query, (promocode,))

        connection.commit()
        connection.close()

        return {'message': "Discount for {} is deleted".format(promocode)}, 200