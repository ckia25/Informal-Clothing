#!/usr/bin/env python

# -----------------------------------------------------------------------
# editlike.py
# -----------------------------------------------------------------------

from services.database import Like
from services.database import _engine

import sqlalchemy.orm
import sqlalchemy

# -----------------------------------------------------------------------

def like_clicked(user_id, listing_id):

    with sqlalchemy.orm.Session(_engine) as session:

        stmt = sqlalchemy.delete(Like)
        stmt = stmt.where(Like.listing_id == listing_id)
        stmt = stmt.where(Like.user_id == user_id)
        result = session.execute(stmt)
        session.commit()
        session.flush()

        if result.rowcount == 0:
            add_like(user_id, listing_id)

# -----------------------------------------------------------------------

def remove_like(user_id, listing_id):

    with sqlalchemy.orm.Session(_engine) as session:

        stmt = (sqlalchemy.delete(Like).where(
            Like.user_id == user_id).
            where(Like.listing_id == listing_id))
        session.execute(stmt)
        session.commit()
        session.flush()
        session.refresh()

# -----------------------------------------------------------------------

def add_like(user_id, listing_id):

    with sqlalchemy.orm.Session(_engine) as session:

        new_like = Like(user_id = user_id, listing_id = listing_id)
        session.add(new_like)
        session.commit()
        session.flush()
        session.refresh(new_like)

# -----------------------------------------------------------------------


def check_if_liked(user_id, listing_id):

    with sqlalchemy.orm.Session(_engine) as session:

        stmt = sqlalchemy.select(Like.listing_id)
        stmt = stmt.where(Like.listing_id == listing_id)
        stmt = stmt.where(Like.user_id == user_id)
        like = session.execute(stmt).all()

        for row in like:
            session.delete(row)
            
        return False
    
# -----------------------------------------------------------------------

def _test():
    print('before inserting like:')
    print()
    if check_if_liked(123, 456):
        print('like exists')
    else:
        print('like does not exist')
    add_like(1, 123, 456)
    print('after adding like:')
    print()
    if check_if_liked(123, 456):
        print('like exists')
        remove_like(123, 456)
    else:
        print('like does not exist')

if __name__ == '__main__':
    _test()