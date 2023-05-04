from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import DATABASE
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:

    def __init__(self, data):

        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # ======== CREATE USER ==========
    @classmethod 
    def create(cls, data):

        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s) ;
                """
        
        return MySQLConnection(DATABASE).query_db(query, data)
    
    # ======== FIND USER BY ID ==========
    @classmethod
    def get_by_id(cls, data):

        query = """
                SELECT * FROM users
                WHERE id = %(id)s ;
                """
        result = MySQLConnection(DATABASE).query_db(query, data)
        if len(result) < 1:
            return []
        return cls(result[0])
    

    # ======== FIND USER BY Email ==========
    @classmethod
    def get_by_email(cls, data):

        query = """
                SELECT * FROM users
                WHERE email = %(email)s ;
                """
        result = MySQLConnection(DATABASE).query_db(query, data)

        if len(result) < 1:
            return []
        return cls(result[0])


    # ========= Vadition ===============

    @staticmethod
    def validate_reg(data):

        is_valid = True
        if len(data['first_name']) < 1:
            is_valid = False
            flash("First name is required", "registration")

        if len(data['last_name']) < 1:
            is_valid = False
            flash("Last name is required", "registration")

        if len(data['email']) < 1:
            is_valid = False
            flash("Email is required", "registration")

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "registration")
            is_valid = False
        else:
            email_dict = {
                'email' : data['email']
            }

            potential_user = User.get_by_email(email_dict)
            if potential_user: #! email is not unique
                is_valid = False
                flash("email already taken ! Please login","registration")
        if len(data['password']) < 1:
            is_valid = False
            flash("Password required!", "registration")
        elif not data['password'] == data['confirm_pw']:
            is_valid = False 
            flash("Passwords don't match!", "registration")
            

        return is_valid