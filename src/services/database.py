#!/usr/bin/env python

# -----------------------------------------------------------------------
# database.py
# -----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.ext.declarative

# -----------------------------------------------------------------------
_database_url = os.environ.get('DATABASE_URL')
_database_url = _database_url.replace('postgres://', 'postgresql://')

# LISTINGS TABLE COLUMNS:
LISTINGS_ID = 'id'
LISTINGS_USER_ID = 'user_id'
LISTINGS_NAME = 'name'
LISTINGS_PRICE = 'price'
# need to add the category to database and all needed places
LISTINGS_CATEGORY = 'category'
LISTINGS_SIZE = 'size'
LISTINGS_SUBCATEGORY = 'subcategory'
LISTINGS_DESCRIPTION = 'description'
LISTINGS_STATUS = 'status'
LISTINGS_PICK_LOCATION = 'pickup_location'
LISTINGS_LIKES = 'likes'

# -----------------------------------------------------------------------

Base = sqlalchemy.ext.declarative.declarative_base()

class User (Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    balance = sqlalchemy.Column(sqlalchemy.Integer)
    headshot = sqlalchemy.Column(sqlalchemy.String)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    bio = sqlalchemy.Column(sqlalchemy.String)
    phone_number = sqlalchemy.Column(sqlalchemy.String)


class Listing (Base):
    __tablename__ = 'listings'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    name = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.BigInteger)
    category = sqlalchemy.Column(sqlalchemy.String)
    size = sqlalchemy.Column(sqlalchemy.String)
    subcategory = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String)
    pickup_location = sqlalchemy.Column(sqlalchemy.String)
    likes = sqlalchemy.Column(sqlalchemy.Integer)


class Image (Base):
    __tablename__ = 'images'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    listing_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    is_primary = sqlalchemy.Column(sqlalchemy.Boolean)
    img_url = sqlalchemy.Column(sqlalchemy.String)
    cloudinary_id = sqlalchemy.Column(sqlalchemy.String)

class Availability (Base):
    __tablename__ = 'availabilities'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    listing_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    transaction_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    borrower_userid = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    listing_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    to_user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    from_user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    date_created = sqlalchemy.Column(sqlalchemy.DateTime)
    status = sqlalchemy.Column(sqlalchemy.String)
    request_msg = sqlalchemy.Column(sqlalchemy.String)
    date_lent_out = sqlalchemy.Column(sqlalchemy.String)
    date_returned = sqlalchemy.Column(sqlalchemy.String)

class Rating(Base):
    __tablename__ = 'ratings'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer)
    user_rated_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    user_rating_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    date_rated = sqlalchemy.Column(sqlalchemy.DateTime)
    transaction_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    msg = sqlalchemy.Column(sqlalchemy.String)
    rated_is_borrower = sqlalchemy.Column(sqlalchemy.Boolean)


class Like(Base):
    __tablename__ = 'likes'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    listing_id = sqlalchemy.Column(sqlalchemy.BigInteger)

class Notification(Base):
    __tablename__ = 'notifications'
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    notif_type = sqlalchemy.Column(sqlalchemy.String)
    listing_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    to_user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    from_user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    date_created = sqlalchemy.Column(sqlalchemy.String)
    transaction_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    msg = sqlalchemy.Column(sqlalchemy.String)
    time_created = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True),
                                     default=sqlalchemy.func.now())

_engine = sqlalchemy.create_engine(_database_url)

# -----------------------------------------------------------------------
# For testing:

def _test():
    print()


if __name__ == '__main__':
    _test()
