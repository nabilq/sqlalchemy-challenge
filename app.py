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

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station






# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
#Home page.
#List all routes that are available.
@app.route("/")
def welcome():
    return (
        f"Aloha! This is the Hawaii temperature and precipitation API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

        
    )



# 4. Define what to do when a user hits the /api/v1.0/precipitation route
#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of the last year of weather including the date and precipitation of each day"""
    daterange = session.query(measurement.date, measurement.prcp).filter(measurement.date.between('2016-08-23', '2017-08-23')).all()

    session.close()

    # Create a dictionary from the row data and append to a list of daterangelist
    daterangelist= []
    for date, prcp in daterange:
        daterange_dict = {}
        daterange_dict["date"] = date
        daterange_dict["prcp"] = prcp
        daterangelist.append(daterange_dict)
    return jsonify(daterangelist)
  

@app.route("/api/v1.0/stations")
#5. Define /api/v1.0/stations
#Return a JSON list of stations from the dataset.

def stations():
  # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(station.station).all()

    session.close()
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
#6. /api/v1.0/tobs
#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures"""
    # Query all passengers
    stationrange = session.query(measurement.tobs).\
            filter(measurement.date.between('2016-08-18', '2017-08-18')).filter_by(station="USC00519281").all()

    session.close()

    # Convert list of tuples into normal list
    stationrange_list= []

    for x in stationrange:
        stationrange_list.append(x[0])

    return jsonify(stationrange_list)



#7 
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")

def calc_temps(start):

    session = Session(engine)
    start=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= "2017-08-23").all()
    session.close()

    startlist = list(start)


    return jsonify(startlist)
    






@app.route("/api/v1.0/<start>/<end>")

def route_temps(start, end):

    session = Session(engine)
    start=session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()

    startlist = list(start)


    return jsonify(startlist)

if __name__ == "__main__":
   app.run(debug=True)
