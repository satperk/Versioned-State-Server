import pytest, sys
import requests
import subprocess, time
import random

host = "http://127.0.0.1:5000"

@pytest.fixture(scope="session", autouse=True)
def pytest_sessionstart():
  server = subprocess.Popen([sys.executable, "-m", "flask", "run", "--host", "127.0.0.1", "--port", "5000"], cwd="local-store")
  time.sleep(2) #wait a bit for the flask server to start
  requests.delete(f"{host}/date")
  requests.delete(f"{host}/newKey")
  requests.delete(f"{host}/memory")
  yield
  server.terminate()


def test_date_key():
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


def test_bad_date_key():
  r = requests.get(f"{host}/date/3")
  assert( r.status_code == 404 or r.status_code == 400), r


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


def test_newKey():
  # == Test a `newKey` ==
  r = requests.get(f"{host}/newKey")
  assert( r.status_code == 404 or r.status_code == 400), r

  r = requests.put(f"{host}/newKey", "Hi")
  assert( r.status_code == 200 ), r

  r = requests.get(f"{host}/newKey")
  assert( r.status_code == 200 ), r
  response = r.json()
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
