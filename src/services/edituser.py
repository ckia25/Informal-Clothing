#!/usr/bin/env python

# -----------------------------------------------------------------------
# newuser.py
# -----------------------------------------------------------------------

from importlib.util import find_spec
from logging.config import valid_ident
import sys
import os

import sqlalchemy
import sqlalchemy.orm

import services.database as database
from services.database import _engine
import classes.user as usermod
import cloudinary.uploader
from constants import ImageSizes, Modals, inputLimits

# -----------------------------------------------------------------------


def remove_user(id):

    with sqlalchemy.orm.Session(_engine) as session:
        stmt = (sqlalchemy.delete(database.User).where(database.User.id == id))
        session.execute(stmt)
        session.commit()

# -----------------------------------------------------------------------

# took out address for now


def create_user(username, email, address=None, balance=0, headshot=None,
                        first_name=None, last_name=None, bio=None, phone_number=None):
    with sqlalchemy.orm.Session(_engine) as session:

        new_user = database.User(username=username,
                                email=email, address=address,
                                balance=balance, headshot=headshot,
                                first_name=first_name, last_name=last_name,
                                bio=bio, phone_number=phone_number)
        session.add(new_user)
        session.commit()
        session.flush()
        session.refresh(new_user)
        new_user_obj = usermod.User(new_user.id, new_user.username,
                                    new_user.email, new_user.address,
                                    new_user.balance, new_user.headshot,
                                    new_user.first_name, new_user.last_name,
                                    new_user.bio, new_user.phone_number)

    return new_user_obj
# -----------------------------------------------------------------------

def get_user(username):
    with sqlalchemy.orm.Session(_engine) as session:
        row = session.scalars(
            sqlalchemy.select(database.User).filter(
                database.User.username.ilike(username))).one_or_none()

        if not row:
            return None

        user = usermod.User(row.id, row.username, row.email,
                            row.address, row.balance, row.headshot,
                            row.first_name, row.last_name, row.bio, row.phone_number)

    return user
# -----------------------------------------------------------------------
def get_headshot_url(headshot_file):
    response = cloudinary.uploader.upload(headshot_file,
                                            transformation=[
                                                {'width': ImageSizes.WIDTH.value,
                                                'height': ImageSizes.HEIGHT.value,
                                                'crop': 'fill'},
                                            ])
    img_url = response['secure_url']
    return  img_url


# -----------------------------------------------------------------------
def restrict_string_input(str, limit):
    if len(str) > limit:
        return str[:limit]
    return str

# -----------------------------------------------------------------------
def edit_user(username, form, headshot_file):

    with sqlalchemy.orm.Session(_engine) as session:
        address = form.get('address', None)
        first_name = form.get('first_name', None)
        last_name = form.get('last_name', None)
        bio = form.get('bio', None)
        phone_number = form.get('phone_number', None)

        user = session.scalars(
            sqlalchemy.select(database.User).filter(
                database.User.username.ilike(username))).one_or_none()
        if user == None:
            return None
        if address != None:
            user.address = address
        if headshot_file != None and headshot_file.filename != '':
            user.headshot = get_headshot_url(headshot_file)
        if first_name != None:
            user.first_name = restrict_string_input(first_name, inputLimits.NAME_LIMIT.value)
        if last_name != None:
            user.last_name = restrict_string_input(last_name, inputLimits.NAME_LIMIT.value)
        if bio != None:
            user.bio = restrict_string_input(bio, inputLimits.BIO_LIMIT.value)
        if phone_number != None:
            user.phone_number = phone_number
        session.commit()

# -----------------------------------------------------------------------
def get_username(user_id):
    with sqlalchemy.orm.Session(_engine) as session:
        row = session.scalars(
            sqlalchemy.select(database.User.username).filter(
                (database.User.id == user_id))).one_or_none()

        return row
# -----------------------------------------------------------------------

def verify_input_edit_profile(username, form):
    return True, Modals.EDIT_PROFILE_SUCCESS.value




# -----------------------------------------------------------------------


def _test():
    get_username('1')


if __name__ == '__main__':
    _test()
