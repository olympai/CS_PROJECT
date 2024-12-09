#import external libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import MinMaxScaler

from db_config import db
from db_config.db_tables import Matches, Offer


# Initialize empty lists for matchings and matching scores
matchings = []
matching_score = 0

#define matching score function
# Calculate matching score based on euclidean distance, some back and forth conversion is needed to make sure the data is in the right format (np and dataframes). also NaNs are filled with 0 
def calculate_matching_score(df, user1, user2):
    user1_preferences = df[df['user_id'] == user1].drop(['user_id'], axis=1).apply(pd.to_numeric, errors='coerce').fillna(0).values.flatten()
    user2_preferences = df[df['user_id'] == user2].drop(['user_id'], axis=1).apply(pd.to_numeric, errors='coerce').fillna(0).values.flatten()
    return euclidean(user1_preferences, user2_preferences)

#define clustering function
def clustering_function(session_id):
    df = pd.read_sql('SELECT * FROM preferences p JOIN flatmate f ON p.user_id = f.id WHERE f.type = TRUE', db.engine)
    #used for matching scores later on
    df_later = df.copy()
    #replace NaNs with True to avoid errors
    df = df.fillna(True)

    #  Define features as specified in clustering.ipynb
    X = pd.get_dummies(df[["semester", "attendance", "fitness"]])
    #make sure true and false are replaced with 0 and 1
    X = np.where(X == True, 1, X)
    X = np.where(X == False, 0, X)

    # Standardize features using MinMaxScaler (preprocessing to improve model performance)
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    #define best amount of clusters based on clusterting.ipynb results
    best_cluster = 10

    #fit the model for best amount of clusters
    kmeans = KMeans(n_clusters=best_cluster)

    #add the cluster to the dataframe (for matching)
    df['cluster'] = kmeans.fit_predict(X)

    # Group customers by cluster
    clusters = df.groupby('cluster')['user_id'].apply(list).to_dict()

    # Add the matching customers to the matchings list
    for cluster, customers in clusters.items():
        for i in range(len(customers)):
            for j in range(len(customers)):
                if i != j:  # Avoid self-matching(!)
                    matchings.append((customers[i], customers[j]))

    # Convert matches to a DataFrame for better clarity
    matches_df = pd.DataFrame(matchings, columns=['user_id', 'offer_id'])

    # Add matching score to matches_df
    matches_df['matching_score'] = matches_df.apply(lambda row: calculate_matching_score(df_later, row['user_id'], row['offer_id']), axis=1)

    # Sort matches by matching score in ascending order (lower distance means better match)
    matches_df = matches_df.sort_values(by='matching_score')
    # Normalize matching scores to a range of 0-100 for better interpretation
    min_score = matches_df['matching_score'].min()
    max_score = matches_df['matching_score'].max()
    matches_df['normalized_matching_score'] = 100 * (1 - (matches_df['matching_score'] - min_score) / (max_score - min_score))

    # # Print the DataFrame with normalized scores to check if it works
    # print(matches_df)
    # print(session_id)

    # Add matches to the database 
    this_df = matches_df[matches_df['user_id'] == session_id]
    print('this df:', this_df)

    # #another check if this works
    # print(this_df)

    # delete old matches
    Matches.query.filter_by(user_id=session_id).delete()
    db.session.commit()


    for index, row in this_df.iterrows():
        print(int(row['offer_id']))
        try:
            offer = Offer.query.filter_by(user_id=int(row['offer_id'])).first()
            # append to database
            new_match = Matches(
                user_id=session_id,
                offer_id=offer.id,
                score=float(row['normalized_matching_score'])
            )
            db.session.add(new_match)
        except:
            print('Error: Could not find offer with id ' + str(row['offer_id']))
            continue
    db.session.commit()

    pass