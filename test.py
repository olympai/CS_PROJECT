import pandas as pd
import random

# Reload the flatmates.csv file
flatmates_file = 'flatmates.csv'
flatmates_df = pd.read_csv(flatmates_file)

# Filter entries where 'type' is True
filtered_flatmates = flatmates_df[flatmates_df['type'] == True]

# Define at least 30 unique addresses in St. Gallen
unique_addresses = [
    "Rosenbergstrasse 51, 9000 St. Gallen",
    "Brühlgasse 20, 9000 St. Gallen",
    "Neugasse 7, 9000 St. Gallen",
    "Marktplatz 5, 9000 St. Gallen",
    "Gallusstrasse 10, 9000 St. Gallen",
    "Vadianstrasse 3, 9000 St. Gallen",
    "Multergasse 4, 9000 St. Gallen",
    "Bohl 1, 9000 St. Gallen",
    "Engelgasse 12, 9000 St. Gallen",
    "Poststrasse 10, 9000 St. Gallen",
    "Notkerstrasse 6, 9000 St. Gallen",
    "Zwinglistrasse 15, 9000 St. Gallen",
    "Schützengarten 8, 9000 St. Gallen",
    "Stadthausgasse 5, 9000 St. Gallen",
    "Lämmlisbrunnenstrasse 2, 9000 St. Gallen",
    "Spisergasse 18, 9000 St. Gallen",
    "Rathausgasse 9, 9000 St. Gallen",
    "Bahnhofstrasse 25, 9000 St. Gallen",
    "Davidstrasse 10, 9000 St. Gallen",
    "Schibenertorstrasse 3, 9000 St. Gallen",
    "Museumstrasse 7, 9000 St. Gallen",
    "Tigerbergstrasse 12, 9000 St. Gallen",
    "Unterer Graben 20, 9000 St. Gallen",
    "Oberer Graben 11, 9000 St. Gallen",
    "Leonhardsstrasse 30, 9000 St. Gallen",
    "Gerbergasse 17, 9000 St. Gallen",
    "Winkelriedstrasse 22, 9000 St. Gallen",
    "Schützengasse 4, 9000 St. Gallen",
    "Webergasse 13, 9000 St. Gallen",
    "Kornhausstrasse 19, 9000 St. Gallen"
]*20

# Prepare titles and descriptions for diversity
titles = [
    "Modern Apartment in the City",
    "Affordable Flat for Students",
    "Spacious Rooms in Prime Location",
    "Quiet Flat with a Great View",
    "Stylish Apartment in St. Gallen"
]
descriptions = [
    "Perfect for students, close to amenities and public transport.",
    "Cozy apartment with modern furnishings and a central location.",
    "Spacious flat with great natural light and modern appliances.",
    "A quiet retreat with all necessary amenities for a comfortable stay.",
    "An affordable option for students and young professionals."
]

# Generate realistic entries for the Offer table
offer_data = []
offer_id = 1  # Start ID for offers
address_pool = unique_addresses[:len(filtered_flatmates)]  # Ensure enough unique addresses

for i, (_, row) in enumerate(filtered_flatmates.iterrows()):
    offer_entry = {
        "id": offer_id,
        "user_id": int(row['id']),  # Assuming 'id' column exists in flatmates.csv
        "title": titles[i % len(titles)],  # Rotate through titles
        "description": descriptions[i % len(descriptions)],  # Rotate through descriptions
        "address": address_pool[i],
        "price": round(random.uniform(800, 2000), 2),  # Random price between 800 and 2000
        "distance": round(random.uniform(0.5, 3.0), 1),  # Random distance between 0.5 and 3.0 km
        "apartment_size": round(random.uniform(2.0, 5.0), 1),  # Random apartment size between 2.0 and 5.0 rooms
        "room_size": round(random.uniform(10.0, 25.0), 1),  # Random room size between 10 and 25 sqm
        "roommates": random.randint(1, 4),  # Random number of roommates between 1 and 4
        "bathrooms": random.randint(1, 2)  # Random number of bathrooms between 1 and 2
    }
    offer_data.append(offer_entry)
    offer_id += 1

# Create a DataFrame for the Offer table
offer_df = pd.DataFrame(offer_data)

# Output CSV file path
output_csv_file = "realistic_offer_entries2.csv"

# Save the Offer table to a CSV file
offer_df.to_csv(output_csv_file, index=False)