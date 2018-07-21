from flask import Flask
from flask_restful import Api

from resources.flights import FlightList, Flight, FlightResult
from resources.fares import Fare
from resources.classes import Classes
from resources.discounts import Discount
from resources.aircrafts import Aircraft
from resources.contacts import Contact
from resources.update_contact import UpdateContact
from resources.book_ticket import Booking
from resources.view_booking import ViewBooking

from models.classes import ClassModel
from models.flights import FlightModel
from models.fares import FareModel
from models.discounts import DiscountModel
from models.aircrafts import AircraftModel

app = Flask(__name__)

app.secret_key = 'bh2'
api = Api(app)


api.add_resource(FlightList, '/book_flight/<string:source>/<string:destination>')
api.add_resource(Flight, '/flight/<int:route_id>')
api.add_resource(Fare, '/fare/<int:route_id>/<string:_class>')
api.add_resource(Classes, '/get_class')
api.add_resource(Discount, '/discount/<string:promocode>')
api.add_resource(Aircraft, '/aircraft/<string:reg_code>')
api.add_resource(Contact, '/contacts/<string:passport>')
api.add_resource(FlightResult, '/return_flight')
api.add_resource(UpdateContact, '/update_contact')
api.add_resource(Booking, '/final_book')
api.add_resource(ViewBooking, '/view_booking')


def pre_run():
    first = ClassModel('first', 4, 40, 14)
    business = ClassModel('business', 8, 30, 10)
    economy = ClassModel('economy', 156, 30, 7)

    flight1 = FlightModel(572, 'mumbai', 'kuwait', '0225', '0400')
    flight2 = FlightModel(574, 'mumbai', 'kuwait', '2125', '2300')

    fare1 = FareModel(572, 'first', 25000)
    fare2 = FareModel(572, 'business', 15000)
    fare3 = FareModel(572, 'economy', 9000)
    fare4 = FareModel(574, 'first', 18000)
    fare5 = FareModel(574, 'business', 11000)
    fare6 = FareModel(574, 'economy', 8000)

    discount1 = DiscountModel('10OFF', 10)
    discount2 = DiscountModel('15OFF', 15)

    aircraft1 = AircraftModel('VT-JGV', 'Boeing 737MAX', 168)
    aircraft2 = AircraftModel('VT-JGW', 'Boeing 737MAX', 168)
    aircraft3 = AircraftModel('VT-JGQ', 'Boeing 737MAX', 168)
    aircraft4 = AircraftModel('VT-JGX', 'Boeing 737MAX', 168)

    flight1.insert()
    flight2.insert()

    fare1.insert()
    fare2.insert()
    fare3.insert()
    fare4.insert()
    fare5.insert()
    fare6.insert()

    first.insert()
    business.insert()
    economy.insert()

    discount1.insert()
    discount2.insert()

    aircraft1.insert()
    aircraft2.insert()
    aircraft3.insert()
    aircraft4.insert()


if __name__ == '__main__':
    pre_run()
    app.run(port=5500, debug=True)

