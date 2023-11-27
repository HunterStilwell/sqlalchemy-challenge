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
        f'Available Routes: <br>'
        f'Precipitation (/api/v1.0/precipitation) <br>'
        f'Stations (/api/v1.0/stations) <br>'
        f'Temperature Observations (/api/v1.0/tobs) <br>'
        f'Start Date (/api/v1.0/<start>) <br>'
        f'Start-End Date Range (/api/v1.0/<start>/<end>)'
    )
    

# precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(2016,8,23)).all()
    prcpWithDates =[]
    for date, prcp in results:
        prcpDictionary = {date:prcp}
        prcpWithDates.append(prcpDictionary)
        

    return jsonify(prcpWithDates)


# stations
@app.route("/api/v1.0/stations")
def stations():
    results2 = session.query(Station.station).all()
    stations = list(np.ravel(results2))

    return jsonify(stations)


# temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    results3 = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281")\
    .filter(Measurement.date >= dt.date(2016,8,23)).all()

    tobs = list(np.ravel(results3))

    return jsonify(tobs)


# start and start-end date ranges
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def startEndDate(start=0,end=0):

    functionList = [
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ]
    output = []


    if end == 0:
        startDate = start.split(',')
        results4 = session.query(functionList[0], functionList[1], functionList[2])\
                .filter(Measurement.date >= dt.date(int(startDate[0]), int(startDate[1]), int(startDate[2]))).all()
    else:
        startDate = start.split(',')
        endDate = end.split(',')
        results4 = session.query(functionList[0], functionList[1], functionList[2])\
                .filter(Measurement.date >= dt.date(int(startDate[0]), int(startDate[1]), int(startDate[2])))\
                .filter(Measurement.date <= dt.date(int(endDate[0]), int(endDate[1]), int(endDate[2]))).all()

    for result in results4:
        output.append(result)

    data = list(np.ravel(output))

    return jsonify(data)





if __name__ == "__main__":
    app.run(debug=True)