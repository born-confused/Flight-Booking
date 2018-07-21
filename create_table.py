import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS f_routes (route_id INT, source TEXT, destination TEXT,' \
               ' d_time TEXT, a_time TEXT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS base_fare (route_id INT, _class TEXT, fare FLOAT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS classes (_class TEXT, seats INT, check_in INT, hand_luggage INT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS discounts (promocode TEXT, discount_per FLOAT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS aircrafts (reg_code TEXT, equipment TEXT, number_of_seats INT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS contacts (passport TEXT, dob TEXT, phone TEXT, email_id TEXT,' \
               ' first_name TEXT, last_name TEXT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS transactions (bank_name TEXT, card TEXT)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS booked_passengers (pnr TEXT, doj TEXT, final_fare FLOAT, passport TEXT,' \
               'bank_name TEXT, card TEXT, route_id INT)'
cursor.execute(create_table)

connection.commit()
connection.close()
