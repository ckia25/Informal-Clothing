#!/usr/bin/env python

# -----------------------------------------------------------------------
# informal.py
# -----------------------------------------------------------------------
import json
import sys
from urllib import request
import flask
from flask import redirect
import flask_wtf
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
from config import config_cloudinary
import services.edituser as edituser
import services.listingservice as listingservice
import services.listingformservice as listingformservice
import services.borrow_lend_service as borrow_lend_service
import services.rateuserservice as rateuserservice
import services.mylistings as mylistings
import services.mynotifications as mynotifications
import services.mylikes as mylikes
import services.rentalrequestservice as rentalrequestservice
import services.editnotification as notificationservice
import services.getpointsservice as getpointsservice
import services.editlike as likeservice
import services.editlisting as editlisting
import constants
from constants import *
import auth
from datetime import datetime
from services.mylikes import get_liked_posts

config_cloudinary()

# -----------------------------------------------------------------------
app = flask.Flask(__name__)
app.secret_key = "should_be_environ_key"
flask_wtf.csrf.CSRFProtect(app)
# -----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
# -----------------------------------------------------------------------


@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()


@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return auth.logoutcas()

# Checks if user with given username exists in DB,
# and creates new user if not. Returns user object.


def check_user_exists(username):
    user_exists = edituser.get_user(username)
    if not user_exists:
        user_exists = edituser.create_user(username=username,
                                           email=username+'@princeton.edu')
        getpointsservice.update_points(username, 500)
    return user_exists

# -----------------------------------------------------------------------


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    username = flask.session.get('username', False)
    html_code = flask.render_template('index.html',
                                      logged_in=username,
                                      username=username)
    response = flask.make_response(html_code)
    flask.session['modal'] = None
    flask.session['rate_user_ticket'] = None
    flask.session['update_status_ticket'] = None
    return response

# -----------------------------------------------------------------------

@app.route('/about', methods=['GET'])
def about():
    username = flask.session.get('username', False)
    html_code = flask.render_template('about.html',
                                      logged_in=username,
                                      username=username)
    response = flask.make_response(html_code)
    return response


@app.route('/faq', methods=['GET'])
def faq():
    username = auth.authenticate()
    user = check_user_exists(username)
    # username = flask.session.get('username', False)
    html_code = flask.render_template('FAQ.html',
                                      logged_in=username,
                                      username=username)
    response = flask.make_response(html_code)
    return response

# -----------------------------------------------------------------------


@app.route('/listings', methods=['GET'])
def listings():
    username = auth.authenticate()
    user = check_user_exists(username)

    modal = flask.session.get('modal', False)

    html_code = flask.render_template('listings.html', modal=modal,
                                      user=user, enumerate=enumerate,
                                      constants=constants, default_category=defaults.DEFAULT_CATEGORY.value,
                                      default_min_price=defaults.MIN_PRICE.value,
                                      default_max_price=defaults.MAX_PRICE.value,
                                      username=username)
    response = flask.make_response(html_code)
    flask.session['modal'] = None
    return response


@app.route('/listings/results', methods=['GET'])
def listings_results():
    username = auth.authenticate()
    user = check_user_exists(username)

    category, subcategory, sizes, minprice, maxprice, sort, search = listingservice.get_filter_args(
        args=flask.request.args)

    listings = listingservice.get_filtered_listings(category=category,
                                                    subcategory=subcategory,
                                                    sizes=sizes,
                                                    price_min=minprice,
                                                    price_max=maxprice,
                                                    sort=sort,
                                                    search=search)
    liked_posts = get_liked_posts(user.get_id())
    html_code = flask.render_template('listing-cards.html',
                                      listings=listings,
                                      user=user, enumerate=enumerate,
                                      constants=constants,
                                      liked_posts=liked_posts,
                                      username=username)
    response = flask.make_response(html_code)
    return response

# ----------------------------------------------------------------------

@app.route('/likepost', methods=['POST'])
def likepost():
    username = auth.authenticate()
    user = check_user_exists(username)

    request = flask.request.form
    listingid, userid = request['listingid'], request['userid']

    likeservice.like_clicked(userid, listingid)

    return '', 204

# -----------------------------------------------------------------------


@app.route('/listingform', methods=['GET'])
def listingform():
    modal = flask.request.args.get('modal', False)
    username = auth.authenticate()
    user = check_user_exists(username)

    html_code = flask.render_template(
        'listing-form.html', logged_in=username, constants=constants, modal=modal,
                                      username=username)
    response = flask.make_response(html_code)
    flask.session['modal'] = None
    return response


@app.route('/listingform/submit', methods=['POST'])
def listingform_submit():
    username = auth.authenticate()
    user = check_user_exists(username)

    primary_img = flask.request.files['primaryImage']
    images = flask.request.files.getlist('additionalImages[]')
    if images[0].filename == '':
        images = []
    if len(images) > 5:
        images = images[:5]
    images.insert(0, primary_img)
    verified, modal = listingformservice.verify_input_listingform_submit(
        flask.request.form, images)
    if verified:
        date_created = flask.request.form['listingDateCreated']
        listing_id = listingformservice.create_new_listing(
            flask.request.form,
            images, user.get_id())
        for key in flask.request.form:
            if 'blackoutDate' in key and flask.request.form[key] != '':
                start_date, end_date = flask.request.form[key].split(' - ')
                rentalrequestservice.create_unavailable_date(listing_id, None, user.get_id(), start_date, end_date)
        modal = 'new_listing'  # temporary
        response = flask.make_response(redirect('/listings'))
        flask.session['modal'] = modal
    else:
        response = flask.make_response(redirect('/listingform?modal=' + modal))

    return response

# -----------------------------------------------------------------------


@app.route('/rentalrequest', methods=['GET'])
def rentalrequest():
    username = auth.authenticate()
    user = check_user_exists(username)

    listing_id = flask.request.args.get('listingid')
    modal = flask.session.get('modal', False)

    try:
        listing = listingservice.get_listing(listing_id)
        if user.get_id() == listing.get_user_id():
            raise Exception("You are not allowed to rent your own item")
        from_username, avg_rating, count = rentalrequestservice.get_lender_username_and_rating(
            listing.get_user_id())
        lender_ratings = rateuserservice.get_lender_rating_history(listing.get_user_id())
    except Exception as err:
        print(err, file=sys.stderr)
        listing = None
        raise Exception(err)

    html_code = flask.render_template('rental-request.html',
                                      modal = modal,
                                      listing=listing,
                                      logged_in=username,
                                      from_username=from_username,
                                      constants=constants,
                                      avg_rating=json.dumps(round(avg_rating)),
                                      count=json.dumps(count),
                                      listing_id=json.dumps(listing_id),
                                      user_id=listing.get_user_id(),
                                      username=username,
                                      lender_ratings=lender_ratings)
    response = flask.make_response(html_code)
    flask.session['modal'] = None
    return response


@app.route('/rentalrequest/getunavailabledates', methods=['GET'])
def rentalrequest_get_unavailabledates():
    username = auth.authenticate()
    user = check_user_exists(username)

    listing_id = flask.request.args.get('listingid', False)
    listing_id = int(listing_id.strip('"'))

    unavailable_dates = rentalrequestservice.get_unavailable_dates(listing_id)
    json_string = json.dumps([date for date in unavailable_dates])

    html_code = flask.render_template('datepicker.html',
                                      listing_id=listing_id,
                                      unavailable_dates=json_string,
                                      username=username)
    response = flask.make_response(html_code)
    return response


@app.route('/rentalrequest/submit', methods=['POST'])
def rentalrequest_submit():
    username = auth.authenticate()
    user = check_user_exists(username)

    request_form = flask.request.form
    listing_id = flask.request.args.get('listingid', None)
    from_user_id = int(flask.request.args.get('uid', None))

    start_date, end_date = request_form['daterange'].split(' - ')
    date_format = "%m/%d/%Y"
    a = datetime.strptime(start_date, date_format)
    b = datetime.strptime(end_date, date_format)
    delta = b - a
    num_days = delta.days + 1
    request_msg, date_created = request_form['request_msg'], request_form['rentRequestDate']
    if len(request_msg) > inputLimits.RENTAL_MSG_LIMIT.value:
        request_msg = request_msg[:inputLimits.RENTAL_MSG_LIMIT.value]

    # check to see that the user has sufficient balance
    user_balance = user.get_balance()
    listing_price = rentalrequestservice.get_listing_price(listing_id)
    cost_to_rent = listing_price * num_days

    if(user_balance < cost_to_rent):
        response = flask.make_response(redirect(flask.url_for('rentalrequest', listingid = listing_id)))
        flask.session['modal'] = "not_enough_money"
        return response
    else:
        transaction_id = rentalrequestservice.create_transaction(listing_id=listing_id,
                                                                from_user_id=from_user_id,
                                                                to_user_id=user.get_id(),
                                                                date_created=date_created,
                                                                request_msg=request_msg,
                                                                date_lent_out=start_date,
                                                                date_returned=end_date)
        rentalrequestservice.create_unavailable_date(
            listing_id, transaction_id, from_user_id, start_date, end_date)
        notificationservice.add_notification(notif_type=constants.NotificationTypes.BORROW_REQUEST.value,listing_id=listing_id, to_user_id=user.get_id(),
            from_user_id=from_user_id, date_created=date_created, transaction_id=transaction_id, msg=request_msg)
        getpointsservice.update_points(user.get_username(), -1 * cost_to_rent)
        response = flask.make_response(redirect('/listings'))
        flask.session['modal'] = "new_rental_request"
        return response

# -----------------------------------------------------------------------


@app.route('/borrowing', methods=['GET'])
def borrowing():
    username = auth.authenticate()
    user = check_user_exists(username)

    listings = borrow_lend_service.get_user_borrowing_listings(user.get_id())

    html_code = flask.render_template('currently-borrowing.html', enumerate=enumerate,
                                      listings=listings, logged_in=username, Status=Status,
                                      username=username)
    response = flask.make_response(html_code)
    flask.session['rate_user_ticket'] = True
    flask.session['update_status_ticket'] = True
    return response


@app.route('/borrowing/status', methods=['GET', 'POST'])
def borrowingstatus():
    username = auth.authenticate()
    user = check_user_exists(username)

    request = flask.request.form

    listing_id = flask.request.args.get('listingid', None)
    transaction_id = flask.request.args.get('tid', None)
    current_date = request['date']
    lender_user_id = request['lender_user_id']

    if listing_id:
        borrow_lend_service.update_status(
            transaction_id, listing_id, lender_user_id, current_date)

    response = flask.make_response(redirect('/borrowing'))
    return response

# -----------------------------------------------------------------------


@app.route('/lending', methods=['GET'])
def lending():
    username = auth.authenticate()
    user = check_user_exists(username)

    listings = borrow_lend_service.get_user_lending_listings(user.get_id())

    html_code = flask.render_template('currently-lending.html', enumerate=enumerate,
                                      listings=listings, logged_in=username, Status=Status,
                                      username=username)
    response = flask.make_response(html_code)
    flask.session['rate_user_ticket'] = True
    flask.session['update_status_ticket'] = True
    return response


@app.route('/lending/status', methods=['GET', 'POST'])
def lendingstatus():
    username = auth.authenticate()
    user = check_user_exists(username)

    try:
        if not flask.session['update_status_ticket']:
            raise Exception("You are not authorized to make this action.")

        request = flask.request.form

        listing_id = flask.request.args.get('listingid', None)
        transaction_id = flask.request.args.get('tid', None)
        current_date = request['date']

        if listing_id:
            borrow_lend_service.update_status(
                transaction_id, listing_id, user.get_id(), current_date)

        response = flask.make_response(redirect('/lending'))
        return response
    except Exception as err:
        print(err, file=sys.stderr)
        raise Exception(err)

@app.route('/lending/reject', methods=['POST'])
def reject_request():
    username = auth.authenticate()
    user = check_user_exists(username)

    try:
        if not flask.session['update_status_ticket']:
            raise Exception("You are not authorized to make this action.")

        listing_id = flask.request.args.get('listingid', None)
        transaction_id = flask.request.args.get('tid', None)

        if listing_id:
            borrow_lend_service.reject_rental_request(
                transaction_id, listing_id, user.get_id())
            rentalrequestservice.remove_availability(transaction_id)


        response = flask.make_response(redirect('/lending'))
        flask.session['rate_user_ticket'] = None
        return response

    except Exception as err:
        print(err, file=sys.stderr)
        raise Exception(err)


# -----------------------------------------------------------------------

# Borrower rating the lender
@app.route('/rateborrower', methods=['POST'])
def rate_borrower():
    username = auth.authenticate()
    user = check_user_exists(username)

    request = flask.request.form
    current_date = request['date']

    return rate_helper(user, False, current_date, username)

# Lender rating the borrower
@app.route('/ratelender', methods=['POST'])
def rate_lender():
    username = auth.authenticate()
    user = check_user_exists(username)

    request = flask.request.form
    current_date = request['date']

    return rate_helper(user, True, current_date, username)


def rate_helper(user, rating_borrower, current_date, username):
    try:
        if not flask.session['rate_user_ticket']:
            raise Exception("You are not authorized to access this page.")
    except Exception as err:
        print(err, file=sys.stderr)
        raise Exception(err)

    listing_id = flask.request.args.get('listingid', None)
    transaction_id = flask.request.args.get('tid', None)
    early_return = flask.request.args.get('early', False)

    lender_user_id = flask.request.form['lender_user_id']

    if listing_id:
        borrow_lend_service.update_status(
            transaction_id, listing_id, lender_user_id, current_date, early_return)

    if rating_borrower:
        rentalrequestservice.remove_availability(transaction_id)

    user_rated_username = flask.request.args.get('user')
    transaction_id = flask.request.args.get('tid')
    headshot = edituser.get_user(user_rated_username).get_headshot()
    html_code = flask.render_template('rate-user.html', logged_in=user,
                                      user=user_rated_username, rating_borrower=rating_borrower,
                                      username=username, headshot=headshot, constants=constants)
    response = flask.make_response(html_code)
    flask.session['user_rated_username'] = user_rated_username
    flask.session['transaction_id'] = transaction_id
    return response

# Borrower rating the lender


@app.route('/rateuser/borrowersubmit', methods=['POST'])
def rateuser_borrower_submit():
    username = auth.authenticate()
    user_rating = check_user_exists(username)

    return rateuser_submit_helper(user_rating, False)

# Lender rating the borrower


@app.route('/rateuser/lendersubmit', methods=['POST'])
def rateuser_lender_submit():
    username = auth.authenticate()
    user_rating = check_user_exists(username)

    return rateuser_submit_helper(user_rating, True)


def rateuser_submit_helper(user_rating, rated_is_borrower):
    request = flask.request.form
    user_rated_username = flask.session.get('user_rated_username')
    transaction_id = flask.session.get('transaction_id')

    user_rated_id = edituser.get_user(user_rated_username).get_id()
    rating, msg, date_rated = request['rating'], request['msg'], request['date_rated']
    if len(msg) > inputLimits.RATING_LIMIT.value:
        msg = msg[:inputLimits.RATING_LIMIT.value]
    rateuserservice.rate_user(rating, user_rated_id, user_rating.get_id(
    ), date_rated=date_rated, transaction_id=transaction_id, msg=msg, rated_is_borrower=rated_is_borrower)

    response = flask.make_response(redirect('/listings'))
    flask.session['transaction_id'] = None
    flask.session['user_rated_username'] = None
    flask.session['rate_user_ticket'] = None
    flask.session['update_status_ticket'] = None
    return response

# -----------------------------------------------------------------------


@app.route('/profile/<user_requested>')
def profile(user_requested):
    username = auth.authenticate()
    logged_in_user = check_user_exists(username)

    user = edituser.get_user(user_requested)

    if user is None:
        raise Exception("User '%s' does not exist." % user_requested)

    if username == user_requested:
        own_profile = True
    else:
        own_profile = False

    balance = user.get_balance()
    modal = flask.session.get('modal', False)
    _, lender_rating, lender_count = rentalrequestservice.get_lender_username_and_rating(
        user.get_id())
    _, borrower_rating, borrower_count = rentalrequestservice.get_borrower_username_and_rating(
        user.get_id())
    if user.get_first_name() is not None and user.get_last_name() is not None:
        fullname = str(user.get_first_name()) + ' ' + str(user.get_last_name())
    else:
        fullname = None
    borrower_ratings, lender_ratings = rateuserservice.get_all_rating_history(user.get_id())
    html_code = flask.render_template('profile.html', enumerate=enumerate,
                                        constants=constants, user_requested=user_requested,
                                        balance=balance, lender_rating=round(lender_rating),
                                        borrower_rating=round(borrower_rating), lender_count=lender_count,
                                        borrower_count=borrower_count, modal=modal, headshot=user.get_headshot(),
                                        fullname=fullname, own_profile=own_profile, username=username,
                                        borrower_ratings=borrower_ratings, lender_ratings=lender_ratings, bio=user.get_bio())
    response = flask.make_response(html_code)
    flask.session['modal'] = None
    return response


@app.route('/profile/<user_requested>/results', methods=['GET'])
def profile_query_results(user_requested):
    username = auth.authenticate()
    logged_in_user = check_user_exists(username)
    user = edituser.get_user(user_requested)

    queryBy = flask.request.args.get('query')

    # this has to match the name of the tab exactly
    if queryBy == "Bookmarked":
        listings = mylikes.get_my_likes(user.get_id())
    else:
        listings = listingservice.get_all_user_listings(user.get_id())

    liked_posts = get_liked_posts(logged_in_user.get_id())
    html_code = flask.render_template('profile-cards.html', enumerate=enumerate,
                                      constants=constants,
                                      listings=listings, logged_in_user=logged_in_user,
                                      username=username, userid=user.get_id(), user=user,
                                      liked_posts = liked_posts)
    response = flask.make_response(html_code)
    return response

# End point to handle points acquisition which happens on profile page


# @app.route('/profile/getpoints', methods=['POST'])
# def get_points():
#     username = auth.authenticate()
#     user = check_user_exists(username)
#     response = get_points_helper(user)
#     return response


# def get_points_helper(user):
#     username = user.get_username()
#     request = flask.request.form
#     points = request['points']
#     if points is None:
#         points = 0
#     elif points[0] == "-":
#         try:
#             points = -1 * int(points[1:])
#         except Exception:
#             points = 0
#     else:
#         try:
#             points = int(points)
#         except Exception:
#             points = 0

#     new_balance = getpointsservice.update_points(username, points)
#     html_string = str(new_balance)
#     response = flask.make_response(html_string)
#     return response


@app.route('/profile/<user_requested>/editlisting', methods=['GET'])
def edit_listing(user_requested):
    username = auth.authenticate()
    user = check_user_exists(user_requested)
    logged_in_user = check_user_exists(username)
    # modal = flask.session.get('modal', False)
    listing_id = flask.request.args.get('listingid', False)
    if listing_id:
        try:
            listing = listingservice.get_listing(listing_id)
            if logged_in_user.get_id() != listing.get_user_id():
                raise Exception(
                    "You cannot edit a listing that you do not own")
            current_stats = borrow_lend_service.get_current_stats_of_listing(
                listing_id)
            # MAY NEED TO CHANGE LATER IF THERE ARE MORE STATUSES WHICH WE WANT TO PREVENT EDITING
            if Status.REQUESTED.value in current_stats:
                raise Exception(
                    "You cannot edit a listing if it is in the process of being rented")

            if Status.REQUEST_ACCEPTED.value in current_stats:
                raise Exception(
                    "You cannot edit a listing if it is in the process of being rented")

            unavailable_dates = rentalrequestservice.get_unavailable_dates(listing_id)
            json_string = json.dumps([date for date in unavailable_dates])

        except Exception as ex:
            print(ex, file=sys.stderr)
            # ADD ERROR HANDLING LATER TO SHOW NICE MODAL
            raise Exception(str(ex))
    html_code = flask.render_template('edit-listing-form.html',
                                    logged_in=username,
                                    listing=listing,
                                    constants=constants,
                                    listing_id=listing_id,
                                    username=username,
                                    unavailable_dates=json_string)
    response = flask.make_response(html_code)
    # flask.session['modal'] = None
    return response


@app.route('/profile/<user_requested>/editlisting/submit', methods=['POST'])
def submit_edit_listing(user_requested):
    username = auth.authenticate()
    if username != user_requested:
        raise Exception("You cannot edit someone else's listing!")
    user = check_user_exists(user_requested)
    logged_in_user = check_user_exists(user_requested)
    # Verify form
    verified, modal = editlisting.verify_input_editlisting_submit(flask.request.form)
    if verified:
        # Try to edit the listing if verified
        try:
            listing_id = flask.request.form['listing_id']
            listing = listingservice.get_listing(listing_id)
            if logged_in_user.get_id() != listing.get_user_id():
                raise Exception(
                    "You cannot edit a listing that you do not own")
            date_created = flask.request.form['listingDateCreated']
            editlisting.edit_listing(listing_id,
                flask.request.form)

            for key in flask.request.form:
                if 'blackoutDate' in key:
                    start_date, end_date = flask.request.form[key].split(' - ')
                    rentalrequestservice.create_unavailable_date(listing_id, None, user.get_id(), start_date, end_date)
            response = flask.make_response(redirect('/profile/%s' % username))
            modal = Modals.EDIT_LISTING_SUCCESS.value  # temporary
        except Exception as ex:
            print(ex, file=sys.stderr)
            modal = Modals.EDIT_LISTING_FAILURE.value
            response = flask.make_response(redirect('/profile/%s' % username))
    else:
        response = flask.make_response(redirect('/profile/%s' % username))
    flask.session['modal'] = modal
    return response

@app.route('/profile/<user_requested>/edit', methods = ['GET'])
def edit_profile(user_requested):
    username = auth.authenticate()
    if username != user_requested:
        raise Exception("You cannot edit someone else's profile!")
    user = check_user_exists(user_requested)


    html_code = flask.render_template('edit-profile.html', constants=constants, user=user,
                                      username = user_requested)
    response = flask.make_response(html_code)
    flask.session['modal'] = None

    return response

@app.route('/profile/<user_requested>/edit/submit', methods = ['POST'])
def submit_edit_profile_form(user_requested):
    username = auth.authenticate()
    if username != user_requested:
        raise Exception("You cannot edit someone else's profile!")
    user = check_user_exists(user_requested)
# WRITE THE VERIFICATION FUNCTION
    verified, modal = edituser.verify_input_edit_profile(username, flask.request.form)

    if verified:
        # Try to edit the listing if verified
        try:
            headshot_file = flask.request.files['headshot']
            edituser.edit_user(username,
                flask.request.form, headshot_file)
            response = flask.make_response(redirect('/profile/%s' % user_requested))
            modal = Modals.EDIT_PROFILE_SUCCESS.value
        except Exception as ex:
            print(ex, file=sys.stderr)
            modal = Modals.EDIT_PROFILE_FAILURE.value
            response = flask.make_response(redirect('/profile/%s' % user_requested))
    else:
        response = flask.make_response(redirect('/profile/%s' % user_requested))
    flask.session['modal'] = modal
    return response



# -----------------------------------------------------------------------
@app.route('/notifications', methods=['GET'])
def display_notifications():
    username = auth.authenticate()
    user = check_user_exists(username)

    lender_notifications = mynotifications.get_lender_notifications(
        user.get_id())
    borrower_notifications = mynotifications.get_borrower_notifications(
        user.get_id())


    # If notification is recent, put secs/min since created
    def minutes_since_timestamp(timestamp_str, date_created):
        try:
            now = datetime.utcnow() - timedelta(hours=4)
            hours, minutes, secs = timestamp_str.split(':')
            # MANUAL TIMEZONE DIFF WITH UTC
            hours = int(hours)
            minutes = int(minutes.split(" ")[0])

            time_format = '%H:%M:%S'
            now_str = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
            now_str, now_time = now_str.strftime('%Y-%m-%d'), now_str.strftime(time_format)

            # if notif. created at 60 sec+ mark, change to avoid datetime bugs
            secs_in_timestamp = timestamp_str.split(":")[2]
            if int(secs_in_timestamp) >= 60:
                timestamp_str = timestamp_str[:6] + '59'

            created_obj = datetime.strptime(timestamp_str, time_format)  # convert to datetime object
            now_obj = datetime.strptime(now_time, time_format)  # convert to datetime object
            time_diff = (now_obj - created_obj).total_seconds()  # calculate difference in seconds

            if now_str == str(date_created):
                if time_diff <= 60*60:
                    if time_diff <= 60:
                        return '%d sec ago' % abs(time_diff)
                    minutes_ago = abs(time_diff / 60)
                    return '%d min ago' % minutes_ago
                hours_ago = abs(time_diff / 60 / 60)
                hour_str = '%d hour ago' if int(hours_ago) == 1 else '%d hours ago'
                return hour_str % hours_ago

            if hours >= 12:
                period = 'PM'
                if hours > 12:
                    hours -= 12
            else:
                period = 'AM'
                if hours == 0:
                    hours = 12

            if minutes < 10:
                minutes = '0' + str(minutes)
            return ' at %d:%s %s' % (hours, minutes, period)
        except Exception:
            return ""

    html_code = flask.render_template('notifications.html', logged_in=user,
                                      lender_notifications=lender_notifications,
                                      borrower_notifications=borrower_notifications,
                                      enumerate=enumerate, minutes_since_timestamp=minutes_since_timestamp,
                                      username=username)
    response = flask.make_response(html_code)
    return response
# -----------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    username = auth.authenticate()
    if 'username' in flask.session:
        logged_in = True
    else:
        logged_in = False
    html_code = flask.render_template('404.html',
                                      logged_in=logged_in,
                                      username=username), 404
    response = flask.make_response(html_code)
    return response

# @app.errorhandler(Exception)
# def handle_error(error):
#     username = auth.authenticate()
#     if 'username' in flask.session:
#         logged_in = True
#     else:
#         logged_in = False

#     html_code = flask.render_template('error.html',
#                                       logged_in=logged_in,
#                                       username=username,
#                                       error=error)
#     response = flask.make_response(html_code)
#     print(error, file=sys.stderr)
#     return response