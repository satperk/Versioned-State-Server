import pytest, sys, requests
import subprocess, time
import random
from pymongo import MongoClient

mongo = MongoClient('localhost', 27017)
db = mongo["mp8-state-server"]
host = "http://127.0.0.1:5001"

@pytest.fixture(scope="session", autouse=True)
def pytest_sessionstart():
    server = subprocess.Popen([sys.executable, "-m", "flask", "run", "--host", "127.0.0.1", "--port", "5001"], cwd="mongodb-nosql")
    time.sleep(2) #wait a bit for the flask server to start
    
    requests.delete(f"{host}/date")
    requests.delete(f"{host}/newKey")
    requests.delete(f"{host}/memory")
    yield
    server.terminate()
    

def test_date_key():
  # == From MP overview ==
  r = requests.put(f"{host}/date", "2020-11-05")
  assert( r.status_code == 200 ), r

  r = requests.put(f"{host}/date", "2020-11-12")
  assert( r.status_code == 200 ), r

  r = requests.get(f"{host}/date")
  assert( r.status_code == 200 ), r
  response = r.json()
  assert( response["version"] == 2 ), response
  assert( response["value"] == "2020-11-12" ), response

  r = requests.get(f"{host}/date/1")
  assert( r.status_code == 200 ), r

  response = r.json()
  assert( response["version"] == 1 ), r
  assert( response["value"] == "2020-11-05" ), r

  r = requests.get(f"{host}/date/3")
  assert( r.status_code == 404 or r.status_code == 400 ), r

  ## Require atleast a collection in the db name.
  assert(len(db.list_collection_names()) >= 1)

def test_memory():
  # == Test memory ==
  num_requests = 100
  for i in range(1, num_requests):
    r = requests.put(f"{host}/memory", f"data{i}")

  randomOrder = list(range(1, num_requests))
  random.shuffle(randomOrder)
  for i in randomOrder:
    r = requests.get(f"{host}/memory/{i}")
    assert( r.status_code == 200 ), r
    
    response = r.json()
    assert( response["version"] == i ), r
    assert( response["value"] == f"data{i}" ), r

  ## Require atleast a collection in the db name.
  assert(len(db.list_collection_names()) >= 1)

def test_newKey():
  # == Test a `newKey` ==
  r = requests.get(f"{host}/newKey")
  assert( r.status_code == 404 or r.status_code == 400), r

  r = requests.put(f"{host}/newKey", "Hi")
  assert( r.status_code == 200 ), r

  r = requests.get(f"{host}/newKey")

  response = r.json()
  assert( r.status_code == 200 ), r
  assert( response["version"] == 1 ), r
  assert( response["value"] == "Hi" ), r

  # == DELETE ==
  r = requests.delete(f"{host}/newKey")
  assert( r.status_code == 200 ), r

  r = requests.get(f"{host}/newKey")
  assert( r.status_code == 404 or r.status_code == 400), r

  r = requests.put(f"{host}/newKey", "Hi")
  assert( r.status_code == 200 ), r

  r = requests.get(f"{host}/newKey")
  assert( r.status_code == 200 ), r
  response = r.json()
  assert( response["version"] == 1 ), r
  assert( response["value"] == "Hi" ), r

  ## Require atleast a collection in the db name.
  assert(len(db.list_collection_names()) >= 1)
