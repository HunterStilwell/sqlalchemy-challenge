# Import the dependencies.
import numpy as np
import datetime as dt
from datetime import datetime
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
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# homepage
@app.route("/")
def home():
    return (
        f'Climate App Homepage <br><br>'
        f'Available Routes: <br><br>'
        f'Precipitation (/api/v1.0/precipitation) <br>'
        f'Stations (/api/v1.0/stations) <br>'
        f'Temperature Observations (/api/v1.0/tobs) <br>'
        f'Start Date (/api/v1.0/start_date) <br>'
        f'Start-End Date Range (/api/v1.0/start_date/end_date) <br><br>'
        f'Replace start_date and end_date with dates in this format: year,month,day'
    )
    

# precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # query for precipitation and dates from the measurement table, filtering for dates in the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(2016,8,23)).all()
    # create an empty list
    prcpWithDates =[]
    #create a for loop that saves the dates and precipitations as key-value pairs and then append the list with the dictionaries
    for date, prcp in results:
        prcpDictionary = {date:prcp}
        prcpWithDates.append(prcpDictionary)
        
    # display the list of dictionary entries
    return jsonify(prcpWithDates)


# stations
@app.route("/api/v1.0/stations")
def stations():
    # query for list of stations and save the results as a list
    results2 = session.query(Station.station).all()
    stations = list(np.ravel(results2))

    # display the list of stations
    return jsonify(stations)


# temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    # query to find the temperature measurements for the most active station for the last 12 months
    results3 = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281")\
    .filter(Measurement.date >= dt.date(2016,8,23)).all()

    # save the results in a list
    tobs = list(np.ravel(results3))

    # display the list of temperatures
    return jsonify(tobs)


# start and start-end date ranges
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def startEndDate(start=0,end=0):
    # make an empty list to store data
    output = []

    # if statement to determine if an end date has been included in the search
    if end == 0:
        # split the start date into 3 separate values (year, month, day)
        startDate = start.split(',')
        # query for the minimum, average, and maximum temperatures from the given start date
        results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                .filter(Measurement.date >= dt.date(int(startDate[0]), int(startDate[1]), int(startDate[2]))).all()
    # if an end date was specified
    else:
        # split the start and end dates into 3 separate values (year, month, date)
        startDate = start.split(',')
        endDate = end.split(',')
        # query for the minimum, average, and maximum temperatures from the given start date up to the given end date
        results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                .filter(Measurement.date >= dt.date(int(startDate[0]), int(startDate[1]), int(startDate[2])))\
                .filter(Measurement.date <= dt.date(int(endDate[0]), int(endDate[1]), int(endDate[2]))).all()

    # add the results to the empty output list
    for result in results4:
        output.append(result)

    data = list(np.ravel(output))

    # display the list of minimum, average, and maximum
    return jsonify(data)





if __name__ == "__main__":
    app.run(debug=True)