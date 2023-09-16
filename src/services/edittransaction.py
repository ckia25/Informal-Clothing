#!/usr/bin/env python

# ----------------------------------------------------------------------
# edittransaction.py
#-----------------------------------------------------------------------

import services.database as database
from services.database import _engine, Transaction
import classes.transaction as transactionmod

import sqlalchemy.orm
import sqlalchemy

#-----------------------------------------------------------------------


def remove_transaction(id):

    with sqlalchemy.orm.Session(_engine) as session:
        stmt = (sqlalchemy.delete(database.Transaction).where(
            database.Transaction.id == id))
        session.execute(stmt)
        session.commit()


#-----------------------------------------------------------------------
def get_all_transactions():
    transactions = []

    with sqlalchemy.orm.Session(_engine) as session:
        table = session.scalars(
            sqlalchemy.select(database.Transaction)
            .order_by(database.Transaction.id)).all()
        for row in table:
            transaction = transactionmod.Transaction(row.id, row.listing_id,
                                                     row.to_user_id, row.from_user_id, row.date_created, row.status,
                                                     row.request_msg, row.date_lent_out, row.date_returned)
            transactions.append(transaction)
    return transactions

#-----------------------------------------------------------------------
def _test():
    remove_transaction(id=10)
    print('Transactions:')
    transactions = get_all_transactions()
    for transaction in transactions:
        print(transaction.to_tuple())
        print()


if __name__ == '__main__':
    _test()
