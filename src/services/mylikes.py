#!/usr/bin/env python

# -----------------------------------------------------------------------
# mylikes.py
# handles route("/likes") endpoint
# -----------------------------------------------------------------------

import sqlalchemy.ext.declarative
import sqlalchemy

from services.database import Like
from services.database import Listing
from services.database import Image
from services.database import User
from services.database import _engine
import services.listingservice as listingservice

import classes.listing as listingmod
from services.listingservice import create_image_object

#-----------------------------------------------------------------------
# This function gets all of the posts that the user has likes

def get_my_likes(user_id):

    with sqlalchemy.orm.Session(_engine) as session:
        
        stmt = sqlalchemy.select(Listing, User.username, Image)
        stmt = stmt.where(Like.user_id == user_id)
        stmt = stmt.where(Listing.user_id == User.id)
        stmt = stmt.where(Like.listing_id == Listing.id)
        stmt = stmt.where(Image.listing_id == Listing.id)
        stmt = stmt.order_by(Listing.id.desc())
        stmt = stmt.distinct()
        results = session.execute(stmt).all()
        liked_posts = listingservice.create_listing_objects(results)
        return liked_posts
    

def get_liked_posts(user_id):
        liked_posts = []

        with sqlalchemy.orm.Session(_engine) as session:
            
            stmt = sqlalchemy.select(Like.listing_id)
            stmt = stmt.where(Like.user_id == user_id)
            results = session.execute(stmt).all()

            for lid in results:
                liked_posts.append(lid[0])

            return liked_posts
            
        