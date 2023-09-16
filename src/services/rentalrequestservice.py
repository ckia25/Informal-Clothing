#!/usr/bin/env python

# -----------------------------------------------------------------------
# rentalrequestservice.py
# handles route('/rentalrequest')
# endpoint
# -----------------------------------------------------------------------

import datetime
import sqlalchemy.orm
from sqlalchemy.sql import func
from services.database import Availability, Listing, Transaction, User, Rating, _engine
import classes.availability as availabilitymod
from constants import Status

from services.edittransaction import get_all_transactions

# -----------------------------------------------------------------------


def create_unavailable_date(listing_id, transaction_id, borrower_userid, start_date, end_date):
    with sqlalchemy.orm.Session(_engine) as session:

        date_range = Availability(listing_id=listing_id, transaction_id=transaction_id,
                                  borrower_userid=borrower_userid,
                                  start_date=start_date, end_date=end_date)
        session.add(date_range)
        session.commit()


# -----------------------------------------------------------------------


def remove_unavailable_date(transaction_id):
    with sqlalchemy.orm.Session(_engine) as session:

        stmt = (sqlalchemy.delete(Availability).where(
            Transaction.id == id))
        session.execute(stmt)
        session.commit()

# -----------------------------------------------------------------------


def get_unavailable_dates(listing_id):
    with sqlalchemy.orm.Session(_engine) as session:

        unavailable_dates = session.scalars(
            sqlalchemy.select(Availability).where(Listing.id == listing_id)
            .where(Availability.listing_id == listing_id)).all()

        date_ranges = []
        for row in unavailable_dates:
            range = (str(row.start_date), str(row.end_date))
            date_ranges.append(range)

        return date_ranges

# -----------------------------------------------------------------------


def create_transaction(listing_id, from_user_id, to_user_id,  date_created, date_lent_out, date_returned, request_msg=None):
    with sqlalchemy.orm.Session(_engine) as session:
        transaction = Transaction(listing_id=listing_id,
                                  from_user_id=from_user_id,
                                  to_user_id=to_user_id,
                                  date_created=date_created,
                                  request_msg=request_msg,
                                  date_lent_out=date_lent_out,
                                  date_returned=date_returned,
                                  status=Status.REQUESTED.value)
        session.add(transaction)
        session.commit()
        session.flush()
        session.refresh(transaction)
        return transaction.id

# -----------------------------------------------------------------------


def get_listing_creator(listing_id):

    with sqlalchemy.orm.Session(_engine) as session:
        listing_creator_id = session.scalars(
            sqlalchemy.select(Listing.user_id).where(Listing.id == listing_id)).one_or_none()

    return listing_creator_id

# -----------------------------------------------------------------------

def get_listing_borrower(transaction_id):

    with sqlalchemy.orm.Session(_engine) as session:
        listing_borrower_id = session.scalars(
            sqlalchemy.select(Transaction.to_user_id).where(Transaction.id == transaction_id)).one_or_none()

    return listing_borrower_id


# -----------------------------------------------------------------------

def get_listing_price(listing_id):

    with sqlalchemy.orm.Session(_engine) as session:
        listing_creator_id = session.scalars(
            sqlalchemy.select(Listing.price).where(Listing.id == listing_id)).one_or_none()

    return listing_creator_id

# ----------------------------------------------------------------------


def get_lender_username_and_rating(user_id):
    return get_user_ratings_helper(user_id, rated_is_borrower=False)


def get_borrower_username_and_rating(user_id):
    return get_user_ratings_helper(user_id, rated_is_borrower=True)

def get_user_ratings_helper(user_id, rated_is_borrower):
    with sqlalchemy.orm.Session(_engine) as session:
        ratings = session.query(User.username, func.avg(Rating.rating),
                                func.count(Rating.rating)).where(
            User.id == user_id).where(
            Rating.rated_is_borrower == rated_is_borrower).where(
            User.id == Rating.user_rated_id).group_by(User.username).one_or_none()

        if not ratings:
            username = session.query(User.username).where(
                User.id == user_id).one_or_none()[0]
            return (username, 0, 0)

        username, avg_rating, count = ratings[0], ratings[1], ratings[2]

        return (username, avg_rating, count)

# ----------------------------------------------------------------------

def remove_availability(transaction_id):

    with sqlalchemy.orm.Session(_engine) as session:

        stmt = sqlalchemy.delete(Availability).where(
            Availability.transaction_id == transaction_id)

        session.execute(stmt)
        session.commit()

# -----------------------------------------------------------------------


def _test():
    print("Testing ratings:")
    print(get_lender_username_and_rating(1))


if __name__ == '__main__':
    _test()
