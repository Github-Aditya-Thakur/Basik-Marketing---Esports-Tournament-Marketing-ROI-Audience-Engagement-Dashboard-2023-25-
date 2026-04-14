import random
import pandas as pd
from datetime import datetime, timedelta
import mysql.connector

# ---- CONFIG ----
NUM_EVENTS = 80
DAYS_BEFORE_EVENT = 30


#Popular Stuff --<><>
games = ["Valorant", "BGMI", "CS2", "Free Fire", "Dota 2", "Fortnite"]
regions = ["India", "SEA", "MENA", "EU", "NA"]
channels = ["Influencer", "Paid Ads", "Organic", "PR"]
platforms = ["YouTube", "Instagram", "Twitter", "Twitch"]

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwerty@2005",
    database="esports_marketing"
)
cursor = conn.cursor()

# ---- EVENTS ----
events = []
start_date = datetime(2024, 1, 1)

for i in range(1, NUM_EVENTS + 1):
    event_date = start_date + timedelta(days=random.randint(10, 600))
    events.append([
        i,
        f"Basik Cup {i}",
        random.choice(games),
        event_date.date(),
        random.choice(regions)
    ])

events_df = pd.DataFrame(events, columns=["event_id","event_name","game","event_date","region"])

# Insert events
cursor.executemany(
    "INSERT INTO events (event_id, event_name, game, event_date, region) VALUES (%s,%s,%s,%s,%s)",
    events
)

# ---- MARKETING + SOCIAL (Daily) ----
for ev in events:
    event_id = ev[0]
    event_date = ev[3]

    for d in range(DAYS_BEFORE_EVENT):
        day = event_date - timedelta(days=d)

        # marketing spend
        for ch in channels:
            spend = round(random.uniform(100, 2000), 2)
            cursor.execute(
                "INSERT INTO marketing_spend (event_id, channel, spend, spend_date) VALUES (%s,%s,%s,%s)",
                (event_id, ch, spend, day)
            )

        # social metrics
        for pl in platforms:
            impressions = random.randint(5000, 200000)
            clicks = random.randint(200, 5000)
            engagement = random.randint(100, 3000)
            cursor.execute(
                "INSERT INTO social_metrics (event_id, platform, impressions, clicks, engagement, metric_date) VALUES (%s,%s,%s,%s,%s,%s)",
                (event_id, pl, impressions, clicks, engagement, day)
            )

    # viewership + registrations
    peak_viewers = random.randint(2000, 200000)
    avg_watch_time = round(random.uniform(5, 60), 2)
    signups = random.randint(300, 15000)
    conversions = int(signups * random.uniform(0.2, 0.6))

    cursor.execute(
        "INSERT INTO viewership (event_id, peak_viewers, avg_watch_time) VALUES (%s,%s,%s)",
        (event_id, peak_viewers, avg_watch_time)
    )
cursor.execute(
    "INSERT INTO registrations (event_id, signups, conversions) VALUES (%s,%s,%s)",
    (event_id, signups, conversions)
)
conn.commit()
cursor.close()
conn.close()

print("Data generation complete.")
