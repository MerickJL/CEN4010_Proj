# Base imports
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# Flask app
app = Flask(__name__)
DBPATH = "sqlite:///" + os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "db.sqlite"
)
# Set database
app.config["SQLALCHEMY_DATABASE_URI"] = DBPATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # Init db
db = SQLAlchemy(app)

# # Init Marshmallow
ma = Marshmallow(app)

# Component imports
"""
We are going to keep classes in separate files. This way it will be easier to
maintain and integrate new features. Please be sure to name classes uniquely.
"""
#import components.views  # noqa:402
import components.controller_browsing_and_sorting_sachin # noqa:402
import components.views  # noqa:402

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, host="0.0.0.0", port=50745)
