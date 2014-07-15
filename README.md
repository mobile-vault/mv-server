<b>Dependencies</b>:
sudo apt-get build-dep python-dev python-psycopg2 python-lxml
sudo apt-get install build-essential python-dev
sudo apt-get install python-pip
su -s
echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
sudo apt-get install postgresql-9.3
sudo apt-get install pgadmin3
sudo apt-get install python-psycopg2
sudo pip install -U virtualenvwrapper

mkvirtualenv mobilevault
pip install -r requirement.txt
