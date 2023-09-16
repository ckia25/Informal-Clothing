#!/usr/bin/env python

# -----------------------------------------------------------------------
# listingformservice.py
# handles route('/listingform')
# endpoint
# -----------------------------------------------------------------------

from cloudinary import CloudinaryImage
import cloudinary.uploader
from email.policy import default
import services.database as database
import services.editimage as editimage
from services.database import _engine
import sys

import sqlalchemy.ext.declarative
import sqlalchemy
from constants import ImageSizes
from constants import ErrorModals
from constants import defaults
from constants import inputLimits

from config import config_cloudinary
config_cloudinary()

# -----------------------------------------------------------------------

# Constants
STATUS_AVAILABLE = 'Available'

# -----------------------------------------------------------------------


def verify_input_listingform_submit(form, images):
    primary_image = images[0]
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
        if primary_image == None:
            raise Exception("primary image invalid")
        if len(images) > 6:
            raise Exception("Too many additional images")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return False, ErrorModals.INVALID_INPUT_LISTINGFORM.value

    return True, 'new_listing'

# -----------------------------------------------------------------------


def create_cloudinary_id(listing_id, image_index):
    return str(listing_id) + '_' + str(image_index)


# Whenever we reset the informal.sql database lets incremenet test_number
def create_cloudinary_test_id(listing_id, image_index, test_number):
    return str(listing_id) + '_TEST' + str(test_number) + '_' + str(image_index)

# -----------------------------------------------------------------------
def restrict_listing_title(name):
    if len(name) > inputLimits.TITLE_LIMIT.value:
        return name[:inputLimits.TITLE_LIMIT.value]
    return name


def restrict_listing_description(description):
    if len(description) > inputLimits.DESCRIPTION_LIMIT.value:
        return description[:inputLimits.DESCRIPTION_LIMIT.value]
    return description
# -----------------------------------------------------------------------
def create_new_listing(request_form, images, user_id):

    with sqlalchemy.orm.Session(_engine) as session:

        # could be replaced by a create listing call.
        new_listing = database.Listing(user_id=user_id,
                                       name=restrict_listing_title(request_form['name']),
                                       price=int(request_form['price']),
                                       category=request_form['category'],
                                       size=request_form['size'],
                                       subcategory=request_form.get(
                                           'subcategory'),
                                       description=restrict_listing_description(request_form.get('description', '')),
                                       status=STATUS_AVAILABLE,
                                       pickup_location=None,
                                       likes=0)
        session.add(new_listing)
        session.commit()
        session.flush()
        session.refresh(new_listing)

    # add the primary key into the database and cloudinary

    is_primary = True
    for i in range(0, len(images)):
        file = images[i]
        image_cloud_id = create_cloudinary_id(new_listing.id, i)
        response = cloudinary.uploader.upload(file,
                                              transformation=[
                                                  {'width': ImageSizes.WIDTH.value,
                                                   'height': ImageSizes.HEIGHT.value,
                                                   'crop': 'fill'},
                                              ])
        img_url = response['secure_url']
        editimage.create_image(listing_id=new_listing.id, is_primary=is_primary,
                               img_url=img_url, cloudinary_id=image_cloud_id)
        if is_primary:
            is_primary = False

    return new_listing.id

# ----------------------------------------------------------------------


def _test():
    print()


if __name__ == '__main__':
    _test()
