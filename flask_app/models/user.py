from sqlite3 import connect
from types import ClassMethodDescriptorType
from flask import flash
from flask_bcrypt import Bcrypt
import re
from flask_app.config.mysqlconnection import connectToMySQL


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

    # METHOD TO VALIDATE USER //////////////////////
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name'])<5:
            flash("first name must be at least 5 characters")
            is_valid = False
            
        if len(user['last_name'])<5:
            flash("last name must be at least 5 characters")
            is_valid = False
            
        if not EMAIL_REGEX.match(user['email']):
            flash("invalid email")
            is_valid = False
            
        if len(user['password'])<8:
            flash("password must be at least 8 characters")
            is_valid = False
        if (user['password'] != user['confirm_password']):
            flash ("wrong password")
            is_valid = False
        return is_valid

    # METHOD TO SAVE OUR USER //////////////////////////
    @classmethod 
    def save(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        results = connectToMySQL("login_schema").query_db(query, data)
        return results 

    #METHOD TO GRAB USER BY EMAIL//////////////////////////
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL("login_schema").query_db(query, data)
        # CHECK TO SEE IF THERE IS NO EMAIL IN RESULT////////////////
        if len(result)<1:
            return False
        return cls(result[0])

    # METHOD TO GET USER BY ID//////////////////////////////
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM user WHERE id = %(user_id)s;"
        result = connectToMySQL("login_schema").query_db(query, data)
        
        if len(result)<1:
            return False
        return cls(result[0])