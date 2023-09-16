from constants import *
from services.database import User
from services.database import Transaction
from services.database import _engine

import sqlalchemy.ext.declarative
import sqlalchemy

# -----------------------------------------------------------------------
def update_points(name, points):
    with sqlalchemy.orm.Session(_engine) as session:
        user = session.query(User).where(User.username == str(name)).one_or_none()
        prev_balance = user.balance
        new_balance = prev_balance + points
        user.balance = new_balance
        session.commit()
        session.close()
    return new_balance

# -----------------------------------------------------------------------
# grab the start date for a listing from transaction
def get_start_date(transaction_id):
    with sqlalchemy.orm.Session(_engine) as session:
        transaction = session.query(Transaction).where(Transaction.id == transaction_id).one_or_none()
        date_lent_out = transaction.date_lent_out
    return date_lent_out

# -----------------------------------------------------------------------
# grab the end date for a listing from transaction
def get_end_date(transaction_id):
    with sqlalchemy.orm.Session(_engine) as session:
        transaction = session.query(Transaction).where(Transaction.id == transaction_id).one_or_none()
        date_returned = transaction.date_returned
    return date_returned