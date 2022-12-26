from flask_app.models.models_user import User
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = 'stocker_data'

class Stock:
    def __init__(self, data):
        self.id = data['id']
        self.symbol = data['symbol']
        self.company_name = data['company_name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.joined = None


    #Create Stock entry
    @classmethod
    def create_stock(cls, data):
        query = """
                INSERT INTO stocks (symbol, company_name, description, user_id)
                VALUES ( %(symbol)s, %(company_name)s, %(description)s, %(user_id)s )
                """
        return connectToMySQL(db).query_db(query, data)


    #Display all stocks
    @classmethod
    def all_stocks(cls):
        query = "SELECT * FROM stocks"
        results = connectToMySQL(db).query_db(query)
        stock = []
        for stocks in results:
            stock.append(cls(stocks))
        return stock


    #Joined tables
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM stocks
                JOIN users ON users.id = stocks.user_id
                WHERE stocks.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        stock = cls(results[0])
        joined_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
        }
        stock.joined = User(joined_data)
        return stock



    #Update Stock
    @classmethod
    def update_stock(cls, form_data, stock_id):
        query = f"UPDATE stocks SET symbol = %(symbol)s, company_name = %(company_name)s, description = %(description)s WHERE id = {stock_id}"
        return connectToMySQL(db).query_db(query, form_data)


    #Delete Stock
    @classmethod
    def delete_stock(cls, data):
        query = """
                DELETE FROM stocks
                WHERE id = %(id)s
                """
        return connectToMySQL(db).query_db(query, data)
