from constants import Status
from constants import NotificationTypes
from services.database import Rating, _engine, Image

import sqlalchemy.ext.declarative
import sqlalchemy
from sqlalchemy import nullslast, or_
from sqlalchemy.orm import aliased
import classes.transaction as transactionmod
import classes.listing as listingmod
import classes.image as imagemod
from services.listingservice import create_image_object
import services.getpointsservice as getpointsservice
import services.rentalrequestservice as rentalrequestservice
import services.edituser as edituser

from services.database import Listing
from services.database import Transaction
from services.database import User
from datetime import datetime

from services.editnotification import add_notification
from services.listingservice import get_listing_images

# -----------------------------------------------------------------------

# Returns a list of a user's current listings that they are borrowing.


def get_user_borrowing_listings(user_id):

    with sqlalchemy.orm.Session(_engine) as session:
        listings = []

        res = session.query(
            Transaction, Listing, Image, User.username, User.phone_number).where(
            Transaction.listing_id == Listing.id).where(
            Transaction.to_user_id == user_id).where(
            User.id == Transaction.from_user_id).where(
            Image.listing_id == Listing.id).where(
            Image.is_primary == True).order_by(nullslast(Transaction.id.desc())).all()

        for tup in res:
            transaction_dict, listing_dict = tup[0].__dict__, tup[1].__dict__
            img_dict, lender_username, other_number = tup[2].__dict__, tup[3], tup[4]

            transaction = transactionmod.Transaction(transaction_dict['id'],
                                                     transaction_dict['listing_id'], transaction_dict['to_user_id'],
                                                     transaction_dict['from_user_id'], transaction_dict['date_created'],
                                                     transaction_dict['status'], transaction_dict[
                                                         'request_msg'], transaction_dict['date_lent_out'],
                                                     transaction_dict['date_returned'], lender_username=lender_username, other_phone_number=other_number)

            image = create_image_object(img_dict)

            listing = listingmod.Listing(listing_dict['id'], listing_dict['user_id'], listing_dict['name'],
                                         listing_dict['price'], listing_dict['category'], listing_dict['size'],
                                         listing_dict['subcategory'], listing_dict['description'],
                                         listing_dict['status'], listing_dict['pickup_location'],
                                         [image], transaction, likes=listing_dict['likes'], poster=lender_username)

            listings.append(listing)

    return listings


# -----------------------------------------------------------------------
# Returns a list of a user's current listings that they are lending.

def get_user_lending_listings(user_id):

    with sqlalchemy.orm.Session(_engine) as session:
        listings = []

        res = session.query(
            Transaction, Listing, Image, User.username, User.phone_number).where(
            Transaction.listing_id == Listing.id).where(
            Transaction.from_user_id == user_id).where(
            User.id == Transaction.to_user_id).where(
            Image.listing_id == Listing.id).where(
            Image.is_primary == True).order_by(nullslast(Transaction.id.desc())).all()

        for tup in res:
            transaction_dict, listing_dict = tup[0].__dict__, tup[1].__dict__
            img_dict, borrower_username, other_number = tup[2].__dict__, tup[3], tup[4]

            transaction = transactionmod.Transaction(transaction_dict['id'],
                                                     transaction_dict['listing_id'], transaction_dict['to_user_id'],
                                                     transaction_dict['from_user_id'], transaction_dict['date_created'],
                                                     transaction_dict['status'], transaction_dict[
                                                         'request_msg'], transaction_dict['date_lent_out'],
                                                     transaction_dict['date_returned'], borrower_username=borrower_username, other_phone_number=other_number)

            image = create_image_object(img_dict)

            listing = listingmod.Listing(listing_dict['id'], listing_dict['user_id'], listing_dict['name'],
                                         listing_dict['price'], listing_dict['category'], listing_dict['size'],
                                         listing_dict['subcategory'], listing_dict['description'],
                                         listing_dict['status'], listing_dict['pickup_location'],
                                         [image], transaction, likes=listing_dict['likes'])

            listings.append(listing)

    return listings


# -----------------------------------------------------------------------


# Returns the most recent transaction for listing with id == listing_id.


def get_listing_transaction(listing_id):

    with sqlalchemy.orm.Session(_engine) as session:
        row = session.scalars(
            sqlalchemy.select(Transaction)
            .where(Transaction.listing_id == listing_id)
            .order_by(Transaction.id)).one()

        transaction = transactionmod.Transaction(
            row.id, row.listing_id, row.to_user_id,
            row.from_user_id, row.date_created, row.status, row.request_msg, row.date_lent_out, row.date_returned)

    return transaction

# -----------------------------------------------------------------------

# Updates status after user interacts with update button on borrow/lending page.


def update_status(transaction_id, listing_id, user_id, current_date, early_return=False, msg=None):
    with sqlalchemy.orm.Session(_engine) as session:
        transaction = session.query(Transaction).where(
            Listing.id == Transaction.listing_id).where(
            Listing.id == listing_id).where(
            Transaction.from_user_id == user_id).where(
            Transaction.id == transaction_id).one_or_none()

        if transaction.status == Status.REQUESTED.value:
            transaction.status = Status.REQUEST_ACCEPTED.value
            add_notification(NotificationTypes.BORROW_REQUEST_ACCEPTED.value,
                             listing_id, transaction.to_user_id, transaction.from_user_id,
                             current_date, transaction_id, msg)

            # compute the profit for the lender
            listing_price = rentalrequestservice.get_listing_price(listing_id)
            start_date = getpointsservice.get_start_date(transaction_id)
            end_date = getpointsservice.get_end_date(transaction_id)
            delta = end_date - start_date
            num_days = delta.days + 1
            profit_from_renting = listing_price * num_days
            username = edituser.get_username(user_id)
            getpointsservice.update_points(username, profit_from_renting)
        elif transaction.status == Status.REQUEST_ACCEPTED.value:
            transaction.status = Status.BORROWER_HAS_POSSESSION.value
            add_notification(NotificationTypes.BORROWER_RECEIVED_ITEM.value,
                             listing_id, transaction.to_user_id, transaction.from_user_id,
                             current_date, transaction_id, msg)
        elif transaction.status == Status.BORROWER_HAS_POSSESSION.value:
            add_notification(NotificationTypes.BORROWER_RETURNED_ITEM.value,
                             listing_id, transaction.to_user_id, transaction.from_user_id,
                             current_date, transaction_id, msg)
            if early_return:
                transaction.status = Status.EARLY_RETURN.value
                add_notification(NotificationTypes.BACK_ON_MARKET.value,
                                 listing_id, transaction.to_user_id, transaction.from_user_id,
                                 current_date, transaction_id, msg)
            else:
                transaction.status = Status.RETURNED.value
        elif (transaction.status == Status.RETURNED.value or
              transaction.status == Status.EARLY_RETURN.value):
            transaction.status = Status.ON_THE_MARKET.value
            add_notification(NotificationTypes.BACK_ON_MARKET.value,
                             listing_id, transaction.to_user_id, transaction.from_user_id,
                             current_date, transaction_id, msg)

        session.commit()


# -----------------------------------------------------------------------

# Rejects a rental request and refunds the borrower

def reject_rental_request(transaction_id, listing_id, user_id):
    with sqlalchemy.orm.Session(_engine) as session:
        transaction = session.query(Transaction).where(
            Listing.id == Transaction.listing_id).where(
            Listing.id == listing_id).where(
            Transaction.from_user_id == user_id).where(
            Transaction.id == transaction_id).one_or_none()

        # refund the user
        listing_price = rentalrequestservice.get_listing_price(listing_id)
        start_date = getpointsservice.get_start_date(transaction_id)
        end_date = getpointsservice.get_end_date(transaction_id)
        delta = end_date - start_date
        num_days = delta.days + 1
        profit_from_renting = listing_price * num_days

        borrower_id = rentalrequestservice.get_listing_borrower(transaction_id)
        borrower = edituser.get_username(borrower_id)
        getpointsservice.update_points(borrower, profit_from_renting)

        # Drop the transaction from the table
        session.delete(transaction)
        session.commit()

# ----------------------------------------------------------------------


def get_current_stats_of_listing(listing_id):
    with sqlalchemy.orm.Session(_engine) as session:
        stats = session.scalars(
            sqlalchemy.select(Transaction.status)
            .where(Transaction.listing_id == listing_id)
            .order_by(Transaction.id)).all()

    return stats
# ----------------------------------------------------------------------


def _test():
    print("Calling get_curr_borrowed_listings(user_id=3):")
    listings = get_user_borrowing_listings(3)
    print("Res = ", listings[0].__dict__)

    print("Calling get_curr_lending_listings(user_id=1):")
    listings = get_user_lending_listings(1, 'mattd')
    print("Res = ", listings[0].__dict__)


if __name__ == '__main__':
    print("Testing refactored:")
    print(get_user_lending_listings(5))
