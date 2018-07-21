import sqlite3


class TransactionModel:
    def __init__(self, bank_name, card):
        self.bank_name = bank_name
        self.card = card

    def json(self):
        return {
            'bank_name': self.bank_name,
            'card': self.card
        }

    def insert(self):
        if not TransactionModel.find_transaction(self.card):
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()

            query = 'INSERT INTO transactions VALUES (?, ?)'
            try:
                cursor.execute(query, (self.bank_name.lower(), self.card))
            except:
                return {'message': 'Unfortunate error occurred'}, 500

            connection.commit()
            connection.close()

    @classmethod
    def find_transaction(cls, card):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        try:
            query = 'SELECT * FROM transactions WHERE card = ?'
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        result = cursor.execute(query, (card,)).fetchone()

        connection.close()

        if result:
            return cls(result[0], result[1])

'''
    @classmethod
    def get_transaction(cls, card):
        try:
            query = 'SELECT * FROM transactions WHERE card = ?'
        except:
            return {'message': 'Unfortunate error occurred'}, 500

        result = cursor.execute(query, (card,)).fetchone()

        return {
            'bank_name': result[0],
            'card': result[1]
        }
'''