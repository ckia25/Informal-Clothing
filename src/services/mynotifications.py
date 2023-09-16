#!/usr/bin/env python

# -----------------------------------------------------------------------
# mynotifications.py
# handles route("/mynotifications") endpoint
# -----------------------------------------------------------------------

import datetime
import services.database as database
from services.database import Notification
from services.database import _engine
from services.database import Image
from services.database import Listing
from services.database import User

import sqlalchemy.ext.declarative
import sqlalchemy
from sqlalchemy import func, or_

import classes.notification as notificationmod
import classes.listing as listingmod
from constants import NotificationTypes


#-----------------------------------------------------------------------

# gets all of a given user's notifications where they are the lender
def get_lender_notifications(user_id):
    lender_notifications = []

    with sqlalchemy.orm.Session(_engine) as session:
        stmt = sqlalchemy.select(Notification, Listing, Image, User.username, User.headshot)
        stmt = stmt.where(Notification.from_user_id == user_id)
        stmt = stmt.where(Listing.id == Notification.listing_id)
        stmt = stmt.where(Image.listing_id == Notification.listing_id)
        stmt = stmt.where(User.id == Notification.to_user_id)
        stmt = stmt.where(Image.is_primary == True)
        stmt = stmt.order_by(Notification.id.desc())
        table = session.execute(stmt).all()
        for tup in table:
            notif_row, listing_row, image_row = tup[0].__dict__, tup[1].__dict__, tup[2].__dict__
            borrower_username, headshot = tup[3], tup[4]

            if notif_row['notif_type'] != NotificationTypes.BORROW_REQUEST_ACCEPTED.value:

                time = str(notif_row['time_created']).split(":")
                hour, minute, secs = int(time[0]), int(time[1]), round(float(time[2]))
                # FOR TIMEZONE DIFF FROM UTC
                time_in_minutes = hour * 60 + minute
                four_hours_ago_in_minutes = time_in_minutes - 4 * 60
                while four_hours_ago_in_minutes < 0:
                    four_hours_ago_in_minutes += 24 * 60
                four_hours_ago_hour, four_hours_ago_minute = divmod(four_hours_ago_in_minutes, 60)
                time_created = '{:02d}:{:02d}:{:02d}'.format(four_hours_ago_hour, four_hours_ago_minute, secs)

                notification = notificationmod.Notification(notif_row['id'], notif_row['notif_type'], notif_row['listing_id'],
                    notif_row['to_user_id'], notif_row['from_user_id'], notif_row['date_created'],
                    notif_row['transaction_id'], notif_row['msg'], listing_row['name'], image_row['img_url'],
                    borrower_username=borrower_username, headshot=headshot, time_created=time_created)
                lender_notifications.append(notification)

    return lender_notifications

# gets all of a given user's notifications where they are the borrower
def get_borrower_notifications(user_id):
    borrower_notifications = []

    with sqlalchemy.orm.Session(_engine) as session:
        stmt = sqlalchemy.select(Notification, Listing, Image, User.username, User.headshot)
        stmt = stmt.where(Notification.to_user_id == user_id)
        stmt = stmt.where(Notification.notif_type != NotificationTypes.LIKE_NOTIFICATION.value)
        stmt = stmt.where(Listing.id == Notification.listing_id)
        stmt = stmt.where(Image.listing_id == Notification.listing_id)
        stmt = stmt.where(User.id == Notification.from_user_id)
        stmt = stmt.where(Image.is_primary == True)
        stmt = stmt.order_by(Notification.id.desc())
        table = session.execute(stmt).all()
        for tup in table:
            notif_row, listing_row, image_row = tup[0].__dict__, tup[1].__dict__, tup[2].__dict__
            lender_username, headshot = tup[3], tup[4]

            if ((notif_row['notif_type'] != NotificationTypes.BORROWER_RECEIVED_ITEM.value) and (notif_row['notif_type'] != NotificationTypes.BORROWER_RETURNED_ITEM.value)):

                time = str(notif_row['time_created']).split(":")
                hour, minute, secs = int(time[0]), int(time[1]), round(float(time[2]))
                # FOR TIMEZONE DIFF FROM UTC
                time_in_minutes = hour * 60 + minute
                four_hours_ago_in_minutes = time_in_minutes - 4 * 60
                while four_hours_ago_in_minutes < 0:
                    four_hours_ago_in_minutes += 24 * 60
                four_hours_ago_hour, four_hours_ago_minute = divmod(four_hours_ago_in_minutes, 60)
                time_created = '{:02d}:{:02d}:{:02d}'.format(four_hours_ago_hour, four_hours_ago_minute, secs)

                notification = notificationmod.Notification(notif_row['id'], notif_row['notif_type'], notif_row['listing_id'],
                        notif_row['to_user_id'], notif_row['from_user_id'], notif_row['date_created'],
                        notif_row['transaction_id'], notif_row['msg'], listing_row['name'], image_row['img_url'],
                        lender_username=lender_username, headshot=headshot, time_created=time_created)
                borrower_notifications.append(notification)

    return borrower_notifications