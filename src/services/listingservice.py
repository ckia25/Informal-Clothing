#!/usr/bin/env python

# -----------------------------------------------------------------------
# listingservice.py
# handles route("/listing") endpoint
# -----------------------------------------------------------------------

from logging import exception
from sys import stderr
from constants import *
from cloudinary.utils import cloudinary_url
from cloudinary import uploader
from typing import List
from services.database import Rating, User
from services.database import Listing
from services.database import Image
from services.database import _engine

import sqlalchemy.ext.declarative
import sqlalchemy
from sqlalchemy import func

import classes.listing as listingmod
import classes.image as imagemod

from config import config_cloudinary
config_cloudinary()

# -----------------------------------------------------------------------
def get_list_filter_args(args, filter_key, default_value):
    filter = args.get(filter_key, [default_value])
    if (type(filter) == type('') and filter != '' and filter != 'undefined'):
        filter = filter.split(',')
    else :
        filter = [default_value]
    return filter

# -----------------------------------------------------------------------
def get_filter_args(args):
    # gets the category:
    category = args.get('category', defaults.DEFAULT_CATEGORY.value)
    if category == 'undefined':
        category = defaults.DEFAULT_CATEGORY.value
    # gets the subcategory:
    subcategory = get_list_filter_args(args=args,
                                    filter_key='subcategories',
                                    default_value=defaults.DEFAULT_SUBCATEGORY.value)
    # gets the sizes:
    sizes = get_list_filter_args(args=args,
                                    filter_key='sizes',
                                    default_value=defaults.DEFAULT_SIZE.value)
    try:
        minprice = int(args.get('minprice', defaults.MIN_PRICE.value))
    except Exception:
        minprice = defaults.MIN_PRICE.value
    try:
        maxprice = int(args.get('maxprice', defaults.MAX_PRICE.value))
    except Exception:
        maxprice = defaults.MAX_PRICE.value
    sort = args.get('sort', defaults.DEFAULT_SORT.value)
    search = args.get('search')
    return category, subcategory, sizes, minprice, maxprice, sort, search
#-----------------------------------------------------------------------
def handle_sorting(stmt, sort):
    if sort == sortings.MOST_RECENT.value:
        return stmt.order_by(Listing.id.desc())
    elif sort == sortings.SORT_A_Z.value:
        return stmt.order_by(Listing.name.asc(), Listing.id.desc())
    elif sort == sortings.OLDEST.value:
        return stmt.order_by(Listing.id.asc())
    elif sort == sortings.SORT_PRICE_LOW_HIGH.value:
        return stmt.order_by(Listing.price.asc(), Listing.id.desc())
    elif sort == sortings.SORT_PRICE_HIGH_LOW.value:
        return stmt.order_by(Listing.price.desc(), Listing.id.desc())
    else:
        return stmt.order_by(Listing.id.desc(), Listing.id.desc())

# -----------------------------------------------------------------------
def create_image_object(image_row):
    image = imagemod.Image(image_row['id'], image_row['listing_id'],
    image_row['is_primary'], image_row['img_url'], image_row['cloudinary_id'])
    return image
# -----------------------------------------------------------------------
# given table of tuples with listing row, username, image row : returns all listings
# as listing objects
def create_listing_objects(sql_results):
    current_id = -1
    listings = []
    images = []
    listing = None
    i = 0
    for tup in sql_results:
        listing_row, username, image_row = tup[0].__dict__, tup[1], tup[2].__dict__
        # when there is new listings id
        if (current_id != image_row['listing_id']):
            if listing != None:
                # insert into the current listing the accumulated images
                if len(images) == 0:
                    print('There are no images associated with listing id: ' + str(image_row['listing_id']), file=stderr)
                else :
                    listing.images=images
                    listings.append(listing)

            # reset the images list
            images = []
            current_id = image_row['listing_id']
            listing = listingmod.Listing(listing_row['id'], listing_row['user_id'],
                                        listing_row['name'], listing_row['price'],
                                        listing_row['category'], listing_row['size'],
                                        listing_row['subcategory'],
                                        listing_row['description'], listing_row['status'],
                                        listing_row['pickup_location'], images=[],
                                        likes=listing_row['likes'], poster=username)


        # add a the current image to the image list
        image=create_image_object(image_row)
        if image.is_primary:
            images.insert(0, image)
        else:
            images.append(image)

        # handle last row in the table corner case
        if i == len(sql_results) - 1 and listing != None:
                if len(images) == 0:
                    print('There are no images associated with listing id: ' + str(image_row['listing_id']), file=stderr)
                else :
                    listing.images=images
                    listings.append(listing)
        i+=1
    return listings

# -----------------------------------------------------------------------
# Get Filtered Images. Given a list of strings for the filters return
# An ordered list of
def get_filtered_listings(category=defaults.DEFAULT_CATEGORY.value,
                          subcategory=[defaults.DEFAULT_SUBCATEGORY.value],
                          price_min=defaults.MIN_PRICE.value,
                          price_max=defaults.MAX_PRICE.value,
                          sizes=[defaults.DEFAULT_SIZE.value],
                          sort=defaults.DEFAULT_SORT.value,
                          search=''):

    with sqlalchemy.orm.Session(_engine) as session:
        stmt = sqlalchemy.select(Listing, User.username, Image)
        stmt = stmt.where(Listing.user_id == User.id)
        stmt = stmt.where(Listing.id == Image.listing_id)
        if category != defaults.DEFAULT_CATEGORY.value:
            stmt = stmt.where(Listing.category == category)
        if defaults.DEFAULT_SUBCATEGORY.value not in subcategory:
            stmt = stmt.where(Listing.subcategory.in_(subcategory))
        if defaults.DEFAULT_SIZE.value not in sizes:
            stmt = stmt.where(Listing.size.in_(sizes))
        stmt = stmt.where(Listing.price.between(price_min, price_max))
        if search != '':
            search = '%' + search + '%'
            stmt = stmt.where(
                sqlalchemy.func.lower(Listing.name).like(sqlalchemy.func.lower(search)))
        stmt = handle_sorting(stmt, sort).limit(300)
        table = session.execute(stmt).all()
        listings = create_listing_objects(table)
    return listings

# -----------------------------------------------------------------------
# This function gets all of the listings and all the info for each
# listing and returns a list of all of the listing object
def get_all_listings():  # later will add filters
    listings = []

    with sqlalchemy.orm.Session(_engine) as session:
        table = session.scalars(
            sqlalchemy.select(Listing).order_by(Listing.id.desc())).all()
        for row in table:
            images = get_listing_images(session, row.id)

            listing = listingmod.Listing(row.id, row.user_id, row.name,
                                         row.price, row.category, row.size, row.subcategory,
                                         row.description, row.status, row.pickup_location,
                                         images, row.likes)
            listings.append(listing)

    return listings

# -----------------------------------------------------------------------
def get_all_user_listings(userid):
    with sqlalchemy.orm.Session(_engine) as session:
        stmt = sqlalchemy.select(Listing, User.username, Image)
        stmt = stmt.where(User.id == userid)
        stmt = stmt.where(User.id == Listing.user_id)
        stmt = stmt.where(Image.listing_id == Listing.id)
        stmt = stmt.order_by(Listing.id.desc())
        table = session.execute(stmt).all()

        listings = create_listing_objects(table)
    return listings



# -----------------------------------------------------------------------
def get_listing(session, listing_id):

    listing_row = session.scalars(
        sqlalchemy.select(Listing).where(Listing.id == listing_id)).one_or_none()

    images = get_listing_images(session, listing_id)

    listing = listingmod.Listing(listing_row.id, listing_row.user_id, listing_row.name,
        listing_row.price, listing_row.category, listing_row.size, listing_row.subcategory,
        listing_row.description, listing_row.status, listing_row.pickup_location,
        images, likes=listing_row.likes)

    return listing

# -----------------------------------------------------------------------

def get_listing(listing_id):

    with sqlalchemy.orm.Session(_engine) as session:
        listing_row = session.scalars(
            sqlalchemy.select(Listing).where(Listing.id == listing_id)).one_or_none()

        if listing_row is None:
            raise Exception(
                "Couldn't find a listing with id %s." % str(listing_id))

        images = get_listing_images(session, listing_id)

        listing = listingmod.Listing(listing_row.id, listing_row.user_id, listing_row.name,
                                     listing_row.price, listing_row.category, listing_row.size, listing_row.subcategory,
                                     listing_row.description, listing_row.status, listing_row.pickup_location,
                                     images, likes=listing_row.likes)

    return listing

# -----------------------------------------------------------------------
# given the listing_id returns a list of all of the images associated
# with this listing_id. primary image will be first in the list.


def get_listing_images(session, listing_id):
    images = []

    table = session.scalars(
        sqlalchemy.select(Image)
        .where(Image.listing_id == listing_id)
        .order_by(Image.is_primary.desc(), Image.id)).all()

    for row in table:
        image = imagemod.Image(
            row.id, row.listing_id,
            row.is_primary, row.img_url, row.cloudinary_id)
        images.append(image)

    if len(images) == 0:
        raise Exception(
            "No images, missing primary image for listing id "
            + str(listing_id))

    if not images[0].get_is_primary():
        raise Exception("Primary image missing for listing id: "
                        + str(listing_id))
    return images

# -----------------------------------------------------------------------


def test_get_listings():
    listings = get_all_listings()
    for post in listings:
        print(post.to_tuple())
        print()


def test_get_filtered_listings(category=defaults.DEFAULT_CATEGORY.value,
                               subcategory=defaults.DEFAULT_SUBCATEGORY.value,
                               sizes=[defaults.DEFAULT_SIZE.value],
                               price_min=defaults.MIN_PRICE.value,
                               price_max=defaults.MAX_PRICE.value):
    men_shirts_listings = get_filtered_listings(category=category,
                                                subcategory=subcategory, sizes=sizes,
                                                price_min=price_min,
                                                price_max=price_max)
    for listing in men_shirts_listings:
        print(listing.to_tuple())

def _test_get_listing():
    print("Calling get_listing(1):")
    listing = get_listing(1)
    print('listing:', listing.to_tuple())
    print('image:', listing.get_images()[0].to_tuple())

def _test():
    # test_get_listings()
    print('Here are all of the "MEN SHIRTS"')
    test_get_filtered_listings(categories.CATEGORY_MENSWEAR.value, subcategories.SUBCATEGORY_SHIRT.value)
    print('Here are all of the WOMEN ITEMS')
    test_get_filtered_listings(categories.CATEGORY_WOMENSWEAR.value)
    print('Here are all of the MEN SHIRT SIZE M')
    test_get_filtered_listings(categories.CATEGORY_MENSWEAR.value, subcategories.SUBCATEGORY_SHIRT.value, [regular_sizes.SIZE_M.value])
    print('Here are all of the MEN PANTS SIZE S and XXL and XL')
    test_get_filtered_listings(categories.CATEGORY_MENSWEAR.value, subcategories.SUBCATEGORY_PANTS.value, [
                               regular_sizes.SIZE_S.value, regular_sizes.SIZE_XXL.value, regular_sizes.SIZE_XL.value])
    print('Here are all of the MEN PANTS SIZE S')
    test_get_filtered_listings(categories.CATEGORY_MENSWEAR.value, subcategories.SUBCATEGORY_PANTS.value, [regular_sizes.SIZE_S.value])
    print('Here are all of prices: min = 50, max = 400')
    test_get_filtered_listings(price_min=50, price_max=400)
    print("DEFAULT SEARCH")
    test_get_filtered_listings()


if __name__ == '__main__':
    _test()
