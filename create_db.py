from api2 import app, db

with app.app_context():
    # Create the database and the database table
    db.create_all()
