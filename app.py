import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precip<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/><br/>"
    )

@app.route("/api/v1.0/precip")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query dates/measurements
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()
    
    for date, precip in results:
        datadict = {}
        datadict['date'] = date
        datadict['precip'] = precip
        precipdict.append(datadict)
    
    return jsonify(precipdict)

