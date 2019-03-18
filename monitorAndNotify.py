from database import greenhouse_monitor_database


db = greenhouse_monitor_database.GreenhouseMonitorDatabase()

db.create_tables()
db.insert_notification_confirmation()