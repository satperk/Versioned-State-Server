from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)


db = {}


# TODO:
# PUT /<key> – Adds a versioned object
@app.route("/<key>", methods=["PUT"])
def PUT_key(key):
	val = request.data.decode("utf-8")
	if key in db.keys():
		db.get(key).append({'val': val})
	else:
		db[key] = [{'val': val}]
	key_index = len(db[key]) - 1
	value = db[key][key_index].get('val')

	return jsonify({'value': value, "version": key_index + 1}), 200


# GET /<key> – Retrieves the latest version of a key
@app.route("/<key>", methods=["GET"])
def GET_key(key):
	if key in db.keys():
		key_index = len(db[key]) - 1
		value = db[key][key_index].get('val')
		return jsonify({'value': value, "version": key_index + 1}), 200
	return "UNABLE TO FIND KEY", 404


# GET /<key>/<version> – Retrieves a specific version of a key
@app.route("/<key>/<version>", methods=["GET"])
def GET_key_version(key,version):
	version_int = int(version)
	if key in db.keys():
		if version_int-1 >= 0 and version_int-1 < len(db[key]):
			value = db[key][version_int-1].get('val')
			return jsonify({'value': value, "version": version_int}), 200
		else:
				return "UNABLE TO FIND VERSION", 404
	return "UNABLE TO FIND KEY", 404

# DELETE /<key> – Completely deletes a key
@app.route("/<key>", methods=["DELETE"])
def DELETE_key(key):
	if key not in db.keys():
		return "KEY DOES NOT EXIST, CANNOT DELETE", 500
	else:
		db.pop(key)
		return key, 200