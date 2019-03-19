import json
from database import greenhouse_monitor_database


db = greenhouse_monitor_database.GreenhouseMonitorDatabase()

db.create_tables()
db.insert_to_db(25,35)
db.query_to_db()



