# the whole dashboard handling
from flask import render_template, redirect
from datetime import datetime

from db_config import db
from db_config.db_tables import Matches, Offer, FlatMate, Matches, Preferences
from machine_learning.clustering import clustering_function

# the customer dashboard load function
def dashboard_1(user_id, selector=False, give_matchings=[]):
    print('dashboard_1')
    properties = []
    matches = {}

    # check if the user is already clustered
    if selector:
        try:
            clustering_function(user_id)
            matchings = Matches.query.filter_by(user_id=user_id).all()
        except Exception as e:
            raise e
            print(f"An error occurred while clustering: {str(e)}")

    # check whether there are any matches provided by the filtering function
    if give_matchings:
        matchings = [
            Matches.query.filter_by(id=match['match_id']).first()
            for match in give_matchings
        ]

    # add the number of total matches
    matches['total'] = len(matchings)
    # initialize the other match counters
    matches['accepted'] = 0
    matches['pending'] = 0
    matches['rejected'] = 0

    for match in matchings:
        # empty values
        matching_status = ''
        contact = ''

        # check if the match is already successful
        match_status = match.successful_match
        if match_status == 1:
            matching_status = 'Pending'
            matches['pending'] += 1
        elif match_status == 2:
            matching_status = 'Successful'
            matches['accepted'] += 1
            contact = FlatMate.query.filter_by(id=Offer.query.filter_by(id=match.offer_id).first().user_id).first().email
        elif match_status == 3:
            matching_status = 'Rejected'
            matches['rejected'] += 1

        property_info = Offer.query.filter_by(id=match.offer_id).first()
        properties.append({
            'id': property_info.id,
            'name': property_info.title,
            'description': property_info.description,
            'address': property_info.address,
            'provider': FlatMate.query.filter_by(id=property_info.user_id).first().first_name,
            'flat_size': property_info.apartment_size,
            'room_size': property_info.room_size,
            'price': property_info.price,
            'distance': property_info.distance,
            'bathrooms': property_info.bathrooms,
            'match_score': round(match.score, 2),
            'matching_status': matching_status,
            'contact': contact
        })

    return render_template('/customer_dashboard.html', properties=properties, matches=matches)

# the provider dashboard load function
def dashboard_2(user_id):
    user = []

    # get the offers of this provider
    all_offers = Offer.query.filter_by(user_id=user_id).first()

    # iterate over the offers
    for offer in all_offers:
        # define empty
        user = []

        matches = Matches.query.filter(Matches.offer_id == offer.id, Matches.successful_match.in_([1, 2])).all()

        # iterate over (potential) matches
        for m in matches:
            matched_user = FlatMate.query.filter_by(id=m.user_id).first()
            if matched_user:
                # append information about the match
                preferences = Preferences.query.filter_by(user_id=matched_user.id).first()
                # check the community
                social_level = ''
                if preferences.community == 1:
                    social_level = 'I like keeping to myself most of the time.'
                elif preferences.community == 2:
                    social_level = 'A mix of hanging out and doing our own thing sounds great.'
                elif preferences.community == 3:
                    social_level = 'I like to socialize often.'

                user.append({
                    'user_id': matched_user.id,
                    'name': matched_user.first_name,
                    'email': matched_user.email,
                    'gender': 'male' if preferences.sex else 'female',
                    'age': preferences.age,
                    'language': preferences.language,
                    'community': social_level,
                    'degree': 'Master' if preferences.degree else 'Bachelor',
                    'semester': preferences.semester,
                    'smoking': 'Yes' if preferences.smoking else 'No',
                    'pets': 'Yes' if preferences.pets else 'No',
                })

    return render_template('/provider_dashboard.html', user=user)

# the filtering function
def filtering_1(user_id, request):
    matchings = []

    # Get filter criteria from request
    min_sq_meters = request.form.get("min_sq_meters", type=int)
    max_distance_to_uni = request.form.get("max_distance_to_uni", type=int)
    max_price = request.form.get("max_price", type=int)

    # Filter matches and offers by criteria from request
    matches = Matches.query.all()
    offers = Offer.query.filter(
        Offer.apartment_size >= min_sq_meters,
        Offer.distance <= max_distance_to_uni,
        Offer.price <= max_price
    ).all()

    # Filter matches based on the filtered offers
    filtered_matches = [match for match in matches if match.offer_id in [offer.id for offer in offers]]

    # Create matchings list with the filtered results
    matchings = [
        {
            'match_id': match.id,
        }
        for match in filtered_matches
    ]

    # Sort matchings by matching_score in descending order
    matchings = sorted(matchings, key=lambda x: x['matching_score'], reverse=True)

    return dashboard_1(user_id=user_id, give_matchings=matchings)

# the matching function
def matches_1(user_id, request):
    # get offer_id of matched offer
    offer_id = request.form.get("offer_id")
    if offer_id:
        # update the successful match
        match = Matches.query.filter_by(user_id=user_id, offer_id=offer_id).first()
        # set the match status to pending
        match.successful_match = 1
        db.session.commit()

    return dashboard_1(user_id)

# provider accepts the match
def accept_1(user_id, request):
    # get offer_id of matched offer
    matched_user_id = request.form.get("user_id")
    if matched_user_id:
        # get the offer_id
        offer_id = Offer.query.filter_by(user_id=user_id).first().id
        # update the successful match
        match = Matches.query.filter_by(user_id=user_id, offer_id=offer_id).first()
        # set the match status to successful
        match.successful_match = 2
        db.session.commit()

    return redirect('/provider_dashboard')

# provider rejects the match
def reject_1(user_id, request):
    # get offer_id of matched offer
    matched_user_id = request.form.get("user_id")
    if matched_user_id:
        # get the offer_id
        offer_id = Offer.query.filter_by(user_id=user_id).first().id
        # update the successful match
        match = Matches.query.filter_by(user_id=user_id, offer_id=offer_id).first()
        # set the match status to successful
        match.successful_match = 3
        db.session.commit()

    return redirect('/provider_dashboard')