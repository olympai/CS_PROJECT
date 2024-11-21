import random
from faker import Faker
from sqlalchemy import text

from db_config import db
from db_config.db_tables import Preferences, FlatMate, Offer

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
    for i in range(2, 102):  # Assuming user_id starts from 1
        # Create sample users
        user = FlatMate(
            id=i,
            first_name=faker.name(),
            email=faker.email(),
            password=faker.password(),
            type=True
        )
        db.session.add(user)


        entry = Preferences(
            user_id=i,
            pets=random.choice([True, False]),
            smoking=random.choice([True, False]),
            sex=random.choice([True, False]),  # True for Male, False for Female, None for not specified
            age=random.randint(18, 35),  # 10% chance for None
            relationship_status=random.choice([True, False]),  # True for In a relationship, False otherwise
            degree=random.choice([True, False]),  # True for Master, False for Bachelor
            language=faker.language_name(),  # 10% chance for None
            community=random.randint(1, 3),  # Scale 1 to 3, 10% chance for None
            attendance=random.choice([True, False]),  # True for weekend there, False otherwise
            semester=random.randint(1, 8),  # Up to 12 semesters
            fitness=random.choice([True, False])  # True for sportive, False for not sportive
        )
        entries.append(entry)

        offer = Offer(
            id=i,
            user_id=i,
            title=faker.sentence(nb_words=2),
            description=faker.text(max_nb_chars=200),
            address=faker.address(),
            price=random.randint(300, 1500),
            distance=random.randint(1, 10),
            apartment_size=random.randint(20, 100),
            room_size=random.randint(10, 30),
            roommates=random.randint(1, 5),
            bathrooms=random.randint(1, 4)
        )
        db.session.add(offer)

    # Add entries to the database
    db.session.add_all(entries)
    db.session.commit()

    return "100 preferences entries have been added to the database."
