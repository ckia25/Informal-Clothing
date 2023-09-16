import sys
from constants import *
import services.database as database
from services.database import User, Rating
from services.database import _engine
import datetime
import classes.ratinghistory as ratinghistorymod

import sqlalchemy.ext.declarative
import sqlalchemy

from config import config_cloudinary
config_cloudinary()

# -----------------------------------------------------------------------


def rate_user(rating, user_rated_id, user_rating_id, date_rated, transaction_id, msg, rated_is_borrower):
    try:
        with sqlalchemy.orm.Session(_engine) as session:
            stmt = sqlalchemy.select(Rating)
            stmt = stmt.where(Rating.transaction_id == transaction_id)
            stmt = stmt.where(Rating.user_rated_id == user_rated_id)
            results = session.execute(stmt).first()
            if results:
                raise Exception("Cannot rate a user multiple times!")

            new_rating = database.Rating(rating=rating, user_rated_id=user_rated_id, user_rating_id=user_rating_id,
                                        date_rated=date_rated, transaction_id=transaction_id, msg=msg, rated_is_borrower=rated_is_borrower)
            session.add(new_rating)
            session.commit()
    except Exception as err:
        print(err, file=sys.stderr)
        raise Exception(err)

# -----------------------------------------------------------------------


def get_lender_rating_history(user_id):
    ratinghistory = []
    with sqlalchemy.orm.Session(_engine) as session:
        table = session.query(User.username, User.first_name, User.last_name,
                              Rating.rating, User.headshot, Rating.msg).where(
            User.id == Rating.user_rating_id).where(
            user_id == Rating.user_rated_id).where(
            Rating.rated_is_borrower.is_(False)).all()

        for tup in table:
            username, fname, lname, rating, headshot, msg = tup
            rating = ratinghistorymod.RatingHistory(
                username, fname, lname, headshot, rating, msg)

            ratinghistory.append(rating)

    return ratinghistory

# -----------------------------------------------------------------------


def get_borrower_rating_history(user_id):
    ratinghistory = []
    with sqlalchemy.orm.Session(_engine) as session:
        table = session.query(User.username, User.first_name, User.last_name,
                              Rating.rating, User.headshot, Rating.msg).where(
            User.id == Rating.user_rating_id).where(
            user_id == Rating.user_rated_id).where(
            Rating.rated_is_borrower.is_(True)).all()

        for tup in table:
            username, fname, lname, rating, headshot, msg = tup
            rating = ratinghistorymod.RatingHistory(
                username, fname, lname, headshot, rating, msg)

            ratinghistory.append(rating)

    return ratinghistory


# -----------------------------------------------------------------------

# returns tuple of arrays: borrower_history, lender_history
def get_all_rating_history(user_id):
    borrower_history, lender_history = [], []
    with sqlalchemy.orm.Session(_engine) as session:
        table = session.query(User.username, User.first_name, User.last_name,
                              Rating.rating, User.headshot, Rating.msg,
                              Rating.rated_is_borrower).where(
            User.id == Rating.user_rating_id).where(
            user_id == Rating.user_rated_id).all()

        for tup in table:
            username, fname, lname, rating, headshot, msg, is_borrower = tup
            rating = ratinghistorymod.RatingHistory(
                username, fname, lname, headshot, rating, msg)
            if is_borrower:
                borrower_history.append(rating)
            else:
                lender_history.append(rating)

    return borrower_history, lender_history


# -----------------------------------------------------------------------
def _test_rate_user():
    print("lender user #100 rating user #1 as borrower 5 times, 1-5:")
    for i in range(1, 6):
        rate_user(i, 6, 100, datetime.datetime.today(),
                  i, "Test msg for rating #%d" % i, True)


def _test_get_rating_history():
    b, l = get_all_rating_history(1)
    print("b ratings")
    for rating in b:
        print(rating.to_tuple())
    print("l ratings")
    for rating in l:
        print(rating.to_tuple())


if __name__ == '__main__':
    _test_get_rating_history()