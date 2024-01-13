from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)
from pymongo import MongoClient
mongo = MongoClient('localhost', 27017)
db = mongo["mp8-state-server"]


# TODO:
# PUT /<key> – Adds a versioned object
@app.route("/<key>", methods=["PUT"])
def PUT_key(key):
    if key in db.list_collection_names():
        for key_version in db[key].find().sort("version", -1):
            record = {"value" : request.data.decode("utf-8"),"version" : key_version["version"] + 1}
            db[key].insert_one(record)
            return "KEY IS UPDATED", 200  
    else:
        record = {"value" : request.data.decode("utf-8"), "version" : 1}
        db[key].insert_one(record)
        return "KEY IS ADDED", 200
    
    return "ERROR, UNABLE TO ADD KEY", 500

# GET /<key> – Retrieves the latest version of a key
@app.route("/<key>", methods=["GET"])
def GET_key(key):
    for key_version in db[key].find({},{"_id":0}).sort("version", -1):
        return jsonify(key_version), 200
    return "ERROR, UNABLE TO LOCATE KEY VERSION", 404


		
# GET /<key>/<version> – Retrieves a specific version of a key
@app.route("/<key>/<version>", methods=["GET"])
def GET_key_version(key,version):
    for key_version in db[key].find({},{"_id":0}).sort("version", -1):
        if key_version.get('version') == int(version):
            return jsonify(key_version), 200
    return "ERROR, UNABLE TO LOCATE KEY VERSION", 404


# DELETE /<key> – Completely deletes a key
@app.route("/<key>", methods=["DELETE"])
def DELETE_key(key):
    if (db[key] != None):
        db[key].drop()
        return "KEY WAS DROPPED",200
    return "ERROR, CANNONT DELETE NONEXISTENT KEY", 404
