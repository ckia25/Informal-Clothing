#!/usr/bin/env python

# -----------------------------------------------------------------------
# notification.py
# -----------------------------------------------------------------------


class Notification:
    def __init__(self, id, notif_type, listing_id, to_user_id, from_user_id,
        date_created, transaction_id, msg, name, img_url, borrower_username=None,
        lender_username=None, headshot=None, time_created=None):
        self.id = id
        self.notif_type = notif_type
        self.listing_id = listing_id
        self.to_user_id = to_user_id
        self.from_user_id = from_user_id
        self.date_created = date_created
        self.transaction_id = transaction_id
        self.msg = msg
        self.name = name
        self.img_url = img_url
        self.borrower_username = borrower_username
        self.lender_username = lender_username
        self.headshot = headshot
        self.time_created = time_created

    def get_id(self):
        return self.id

    def get_notif_type(self):
        return self.notif_type

    def get_listing_id(self):
        return self.listing_id

    def get_to_user_id(self):
        return self.to_user_id

    def get_from_user_id(self):
        return self.from_user_id

    def get_date_created(self):
        return self.date_created

    def get_transaction_id(self):
        return self.transaction_id

    def get_msg(self):
        return self.msg

    def get_name(self):
        return self.name

    def get_img_url(self):
        return self.img_url

    def get_borrower_username(self):
        return self.borrower_username

    def get_lender_username(self):
        return self.lender_username

    def get_headshot(self):
        return self.headshot

    def get_time_created(self):
        return self.time_created


    def to_tuple(self):
        return (self.id,
        self.notif_type,
        self.listing_id,
        self.to_user_id,
        self.from_user_id,
        self.date_created,
        self.transaction_id,
        self.msg,
        self.name,
        self.img_url,
        self.borrower_username,
        self.lender_username,
        self.headshot,
        self.time_created)