#!/usr/bin/env python

# -----------------------------------------------------------------------
# transaction.py
# -----------------------------------------------------------------------


class Transaction:
    def __init__(self, id, listing_id, to_user_id, from_user_id, date_created, status, request_msg=None, date_lent_out=None, date_returned=None, borrower_username=None, lender_username=None, other_phone_number=None):
        self.id = id
        self.listing_id = listing_id
        self.to_user_id = to_user_id
        self.from_user_id = from_user_id
        self.date_created = date_created
        self.status = status
        self.request_msg = request_msg
        self.date_lent_out = date_lent_out
        self.date_returned = date_returned
        self.borrower_username = borrower_username
        self.lender_username = lender_username
        self.other_phone_number = other_phone_number

    def get_id(self):
        return self.id

    def get_listing_id(self):
        return self.listing_id

    def get_to_user_id(self):
        return self.to_user_id

    def get_from_user_id(self):
        return self.from_user_id

    def get_date_created(self):
        return self.date_created

    def get_status(self):
        return self.status

    def get_request_msg(self):
        return self.request_msg

    def get_date_lent_out(self):
        return self.date_lent_out

    def get_date_returned(self):
        return self.date_returned

    def get_borrower_username(self):
        return self.borrower_username

    def get_lender_username(self):
        return self.lender_username
    
    def get_other_phone_number(self): 
        return self.other_phone_number

    def to_tuple(self):
        return (self.id,
        self.listing_id,
        self.to_user_id,
        self.from_user_id,
        self.date_created,
        self.status,
        self.request_msg,
        self.date_lent_out,
        self.date_returned, self.borrower_username,
        self.lender_username,
        self.other_phone_number)
