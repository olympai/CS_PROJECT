# the whole dashboard handling
from flask import render_template
from datetime import datetime

from db_config import db
from db_config.db_tables import Matches, Offer, User
from machine_learning.clustering import clustering_function

# the customer dashboard load function
def dashboard_1(user_id):
    matchings = clustering_function(user_id)
    return render_template('/customer_dashboard.html', matchings=matchings)

# the provider dashboard load function
def dashboard_2(user_id):
    offers = []

    # get the offers of this provider
    all_offers = Offer.query.filter_by(user_id=user_id).all()

    # iterate over the users
    for offer in all_offers:
        match = []
        matches = Matches.query.filter_by(offer_id=offer.id, successful_match=True).all()

        # iterate over (potential) matches
        for m in matches:
            # append information about the match
            match.append({
                'user_id': m.user_id,
                'email': User.query.filter_by(id=m.user_id).first().email
            })

        # gather information about the offers
        offers.append({
            'offer_id': offer.id,
            'title': offer.title,
            'description': offer.description,
            'address': offer.address,
            'time_live': datetime.strftime(offer.time_live),
            'match': match
        })

    return render_template('/provider_dashboard.html', offers=offers)

# the filtering function
def filtering_1(user_id, request):
    matchings = []

    matches = Matches.query.all() # filter matches by criteria from request
    offers = Offer.query.all() # filter offer by criteria from request

    # MY CODE
    # ...

    # return the matchings, e.g. with the following structure
    matchings = [
        # best matchings in descending order
        # best matching
        {
            'offer_id': '...', # the corresponding offer_id
            'matching_score': matches.score # the score on which basis we should rank the matchings
        },
        # second best matching
        {
            'offer_id': '...', # the corresponding offer_id
            'matching_score': matches.score # the score on which basis we should rank the matchings
        }
        # n-th best matching
        # ...
    ]

    return render_template('/customer_dashboard.html', matchings=matchings)

# the matching function
def matches_1(user_id, request):
    matchings = []
    matched_contact = ''

    # get offer_id of matched offer
    offer_id = request.form.get("offer_id")
    if offer_id:
        # get the matched contact
        matched_user_id = Offer.query.filter_by(id=offer_id).first().user_id
        matched_contact = User.query.filter_by(id=matched_user_id).first().email

        # update the successful match
        match = Matches.query.filter_by(user_id=user_id, offer_id=offer_id).first()
        match.successful_match = True
        db.session.commit()

    return render_template('/dashboard.html', matchings=matchings, matched_contact=matched_contact)
