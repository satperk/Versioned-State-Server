# To start a MongoDB server
docker run -d --rm -p 27017:27017 --name mp8-mongo mongo
# To start your flask application
python3 -m flask run --port 5001