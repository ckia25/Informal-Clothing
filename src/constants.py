#!/usr/bin/env python

#-----------------------------------------------------------------------
# constants.py
# All constants we need
# Functions to get those constants
#-----------------------------------------------------------------------
import random
from enum import Enum
from sre_constants import CATEGORY


# Regular Sizes


def get_men_pant_waiste_sizes():
    return [26, 27, 28, 29, 30, 31, 32, 33, 34,
            35, 36, 38, 40, 42, 44, 46, 48, 50]

def get_men_pant_length_sizes():
    return [26, 28, 30, 32, 34, 36, 38]

def get_women_pant_waiste_sizes():
    return [23, 24, 25, 26, 27, 28, 29, 30, 31,
            32, 33, 34, 36, 38, 40, 42, 44, 46, 48, 50]

def get_woman_pant_length_sizes():
    return [26, 28, 30, 32, 34]

def get_men_shorts_sizes():
    return get_men_pant_waiste_sizes()

def get_women_shorts_sizes():
    return get_women_pant_waiste_sizes()

def get_men_shoe_sizes():
    return []

def get_women_shoe_sizes():
    return []

# CATEGORIES
class categories(Enum):
    CATEGORY_MENSWEAR = 'menswear'
    CATEGORY_WOMENSWEAR = 'womenswear'
    CATEGORY_ACCESSORIES = 'accessories'
    CATEGORY_OTHER = 'other'


# SUBCATEGORIES
class subcategories(Enum):
    SUBCATEGORY_ALL_CLOTHING = 'all clothing'
    SUBCATEGORY_TOPS = 'tops'
    SUBCATEGORY_DRESSES = 'dresses'
    SUBCATEGORY_BOTTOMS = 'bottoms'
    SUBCATEGORY_SHIRT = 'shirt'
    SUBCATEGORY_PANTS = 'pants'
    SUBCATEGORY_SHORTS = 'shorts'
    SUBCATEGORY_SHOES = 'shoes'
    SUBCATEGORY_SWEATER = 'sweater'
    SUBCATEGORY_SWEATSHIRT = 'sweatshirt'
    SUBCATEGORY_JACKET = 'jacket'
    SUBCATEGORY_OTHER = 'other'

# REGULAR SIZES
class regular_sizes(Enum):
    SIZE_XS = 'XS'
    SIZE_S = 'S'
    SIZE_M = 'M'
    SIZE_L = 'L'
    SIZE_XL = 'XL'
    SIZE_XXL = 'XXL'
    SIZE_OTHER = 'Other'
    SIZE_NA = 'N/A'
    SIZE_ALL = 'All Sizes'

#SORTINGS
class sortings(Enum):
    MOST_RECENT = 'Most Recent'
    OLDEST = 'Oldest'
    SORT_A_Z = 'A to Z'
    SORT_PRICE_LOW_HIGH = 'Price low to high'
    SORT_PRICE_HIGH_LOW = 'Price high to low'

#DEFAULTS
class defaults(Enum):
    DEFAULT_CATEGORY = 'all categories'
    DEFAULT_SUBCATEGORY = subcategories.SUBCATEGORY_ALL_CLOTHING.value
    MAX_PRICE = 100000
    MIN_PRICE = 0
    DEFAULT_SIZE = regular_sizes.SIZE_ALL.value
    DEFAULT_SORT = sortings.MOST_RECENT.value

#STATUS OPTIONS
class Status(Enum):
    REQUESTED = "Awaiting approval"
    REQUEST_ACCEPTED = "Ready to exchange"
    BORROWER_HAS_POSSESSION = "In borrower's hands"
    RETURNED = "Returned"
    OVERDUE = "Overdue"
    NEVER_RETURNED = "Never returned"
    ON_THE_MARKET = "On the market"
    EARLY_RETURN = "Early return"

class ImageSizes(Enum):
    HEIGHT = 600
    WIDTH = 600

class NotificationTypes(Enum):
    BORROW_REQUEST = 'Borrow request'
    LIKE_NOTIFICATION = 'Someone liked your post'
    BORROW_REQUEST_ACCEPTED = 'Borrow request approved'
    BORROWER_RECEIVED_ITEM = 'Borrower received item'
    BORROWER_RETURNED_ITEM = 'Borrower returned item'
    BACK_ON_MARKET = 'Item back on market'
    USER_RATING = 'User has been rated'

class inputLimits(Enum):
    DESCRIPTION_LIMIT = 300
    TITLE_LIMIT = 20
    NAME_LIMIT = 15
    BIO_LIMIT = 300
    RATING_LIMIT = 100
    RENTAL_MSG_LIMIT = 50
    

# ERROR MODAL NAMES
class ErrorModals(Enum):
    INVALID_INPUT_LISTINGFORM = 'invalid_input_in_the_listing_form'
    INVALID_LISTINGFORM_MESSAGE = 'Listing was unable to be created! Please make sure you put the correct values in each field'

class Modals(Enum):
    EDIT_LISTING_SUCCESS = 'edit_listing_success'
    EDIT_LISTING_FAILURE = 'edit_listing_failure'
    INVALID_EDIT_MESSAGE = 'Listing was unable to be edited! Please make sure you put the correct values in each field'
    SUCCESS_EDIT_MESSAGE = 'Listing was edited successfully'
    EDIT_PROFILE_SUCCESS = 'edit_profile_success'
    EDIT_PROFILE_FAILURE = 'edit_profile_failure'
    EDIT_PROFILE_SUCCESS_MESSAGE = 'Profile was edited successfully!'
    EDIT_PROFILE_FAILURE_MESSAGE = 'Profile was unable to be edited! Please make sure you put the correct values in each field'


class ProfileTabs(Enum):
    MY_LISTINGS = 'My Listings'
    LENDING = 'Lending'
    BORROWING = 'Borrowing'
    LIKED = 'Bookmarked'

#TEST_IMAGES_URLS
def get_test_image_urls():
    return [
        (categories.CATEGORY_MENSWEAR.value, subcategories.SUBCATEGORY_SHIRT.value, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJTJGTHPV8zKF-jU55m-IoLAZwW5_XbnsA4xWcG-md__I1DGe6sQLkLZrpb1f4KrlclOQ&usqp=CAU'),
        (categories.CATEGORY_MENSWEAR.value, subcategories.SUBCATEGORY_SHIRT.value, 'https://media.istockphoto.com/id/186846165/photo/portrait-of-a-man-with-his-finger-pointing-up.jpg?s=612x612&w=0&k=20&c=UD36mzdDnTbr8avUm2_0EB2J1PBprxRg7MqNoTM9KrU='),
        (categories.CATEGORY_MENSWEAR.value, subcategories.SUBCATEGORY_PANTS.value, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQl1I1MA-7dpnEBjASb48J0VQAI2jde4way4g&usqp=CAU'),
        (categories.CATEGORY_WOMENSWEAR.value, subcategories.SUBCATEGORY_SWEATSHIRT.value, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnUCNXvX8XuD0knDv9pZcpdvC4PETKYxJIHg&usqp=CAU')
        ]

def get_random_size():
    sizes = [e.value for e in regular_sizes]
    i = random.randint(0, len(sizes)-1)
    return sizes[i]
