# To install dependencies
apt-get -y update;
apt-get -y install python3-pip;
python3 -m pip install flask;
python3 -m pip install python-dotenv;
python3 -m pip install requests;
pip install pytest;
echo finished with install dependencies;
# Alternatively, you can do
pip install -r requirements.txt
