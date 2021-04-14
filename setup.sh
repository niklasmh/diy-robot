# Make sure the raspberry pi has everything set up correctly
pip3 install -r requirements.txt

sudo apt install ufw libatlas-base-dev -y

sudo ufw enable
sudo ufw allow 5000
