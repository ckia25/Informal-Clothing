#!/usr/bin/env python

# ----------------------------------------------------------------------
# editnotification.py
#-----------------------------------------------------------------------

import services.database as database
from services.database import _engine, Notification
import classes.notification as notificationmod
from classes.listing import Listing

import sqlalchemy.orm
import sqlalchemy

from config import config_cloudinary
config_cloudinary()
from cloudinary import uploader

#-----------------------------------------------------------------------


def remove_notification(id):

    with sqlalchemy.orm.Session(_engine) as session:
        stmt = (sqlalchemy.delete(database.Notification).where(
            database.Notification.id == id))
        session.execute(stmt)
        session.commit()


#-----------------------------------------------------------------------


def add_notification(notif_type, listing_id, to_user_id, from_user_id,
    date_created, transaction_id, msg):

    with sqlalchemy.orm.Session(_engine) as session:
        new_notification = database.Notification(notif_type=notif_type, 
            listing_id=listing_id, to_user_id=to_user_id, from_user_id=from_user_id,
            date_created=date_created, transaction_id=transaction_id, msg=msg)
        session.add(new_notification)
        session.commit()
        session.flush()
        session.refresh(new_notification)


#-----------------------------------------------------------------------

def _test():

    # add a new test listing to database
    with sqlalchemy.orm.Session(_engine) as session:

        new_listing = database.Listing(user_id=3329, name='katie',
            price=100, category='shirt', size='small', subcategory='what',
            description='test listing', status='Available', pickup_location=None,
            likes=0)
        session.add(new_listing)
        session.commit()
        session.flush()
        session.refresh(new_listing)