#!/usr/bin/env python

#-----------------------------------------------------------------------
# image.py
#-----------------------------------------------------------------------

class Image:
    def __init__(self, id, listing_id, is_primary, img_url, cloudinary_id):
        self.id = id
        self.listing_id = listing_id
        self.is_primary = is_primary
        self.img_url = img_url
        self.cloudinary_id = cloudinary_id

    def get_id(self):
        return self.id

    def get_listing_id(self):
        return self.listing_id

    def get_is_primary(self):
        return self.is_primary

    def get_img_url(self):
        return self.img_url

    def get_cloudinary_id(self):
        return self.cloudinary_id

    def to_tuple(self):
        return (self.id, self.listing_id, self.is_primary, self.img_url, self.cloudinary_id)
