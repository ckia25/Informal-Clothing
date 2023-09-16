#!/usr/bin/env python

# -----------------------------------------------------------------------
# editimage.py
# This file is dedicated for basic functions that interact with the
# images table in database
# -----------------------------------------------------------------------
import services.database as database
from services.database import _engine

import sqlalchemy.orm
import sqlalchemy

#-----------------------------------------------------------------------
TEST = 'test'
#-----------------------------------------------------------------------
def create_image(listing_id, is_primary, img_url, cloudinary_id):

    with sqlalchemy.orm.Session(_engine) as session:

        new_image = database.Image(
            is_primary=is_primary,
            listing_id=listing_id,
            img_url=img_url, cloudinary_id=cloudinary_id)
        session.add(new_image)
        session.commit()

# -----------------------------------------------------------------------
def remove_image(id):

    with sqlalchemy.orm.Session(_engine) as session:
        stmt = (sqlalchemy.delete(database.Image).where(
            database.Image.id == id))
        session.execute(stmt)
        session.commit()

# -----------------------------------------------------------------------
def remove_test_images():

    with sqlalchemy.orm.Session(_engine) as session:
        stmt = (sqlalchemy.delete(database.Image).where(
            database.Image.cloudinary_id == TEST))
        session.execute(stmt)
        session.commit()

# -----------------------------------------------------------------------
def _test():
    print()

if __name__ == '__main__':
    _test()