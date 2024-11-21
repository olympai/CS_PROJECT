from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import euclidean

from db_config import db
from db_config.db_tables import Matches, Offer

# the machine learning function
# def clustering_function(user_id):
# initialize empty
matchings = []
matchings_entries = []
matching_score = 0


# Calculate matching score based on euclidean distance
def calculate_matching_score(user1, user2):
    df = pd.read_sql('SELECT * FROM preferences', db.engine)

    user1_preferences = df[df['user_id'] == user1].drop(['user_id', 'cluster'], axis=1).apply(pd.to_numeric, errors='coerce').fillna(0).values.flatten()
    user2_preferences = df[df['user_id'] == user2].drop(['user_id', 'cluster'], axis=1).apply(pd.to_numeric, errors='coerce').fillna(0).values.flatten()
    return euclidean(user1_preferences, user2_preferences)


def clustering_function(session_id):
    df = pd.read_sql('SELECT * FROM preferences', db.engine)
    #replace NaNs with True to avoid errors
    df = df.fillna(True)

    #  Define features and target
    X = pd.get_dummies(df[["pets", "sex", "age", "smoking"]])
    X = np.where(X == True, 1, X)
    X = np.where(X == False, 0, X)

    #Standardize features 
    scaler = StandardScaler() 
    X = scaler.fit_transform(X) 

    #define our clusters
    #define cluster list, start from 2 so that silhouette score can be calculated
    cluster_amount = list(range(10, 100))
    for i in cluster_amount:
        kmeans = KMeans(n_clusters=i)
        #fit the model 
        df['cluster'] = kmeans.fit_predict(X)

        #Evaluate performance
        silhouette_avg = silhouette_score(X, df['cluster'])
        if 'best_score' not in locals() or silhouette_avg > best_score:
            best_score = silhouette_avg
            best_cluster = i

    # print(f'Best Silhouette Score is: {best_score} for {best_cluster} clusters')

    kmeans = KMeans(n_clusters=best_cluster)
    #fit the model 
    df['cluster'] = kmeans.fit_predict(X)

    # Group customers by cluster
    clusters = df.groupby('cluster')['user_id'].apply(list).to_dict()

    #add the matchings to the list
    for cluster, customers in clusters.items():
        for i in range(len(customers)):
            for j in range(i + 1, len(customers)):  # Avoid self-matching and duplicates
                matchings.append((customers[i], customers[j]))

    # Convert matches to a DataFrame for clarity
    matches_df = pd.DataFrame(matchings, columns=['user_id', 'offer_id'])
    print(matches_df)

    # Add matching score to matches_df
    matches_df['matching_score'] = matches_df.apply(lambda row: calculate_matching_score(row['user_id'], row['offer_id']), axis=1)

    # Sort matches by matching score in ascending order (lower distance means better match)
    matches_df = matches_df.sort_values(by='matching_score')
    # Normalize matching scores to a range of 0-100
    min_score = matches_df['matching_score'].min()
    max_score = matches_df['matching_score'].max()

    matches_df['normalized_matching_score'] = 100 * (1 - (matches_df['matching_score'] - min_score) / (max_score - min_score))

    # Print the DataFrame with normalized scores
    # print(matches_df)

    this_df = matches_df[matches_df['user_id'] == session_id]
    for index, row in this_df.iterrows():
        offer = Offer.query.filter_by(user_id=row['offer_id']).first()
        matchings_entries.append({
            'offer_id': offer.id,
            'match_score': row['normalized_matching_score']
        })
        # append to database
        new_match = Matches(
            user_id=session_id,
            offer_id=offer.id,
            score=row['normalized_matching_score']
        )
        db.session.add(new_match)
    db.session.commit()

    return matchings