#!/usr/bin/env python

#-----------------------------------------------------------------------
# ratinghistory.py
#-----------------------------------------------------------------------

class RatingHistory:
    def __init__(self, username, first_name, last_name, headshot, rating, msg):
        self._username = username
        self._first_name = first_name
        self._last_name = last_name
        self._headshot = headshot
        self._rating = rating
        self._msg = msg

    def get_username(self):
        return self._username

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_headshot(self):
        return self._headshot

    def get_rating(self):
        return self._rating

    def get_msg(self):
        return self._msg

    def to_tuple(self):
        return (self._username, self._first_name, self._last_name, self._headshot, self._rating, self._msg)
