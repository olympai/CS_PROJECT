import random
from faker import Faker
from sqlalchemy import text

from db_config import db
from db_config.db_tables import Preferences, FlatMate

def update_db():
    drop_table_sql = text('DROP TABLE Preferences')
    db.session.execute(drop_table_sql)
    drop_table_sql = text('DROP TABLE Matches')
    db.session.execute(drop_table_sql)
    drop_table_sql = text('DROP TABLE Offer')
    db.session.execute(drop_table_sql)

    db.create_all()
    db.session.commit()
    return "Done"

def init_db():
    # Initialize Faker for generating random data
    faker = Faker()

    # Generate dataset with 100 random entries
    entries = []
    for i in range(1, 101):  # Assuming user_id starts from 1
        entry = Preferences(
            user_id=i,
            pets=random.choice([True, False, None]),
            smoking=random.choice([True, False, None]),
            sex=random.choice([True, False, None]),  # True for Male, False for Female, None for not specified
            age=random.randint(18, 35) if random.random() > 0.1 else None,  # 10% chance for None
            relationship_status=random.choice([True, False, None]),  # True for In a relationship, False otherwise
            degree=random.choice([True, False, None]),  # True for Master, False for Bachelor
            parking_spots=random.choice([True, False, None]),
            language=faker.language_name() if random.random() > 0.1 else None,  # 10% chance for None
            condition=random.choice([True, False, None]),  # True for new, False for old
            community=random.randint(1, 5) if random.random() > 0.1 else None,  # Scale 1 to 5, 10% chance for None
            attendance=random.choice([True, False, None]),  # True for weekend there, False otherwise
            semester=random.randint(1, 12) if random.random() > 0.1 else None,  # Up to 12 semesters
            fitness=random.choice([True, False, None]),
            baths_per_person=round(random.uniform(0.5, 2.0), 1) if random.random() > 0.1 else None  # Decimal between 0.5 and 2.0
        )
        entries.append(entry)

    # Add entries to the database
    db.session.add_all(entries)
    db.session.commit()

    return "100 preferences entries have been added to the database."