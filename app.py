import numpy as np
import datetime as dt
from statistics import mean
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database setup

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
MS = Base.classes.measurement
ST = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(MS.date,MS.prcp).all()
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    sel3 = [MS.tobs]
    temp = session.query(*sel3).\
        filter(MS.station == "USC00519281").\
        filter (MS.date >= "2016-08-23").\
        all()
    temp2 = list(np.ravel(temp))
    session.close()
    return jsonify(temp2)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    results = session.query(MS.tobs).\
        filter (MS.date >= start_date).\
        all()
    session.close()
    
    results2 = list(np.ravel(results))
    
    results3 = []
    dic = {}
    dic["Start_Date"] = start_date
    dic["TMIN"] = min(results2)
    dic["TAVG"] = mean(results2)
    dic["TMAX"] = max(results2)
    results3.append(dic)
  
    return jsonify(results3)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    session = Session(engine)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    results = session.query(MS.tobs).\
        filter (MS.date >= start_date).\
        filter (MS.date <= end_date).\
        all()
    session.close()
    
    results2 = list(np.ravel(results))
    
    results3 = []
    dic = {}
    dic["Start_Date"] = start_date
    dic["End_Date"] = end_date
    dic["TMIN"] = min(results2)
    dic["TAVG"] = mean(results2)
    dic["TMAX"] = max(results2)
    results3.append(dic)
  
    return jsonify(results3)

if __name__ =="__main__":
    app.run(debug =  True)