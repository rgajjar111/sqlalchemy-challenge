# Import the dependencies.
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# 1. Import Flask
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def Home():
    return (
        f"<h1/>Welcome to the Hawai Climate App ! </h1>"
        f"<h2/>Available Routes:</h2>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end <br/>"
        f"<p/>'start' and 'end' date should be available in the format YYYY-MM-DD <p/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    #Query 12 months of data
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= '2016-08-23').all()
    
    session.close()
    
    #create a dictionary
    prcp_dict = {date: prcp for date, prcp in prcp_data}
    return jsonify(prcp_dict)
    
@app.route("/api/v1.0/stations")
def stations():
    session= Session(engine)

    #Query the list of stations
    station_list = session.query(Station.station).all()

    session.close()
    stations = [station[0] for station in station_list]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #Query the dates and temperature observations of the most-active station for the previous year of data
    tobs_data = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date>= '2016-08-23', Measurement.station == 'USC00519281').all()
    session.close()
    tobs_dict = {date: tobs for date, tobs in tobs_data}
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    session = Session(engine)

    # Query the temperature statistics based on the provided date range(s)
    if end:
        # For the specified start and end date range
        temperature_stats = session.query(func.min(Measurement.tobs).label('TMIN'),
                                           func.avg(Measurement.tobs).label('TAVG'),
                                           func.max(Measurement.tobs).label('TMAX'))\
            .filter(Measurement.station == 'USC00519281', Measurement.date >= start, Measurement.date <= end).all()
    else:
        # For the specified start date only
        temperature_stats = session.query(func.min(Measurement.tobs).label('TMIN'),
                                           func.avg(Measurement.tobs).label('TAVG'),
                                           func.max(Measurement.tobs).label('TMAX'))\
            .filter(Measurement.station == 'USC00519281', Measurement.date >= start).all()
   

    session.close()

    # Create a dictionary with temperature statistics
    temp_stats_dict = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }

    return jsonify(temp_stats_dict)

if __name__ == "__main__":
    app.run(debug=True)