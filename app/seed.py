from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Hero, Power, HeroPower
 
# Set up the database connection
engine = create_engine("sqlite:///instance/app.db")
# db.init_app(engine)
Session = sessionmaker(bind=engine)
session = Session()
 
# Create heroes
heroes = [
    Hero(
        name=f"Hero {i + 1}",
        super_name=f"Superhero {i + 1}",
        created_at=datetime.utcnow(),
    )
    for i in range(10)
]
 
# Create powers
powers = [
    Power(
        name=f"Power {i + 1}",
        description=f"Description {i + 1} - More than 20 characters",
        created_at=datetime.utcnow(),
    )
    for i in range(10)
]
 
# Create hero_powers associations with valid strength values
hero_powers = [
    HeroPower(
        strength="Strong",  # Use a valid strength value
        hero=heroes[i % len(heroes)],
        power=powers[i % len(powers)],
        created_at=datetime.utcnow(),
    )
    for i in range(10)
]
 
# Add objects to the session
session.add_all(heroes + powers + hero_powers)
 
# Commit the session to persist the data
try:
    session.commit()
    print("Data added successfully!")
except ValueError as e:
    # Handle validation errors
    print(f"Validation error: {e}")
    session.rollback()
finally:
    session.close()