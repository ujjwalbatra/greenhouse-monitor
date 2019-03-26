from database import greenhouse_monitor_database
import random

db = greenhouse_monitor_database.GreenhouseMonitorDatabase()
db.create_tables()
for x in range(30):
    db.insert_sensor_data(random.randint(1, 40), random.randint(40, 90))
