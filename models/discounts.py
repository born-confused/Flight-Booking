import sqlite3


class DiscountModel:
    def __init__(self, promocode, discount_per):
        self.promocode = promocode
        self.discount_per = discount_per

    def json(self):
        return {
            'promocode': self.promocode,
            'discount_percentage': self.discount_per
        }

    def insert(self):
        if not DiscountModel.find_discount(self.promocode):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            query = 'INSERT INTO discounts VALUES (?, ?)'
            cursor.execute(query, (self.promocode.lower(), self.discount_per))

            connection.commit()
            connection.close()


    @classmethod
    def get_discount(cls, promocode, cursor):
        try:
            query = 'SELECT * FROM discounts WHERE promocode = ?'
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        result = cursor.execute(query, (promocode.lower(),)).fetchone()
        if result:
            return {'percentage': result[1]}
        return {'percentage': 0}

    @classmethod
    def find_discount(cls, promocode):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        try:
            query = 'SELECT * FROM discounts WHERE promocode = ?'
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        result = cursor.execute(query, (promocode.lower(),)).fetchone()

        connection.close()

        if result:
            return cls(promocode, result[1])
