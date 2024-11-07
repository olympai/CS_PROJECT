# importing the necessary tables
from db_config import db
from db_config.db_tables import Preferences, Offer, Matches

# the machine learning function
def clustering_function(user_id):
    # initialize empty
    matchings = []
    matching_score = 0

    # get the preferences of a user or specification of the offer, look the structure in db_config.db_table up
    preferences = Preferences.query.filter_by(id=user_id).first()
    offers = Offer.query.all()

    # YOUR CODE 
    # ...

    # return the matchings, e.g. with the following structure
    matchings = [
        # best matchings in descending order
        # best matching
        {
            'offer_id': '...', # the corresponding offer_id
            'matching_score': matching_score # the score on which basis we should rank the matchings
        },
        # second best matching
        {
            'offer_id': '...', # the corresponding offer_id
            'matching_score': matching_score # the score on which basis we should rank the matchings
        }
        # n-th best matching
        # ...
    ]

    # append new matches to the database, following this structure (also look in
    for match in matchings:
        new_match = Matches(
            user_id = user_id,
            offer_id = match.offer_id,
            score = match.matching_score
        )
        db.session.add(new_match)
    db.session.commit()

    return matchings