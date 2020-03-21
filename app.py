from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

#################################################
# Database Setup
#################################################
# Reference: https://stackoverflow.com/questions/33055039/using-sqlalchemy-scoped-session-in-theading-thread
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)


Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home Route
@app.route("/")
def welcome():
   
     return (
        f"Available Routes:<br/>"
        f"The dates and temperature observations from the last year:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"List of stations from the dataset:<br/>"
        f"/api/v1.0/stations<br/>"
        f"List of Temperature Observations (tobs) for the previous year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"List of the minimum temperature, the average temperature, and the max temperature for a given start(i.e.2017-1-1):<br/>"
        f"/api/v1.0/<start><br/>"
        f"List of the minimum temperature, the average temperature, and the max temperature for a given start and end(i.e.2017-01-01/2017-01-07):<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
         
        prcp_data = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= one_year_ago).\
            order_by(Measurement.date).all()
        
        prcp_data_list = dict(prcp_data)
        
        return jsonify(prcp_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        stations_all = session.query(Station.station, Station.name).all()
        
        station_list = list(stations_all)
        return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        tobs_data_list = list(tobs_data)
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        start_day_list = list(start_day)
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        start_end_day_list = list(start_end_day)
        return jsonify(start_end_day_list)

#################################################
if __name__ == '__main__':
    app.run(debug=True)