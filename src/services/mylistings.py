#!/usr/bin/env python

# -----------------------------------------------------------------------
# mylistings.py
# handles route("/mylistings") endpoint
# -----------------------------------------------------------------------

import services.database as database
from services.database import Listing
from services.database import Image
from services.database import _engine
import services.listingservice as listingservice

import sqlalchemy.ext.declarative
import sqlalchemy

import classes.listing as listingmod
import classes.image as imagemod

from config import config_cloudinary
config_cloudinary()
from cloudinary import uploader
from cloudinary.utils import cloudinary_url


#-----------------------------------------------------------------------
# This function gets all of the listings that the user has posted

def get_my_listings(user_id):
    listings = []

    with sqlalchemy.orm.Session(_engine) as session:
        table = session.scalars(
            sqlalchemy.select(Listing).where(Listing.user_id == user_id).order_by(Listing.id))
        for row in table:
            images = listingservice.get_listing_images(session, row.id)
            listing = listingmod.Listing(row.id, row.user_id, row.name,
                                         row.price, row.category, row.size, row.subcategory,
                                         row.description, row.status, row.pickup_location,
                                         images, likes=row.likes)
            listings.append(listing)
    return listings

# -----------------------------------------------------------------------

def test_get_listings():
    listings = get_my_listings(1)
    for post in listings:
        print(post.to_tuple())
        print()

def _test():
    print()

if __name__ == '__main__':
    test_get_listings()

