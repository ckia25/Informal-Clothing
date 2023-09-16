#!/usr/bin/env python

# -----------------------------------------------------------------------
# listing.py
# -----------------------------------------------------------------------

class Listing:
    def __init__(self, id, user_id, name, price, category, size, subcategory, description, status, pickup_location, images, transaction=None, availability=None, likes=0, poster=None, avg_lender_rating=None, rating_count=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.price = price
        self.category = category
        self.size = size
        self.subcategory = subcategory
        self.description = description
        self.status = status
        self.pickup_location = pickup_location
        self.images = images
        self.transaction = transaction
        self.availability = availability
        self.likes = likes
        self.poster = poster
        self.avg_lender_rating = avg_lender_rating
        self.rating_count = rating_count

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_category(self):
        return self.category

    def get_size(self):
        return self.size

    def get_subcategory(self):
        return self.subcategory

    def get_description(self):
        return self.description

    def get_status(self):
        return self.status

    def get_pickup_location(self):
        return self.pickup_location

    def get_images(self):
        return self.images

    def get_transaction(self):
        return self.transaction

    def get_availability(self):
        return self.availability

    def get_likes(self):
        return self.likes

    def get_poster(self):
        return self.poster

    def get_avg_lender_rating(self):
        return self.avg_lender_rating

    def get_rating_count(self):
        return self.rating_count

    def to_tuple(self):
        return (self.id,
                self.user_id,
                self.name,
                self.price,
                self.category,
                self.size,
                self.subcategory,
                self.description,
                self.status,
                self.pickup_location,
                self.images,
                self.transaction,
                self.likes,
                self.avg_lender_rating,
                self.rating_count)
