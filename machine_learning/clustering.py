#import external libraries
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import euclidean

from db_config import db
from db_config.db_tables import Matches, Offer

# Initialize empty lists for matchings and matching scores
matchings = []
matchings_entries = []
matching_score = 0

#define matching score function
# Calculate matching score based on euclidean distance
def calculate_matching_score(df, user1, user2):
    user1_preferences = df[df['user_id'] == user1].drop(['user_id'], axis=1).apply(pd.to_numeric, errors='coerce').fillna(0).values.flatten()
    user2_preferences = df[df['user_id'] == user2].drop(['user_id'], axis=1).apply(pd.to_numeric, errors='coerce').fillna(0).values.flatten()
    return euclidean(user1_preferences, user2_preferences)

#define clustering function
def clustering_function(session_id):
    df = pd.read_sql('SELECT * FROM preferences', db.engine)
    df_later = df.copy()
    print('1:', df[df['user_id'] == session_id])
    #replace NaNs with True to avoid errors
    df = df.fillna(True)

    print('2:', df[df['user_id'] == session_id])

    #  Define features and hot-encode categorical variables
    X = pd.get_dummies(df[["pets", "sex", "age", "smoking"]])
    #make sure true and false are replaced with 0 and 1
    X = np.where(X == True, 1, X)
    X = np.where(X == False, 0, X)

    #Standardize features (preprocessing to improve model performance)
    scaler = StandardScaler() 
    X = scaler.fit_transform(X) 

    print('3:', df[df['user_id'] == session_id])

    #define our clusters
    #define cluster list, start from 2 so that silhouette score can be calculated
    cluster_amount = list(range(10, 100))
    best_score = -1
    best_cluster = None
    for i in cluster_amount:
        kmeans = KMeans(n_clusters=i)
        #fit the model 
        df['cluster'] = kmeans.fit_predict(X)

        #Evaluate performance using the silhouette score and find best performing cluster amount
        silhouette_avg = silhouette_score(X, df['cluster'])
        if silhouette_avg > best_score:
            best_score = silhouette_avg
            best_cluster = i

    print('4:', df[df['user_id'] == session_id])

    # print(f'Best Silhouette Score is: {best_score} for {best_cluster} clusters')

    #fit the model for best amount of clusters
    kmeans = KMeans(n_clusters=best_cluster)

    #add the cluster to the dataframe
    df['cluster'] = kmeans.fit_predict(X)

    print('5:', df[df['user_id'] == session_id])

    # Group customers by cluster
    clusters = df.groupby('cluster')['user_id'].apply(list).to_dict()

    print('6:', clusters)

    # Add the matching customers to the matchings list
    for cluster, customers in clusters.items():
        for i in range(len(customers)):
            for j in range(len(customers)):
                if i != j:  # Avoid self-matching
                    matchings.append((customers[i], customers[j]))

    # Convert matches to a DataFrame for better clarity
    matches_df = pd.DataFrame(matchings, columns=['user_id', 'offer_id'])

    print('7:', matches_df[matches_df['user_id'] == session_id])

    # Add matching score to matches_df
    matches_df['matching_score'] = matches_df.apply(lambda row: calculate_matching_score(df_later, row['user_id'], row['offer_id']), axis=1)

    print('8:', matches_df[matches_df['user_id'] == session_id])

    # Sort matches by matching score in ascending order (lower distance means better match)
    matches_df = matches_df.sort_values(by='matching_score')
    # Normalize matching scores to a range of 0-100
    min_score = matches_df['matching_score'].min()
    max_score = matches_df['matching_score'].max()

    print('9:', matches_df[matches_df['user_id'] == session_id])

    matches_df['normalized_matching_score'] = 100 * (1 - (matches_df['matching_score'] - min_score) / (max_score - min_score))

    print('10:', matches_df[matches_df['user_id'] == session_id])

    # Print the DataFrame with normalized scores to check if it works
    print(matches_df)
    print(session_id)

    # Add matches to the database 
    this_df = matches_df[matches_df['user_id'] == session_id]

    print(this_df)

    # delete old matches
    Matches.query.filter_by(user_id=session_id).delete()
    db.session.commit()
    
    for index, row in this_df.iterrows():
        offer = Offer.query.filter_by(user_id=int(row['offer_id'])).first()
        # append to database
        new_match = Matches(
            user_id=session_id,
            offer_id=int(offer.id),
            score=float(row['normalized_matching_score'])
        )
        db.session.add(new_match)
    db.session.commit()

    return matchings_entries