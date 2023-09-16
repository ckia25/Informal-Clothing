#!/usr/bin/env python

#-----------------------------------------------------------------------
# user.py
#-----------------------------------------------------------------------

import sqlalchemy
import sqlalchemy.ext.declarative
from services.database import _engine
from services.database import Like

#-----------------------------------------------------------------------

class User:

    def __init__(self, id, username, email, address=None, balance=0, headshot=None,
                first_name=None, last_name=None, bio=None, phone_number=None):
        self._id = id
        self._username = username
        self._email = email
        self._address = address
        self._balance = balance
        self._headshot = headshot
        self._first_name = first_name
        self._last_name = last_name
        self._bio = bio
        self._phone_number = phone_number

    def get_id(self):
        return self._id

    def get_username(self):
        return self._username

    def get_email(self):
        return self._email

    def get_address(self):
        return self._address

    def get_balance(self):
        return self._balance

    def get_headshot(self):
        return self._headshot

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name
    
    def get_bio(self):
        return self._bio

    def get_phone_number(self):
        return self._phone_number

    def to_tuple(self):
        return (self._username, self._email,
                self._address, self._balance,
                self._headshot, self._first_name,
                self._last_name,
                self._bio, self._phone_number)
