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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startDate<br/>"
        f"/api/v1.0/startDate/endDate<br/><br/>"
        f"Input dates as: YYYY-MM-DD"
    )

@app.route("/api/v1.0/precip")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query dates/measurements
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()
    
    precipL = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['precip'] = prcp
        precipL.append(precip_dict)
    
    # convert list
    
    return jsonify(precipL)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query all station names
    results = session.query(station.name).all()
    session.close()

    #conversions
    AStations = list(np.ravel(results))
    return jsonify(AStations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query dates and temperature observations for the most active station 
    results = session.query(measurement.date, measurement.tobs).\
                filter(measurement.station == 'USC00519281', measurement.date > "2016-08-23").all()

    # convert the results into a dictionary of temp observed by date 
    tobsL = []

    for date, temp in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['temp'] = temp
        tobsL.append(tobs_dict)

    #convert
    return jsonify(tobsL)


@app.route("/api/v1.0/<start>")
def start(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #select and filter
    sel = [func.min(measurement.tobs), 
    func.max(measurement.tobs), 
    func.avg(measurement.tobs),]
    calc = session.query(*sel).filter(measurement.date >= start).all()
    calc

    session.close()

    # Convert
    astart = list(np.ravel(calc))
    return jsonify(astart)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [func.min(measurement.tobs), 
    func.max(measurement.tobs), 
    func.avg(measurement.tobs),]
    calc2= session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    calc2

    session.close()

    # Convert 
    astart_end = list(np.ravel(calc2))
    return jsonify (astart_end)

if __name__ == '__main__':
    app.run(debug=True)  
