#!/usr/bin/env python

# -----------------------------------------------------------------------
# availability.py
# -----------------------------------------------------------------------

class Availability:
    def __init__(self, id, listing_id, borrower_userid, start_date, end_date):
        self.id = id
        self.listing_id = listing_id
        self.borrower_userid = borrower_userid
        self.start_date = start_date
        self.end_date = end_date

    def get_id(self):
        return self.id

    def get_listing_id(self):
        return self.listing_id

    def get_borrower_userid(self):
        return self.borrower_userid

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def to_tuple(self):
        return (self.id,
        self.listing_id,
        self.borrower_userid,
        self.start_date,
        self.end_date)
