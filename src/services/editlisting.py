#!/usr/bin/env python

# -----------------------------------------------------------------------
# editlisting.py
# This file is dedicated for basic functions that interact with the
# listings table in database
# -----------------------------------------------------------------------

from constants import get_random_size, get_test_image_urls
import services.database as database
from services.database import _engine
from services.listingservice import get_all_listings
from services.rentalrequestservice import create_transaction
from constants import *
import sys
import sqlalchemy.orm
import sqlalchemy
import services.listingformservice as listingformservice

import services.editimage as editimage

from config import config_cloudinary
config_cloudinary()
from cloudinary import uploader
import random

#-----------------------------------------------------------------------

# Constants
STATUS_AVAILABLE = 'Available'
TEST = 'test'
#-----------------------------------------------------------------------
# Prevent large string inputs
def verify_input_editlisting_submit(form):
    try:
        price = form['price']
        if price == None or int(price) < defaults.MIN_PRICE.value or int(price) > defaults.MAX_PRICE.value:
            raise Exception("Price invalid")
        if form['name'] == None:
            raise Exception("Name invalid")
        if form['category'] == None:
            raise Exception("Category invalid")
        if form['subcategory'] == None:
            raise Exception("Subcategory invalid")
        if form['size'] == None:
            raise Exception("Size invalid")
        # This should check regular expression to confirm that we are getting dates
        for key in form:
                if 'blackoutDate' in key:
                    if len(form[key].split(' - ')) != 2:
                        raise Exception("Invalid Blackout Dates")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return False, Modals.EDIT_LISTING_FAILURE.value

    return True, Modals.EDIT_LISTING_SUCCESS.value


#-----------------------------------------------------------------------
def edit_listing(id, args):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        if args['name'] != None:
            listing.name = listingformservice.restrict_listing_title(args['name'])
        if args['price'] != -1:
            listing.price = int(args['price'])
        if args['category'] != None:
            listing.category = args['category']
        if args['size'] != None:
            listing.size = args['size']
        if args['subcategory'] != None:
            listing.subcategory = args['subcategory']
        if args['description'] != None:
            listing.description = listingformservice.restrict_listing_description(args.get('description', ''))
        
        session.commit()

#-----------------------------------------------------------------------
def remove_listing(id):
    with sqlalchemy.orm.Session(_engine) as session:
        stmt = (sqlalchemy.delete(database.Listing).where(
            database.Listing.id == id))
        session.execute(stmt)
        session.commit()

#-----------------------------------------------------------------------
def edit_name(id, new_name):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.name = new_name
        session.commit()

# -----------------------------------------------------------------------
def edit_price(id, new_price):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.price = new_price
        session.commit()

# -----------------------------------------------------------------------
def edit_size(id, new_size):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.size = new_size
        session.commit()

# -----------------------------------------------------------------------
def edit_category(id, new_category):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.category = new_category
        session.commit()

# -----------------------------------------------------------------------
def edit_subcategory(id, new_subcategory):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.subcategory = new_subcategory
        session.commit()

# -----------------------------------------------------------------------
def edit_description(id, new_description):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.description = new_description
        session.commit()

# -----------------------------------------------------------------------
def edit_status(id, new_status):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.status = new_status
        session.commit()

# -----------------------------------------------------------------------
def edit_pickup_location(id, new_pickup_location):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.pickup_location = new_pickup_location
        session.commit()

# -----------------------------------------------------------------------
def increment_likes(id):
    with sqlalchemy.orm.Session(_engine) as session:
        listing = session.query(database.Listing).filter(database.Listing.id == id).first()
        listing.likes += 1
        session.commit()

# -----------------------------------------------------------------------
def remove_test_listings():
    with sqlalchemy.orm.Session(_engine) as session:
        stmt = (sqlalchemy.delete(database.Listing).where(
            database.Listing.description == TEST))
        session.execute(stmt)
        session.commit()

# -----------------------------------------------------------------------
def create_listing_basic(name, category, subcategory, size, price, url):

    with sqlalchemy.orm.Session(_engine) as session:

        # could be replaced by a create listing call.
        new_listing = database.Listing(user_id=1,
                                    name=name,
                                    price=price,
                                    category=category,
                                    size=size,
                                    subcategory=subcategory,
                                    description=TEST,
                                    status=STATUS_AVAILABLE,
                                    pickup_location='',
                                    likes=0)
        session.add(new_listing)
        session.commit()
        session.flush()
        session.refresh(new_listing)

        editimage.create_image(
        listing_id=new_listing.id, is_primary=True, img_url=url,
        cloudinary_id=TEST)

    return new_listing.id
# -----------------------------------------------------------------------
def create_test_listing(session):
        new_listing = database.Listing(user_id=1,
                                    name='Test Listing',
                                    price=0,
                                    category='menswear',
                                    size='M',
                                    subcategory='shirt',
                                    description=TEST,
                                    status=STATUS_AVAILABLE,
                                    pickup_location='',
                                    likes=0)
        session.add(new_listing)
        session.commit()
        session.flush()
        session.refresh(new_listing)
        id = new_listing.id
        new_image = database.Image(
            is_primary=True,
            listing_id=id,
            img_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJTJGTHPV8zKF-jU55m-IoLAZwW5_XbnsA4xWcG-md__I1DGe6sQLkLZrpb1f4KrlclOQ&usqp=CAU',
             cloudinary_id='cloudinary_id')
        session.add(new_image)
        session.commit()

# -----------------------------------------------------------------------
# creates n test listings and adds them to the database
def create_test_listings(n):
    images = get_test_image_urls()
    k = len(images)
    for i in range(0, n):
        j = i % k
        price = random.randint(10, 1000)
        listing_id = create_listing_basic(name = 'BASIC_TEST_LISTING',
                            category=images[j][0],
                            subcategory=images[j][1],
                            size=get_random_size(),
                            price=price,
                            url=images[j][2])
        # create_transaction(listing_id=listing_id,
        #                     from_user_id=1)

def create_duplicate_listings(n):
    with sqlalchemy.orm.Session(_engine) as session:
        for i in range(0, n):
            create_test_listing(session)


def _test():
    # create_test_listings(10)
    test_id = create_listing_basic("katie's test listing", "female", "skirt",
        "small", 100,
        "https://dogexpress.in/wp-content/uploads/2016/03/dog-underwater-660x330.jpg")
    all_listings = get_all_listings()
    print("Listing before edits:")
    print()
    for listing in all_listings:
        if listing.get_id() == test_id:
            print(listing.to_tuple())
    print()
    edit_description(test_id, "new description for test listing")
    edit_category(test_id, "menswearTEST")
    edit_subcategory(test_id, "sweatshirt")
    edit_name(test_id, "new name")
    edit_pickup_location(test_id, "new location")
    edit_price(test_id, 200)
    edit_status(test_id, "not available")
    increment_likes(test_id)
    all_listings = get_all_listings()
    print("Listing after edits:")
    print()
    for listing in all_listings:
        if listing.get_id() == test_id:
            print(listing.to_tuple())
    remove_listing(test_id)


if __name__ == '__main__':
    create_test_listings(10)
    # create_duplicate_listings(10000)
