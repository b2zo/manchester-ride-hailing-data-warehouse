from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker("en_GB")

NUM_ROWS = 50000

locations = [
    "Manchester Airport",
    "Piccadilly",
    "Deansgate",
    "MediaCityUK",
    "Old Trafford",
    "Salford Quays",
    "Stockport",
    "Trafford Centre"
]

trip_types = [
    "Standard",
    "Airport",
    "Business",
    "Premium"
]

rows = []

for i in range(NUM_ROWS):

    pickup_time = fake.date_time_between(
        start_date="-365d",
        end_date="now"
    )

    distance = round(random.uniform(1, 35), 2)

    duration = round(distance * random.uniform(2, 5), 0)

    fare = round(distance * random.uniform(1.2, 2.8), 2)

    rows.append({
        "trip_id": i + 1,
        "pickup_datetime": pickup_time,
        "pickup_location": random.choice(locations),
        "trip_type": random.choice(trip_types),
        "distance_miles": distance,
        "duration_minutes": duration,
        "fare_amount": fare
    })

df = pd.DataFrame(rows)

df.to_csv(
    "data/raw/trips_raw.csv",
    index=False
)

print(f"{len(df)} trips created")