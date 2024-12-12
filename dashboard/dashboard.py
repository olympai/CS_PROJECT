from flask import render_template, redirect
from datetime import datetime

from db_config import db
from db_config.db_tables import Matches, Offer, FlatMate, Preferences
from celery_setup.celery_config import async_clustering_function

# The customer dashboard load function
def dashboard_1(user_id, selector: int, give_matchings=[]):
    print('dashboard_1')  # Debugging information
    print('user_id:', user_id)
    
    # Initialize data structures
    properties = []  # Stores property details for the dashboard
    matches = {}  # Tracks match statistics (total, accepted, pending, rejected)
    matchings = []  # Stores matching data

    # Determine action based on the selector value
    if selector == 1:  # Case 1: Perform clustering for the user
        try:
            job = async_clustering_function.apply_async(queue='alpha', args=(user_id,))
            return render_template('progress.html', JOBID=job.id)
        except Exception as e:
            print(f"An error occurred while clustering: {str(e)}")  # Log clustering errors

    elif selector == 2:  # Case 2: Fetch all existing matches for the user
        matchings = Matches.query.filter_by(user_id=user_id).all()

    elif selector == 3:  # Case 3: Use pre-filtered matches provided
        matchings = [
            Matches.query.filter_by(id=match['match_id']).first()
            for match in give_matchings
        ]

    # Initialize match statistics
    matches['total'] = len(matchings)-1 # -1 because 0 indexed (for frontend)
    matches['accepted'] = 0
    matches['pending'] = 0
    matches['rejected'] = 0

    # Process each match
    for i, match in enumerate(matchings, start=1):
        matching_status = ''  # Default matching status
        contact = ''  # Default contact info

        # Determine match status and update counters
        if match.successful_match == 1:  # Pending match
            matching_status = 'Pending'
            matches['pending'] += 1
        elif match.successful_match == 2:  # Accepted match
            matching_status = 'Successful'
            matches['accepted'] += 1
            contact = FlatMate.query.filter_by(id=Offer.query.filter_by(id=match.offer_id).first().user_id).first().email
        elif match.successful_match == 3:  # Rejected match
            matching_status = 'Rejected'
            matches['rejected'] += 1

        # Retrieve property details associated with the match
        property_info = Offer.query.filter_by(id=match.offer_id).first()
        
        # Append formatted property information to the list
        properties.append({
            'id': property_info.id,
            'name': property_info.title,
            'description': property_info.description,
            'address': property_info.address,
            'provider': FlatMate.query.filter_by(id=property_info.user_id).first().first_name,
            'flat_size': property_info.room_size,
            'room_size': property_info.apartment_size,
            'price': property_info.price,
            'distance': property_info.distance,
            'bathrooms': property_info.bathrooms,
            'match_score': round(match.score, 2),
            'matching_status': matching_status,
            'contact': contact,
            'i': i,  # Serial number
        })

        # Sort the properties:
        # - First by whether `matching_status` is 'Pending', 'Successful', or 'Rejected' (successful_match != 0).
        # - Then by `match_score` in descending order.
        properties = sorted(
            properties,
            key=lambda x: (x['matching_status'] == '', -x['match_score'])
        )
        print('properties:', properties)

    # Render the customer dashboard with properties and match statistics
    return render_template('/customer_dashboard.html', properties=properties, matches=matches)

# The provider dashboard load function
def dashboard_2(user_id):
    users = []

    # Get all offers made by the provider
    all_offers = Offer.query.filter_by(user_id=user_id).all()

    for offer in all_offers:
        matches = Matches.query.filter(Matches.offer_id == offer.id, Matches.successful_match.in_([1, 2])).all()
        print('matches:', matches)

        for m in matches:  # Process each match
            matched_user = FlatMate.query.filter_by(id=m.user_id).first()
            if matched_user:
                preferences = Preferences.query.filter_by(user_id=matched_user.id).first()
                print('preferences:', preferences)

                # Map preferences to human-readable format
                social_level = {
                    1: '1 - I like keeping to myself most of the time.',
                    2: '2 - I prefer occasional social interactions.',
                    3: '3 - A mix of hanging out and doing our own thing sounds great.',
                    4: '4 - I enjoy frequent social interactions.',
                    5: '5 - Let’s hang out and do things together often!'
                }.get(preferences.community, '')
                pet_level = {
                    1: '1 - Not at all comfortable',
                    2: '2 - Slightly comfortable',
                    3: '3 - Moderately comfortable',
                    4: '4 - Very comfortable',
                    5: '5 - Extremely comfortable'
                }.get(preferences.pets, '')
                smoking_level = {
                    1: '1 - Not at all comfortable',
                    2: '2 - Slightly comfortable',
                    3: '3 - Moderately comfortable',
                    4: '4 - Very comfortable',
                    5: '5 - Extremely comfortable'
                }.get(preferences.smoking, '')
                fitness_level = {
                    1: '1 - Never',
                    2: '2 - Rarely',
                    3: '3 - Occasionally',
                    4: '4 - Often',
                    5: '5 - Very frequently'
                }.get(preferences.fitness, '')
                attendance_level = {
                    1: '1 - Never',
                    2: '2 - Rarely',
                    3: '3 - Sometimes',
                    4: '4 - Often',
                    5: '5 - Always'
                }.get(preferences.attendance, '')

                # Append user details to the list
                users.append({
                    'user_id': matched_user.id,
                    'name': matched_user.first_name,
                    'email': matched_user.email,
                    'gender': 'male' if preferences.sex else 'female',
                    'age': preferences.age,
                    'language': preferences.language,
                    'community': social_level,
                    'degree': 'Master' if preferences.degree else 'Bachelor',
                    'semester': preferences.semester,
                    'smoking': smoking_level,
                    'pets': pet_level,
                    'fitness': fitness_level,
                    'attendance': attendance_level,
                    # relationship status let out, this is not a dating app
                })
                print('users:', users)

    # Render the provider dashboard
    return render_template('/provider_dashboard.html', users=users)

# The filtering function
def filtering_1(user_id, request):
    # Parse filter criteria from the request
    min_sq_meters = request.form.get("min_sq_meters", type=int, default=0)
    max_distance_to_uni = request.form.get("max_distance_to_uni", type=int, default=1000000)
    max_price = request.form.get("max_price", type=int, default=100000000)

    # Filter offers based on criteria
    offers = Offer.query.filter(
        Offer.apartment_size >= min_sq_meters,
        Offer.distance <= max_distance_to_uni,
        Offer.price <= max_price
    ).all()

    # Filter matches by valid offers
    matches = Matches.query.filter(Matches.offer_id.in_([offer.id for offer in offers]), Matches.user_id == user_id).all()

    # Create matchings list with scores
    matchings = [
        {'match_id': match.id, 'matching_score': match.score}
        for match in matches
    ]

    # Sort matches by score
    matchings.sort(key=lambda x: x['matching_score'], reverse=True)

    # Pass filtered matches to the customer dashboard
    return dashboard_1(user_id, 3, matchings)

# The matching function
def matches_1(user_id, request):
    offer_id = request.form.get("offer_id")  # Retrieve offer ID
    if offer_id:
        match = Matches.query.filter_by(user_id=user_id, offer_id=offer_id).first()
        match.successful_match = 1  # Set match status to pending
        db.session.commit()

    return dashboard_1(user_id, 2)  # Refresh dashboard with updated matches

# Provider accepts the match
def accept_1(user_id, request):
    matched_user_id = request.args.get("user_id")
    print('matched_user_id:', matched_user_id)
    if matched_user_id:
        offer_id = Offer.query.filter_by(user_id=user_id).first().id
        match = Matches.query.filter_by(user_id=matched_user_id, offer_id=offer_id).first()
        match.successful_match = 2  # Set status to successful
        db.session.commit()

    return redirect('/provider_dashboard')

# Provider rejects the match
def reject_1(user_id, request):
    matched_user_id = request.args.get("user_id")
    if matched_user_id:
        offer_id = Offer.query.filter_by(user_id=user_id).first().id
        match = Matches.query.filter_by(user_id=matched_user_id, offer_id=offer_id).first()
        match.successful_match = 3  # Set status to rejected
        db.session.commit()

    return redirect('/provider_dashboard')

def refresh_1(user_id):
    # delete old matches to refresh with new ones
    all_matches = Matches.query.filter_by(user_id=user_id, successful_match=0).all()
    for match in all_matches:
        db.session.delete(match)
    return dashboard_1(user_id, 1)  # Refresh dashboard with updated matches