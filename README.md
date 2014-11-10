Currently there is no fabric script for automatic deployment, so here is the
manual step by step process to setup the Project.

Below steps was tested on ubuntu 14.04 LTS.

Install Packages: -

    $ sudo apt-get update
    $ sudo apt-get upgrade -y
    $ sudo apt-get build-dep python-dev python-psycopg2 python-lxml python-gevent python-m2crypto python-celery
    $ sudo apt-get install build-essential python-dev
    $ sudo apt-get install python-pip screen git vim nginx supervisor
    $ sudo apt-get install python-psycopg2
    $ sudo pip install -U virtualenvwrapper

For Postgresql Installation:

    $ echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
    $ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    $ sudo apt-get update
    $ sudo apt-get install postgresql-9.3 postgresql-server-dev-9.3 postgresql-contrib -y
    $ sudo vim /etc/postgresql/9.3/main/pg_hba.conf (replace `peer` with `trust`)
    $ sudo service postgresql reload

For RabbitMQ Server Installations:

    Add the following line to your `/etc/apt/sources.list`:
        `deb http://www.rabbitmq.com/debian/ testing main`
    $ wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
    $ sudo apt-key add rabbitmq-signing-key-public.asc
    $ sudo apt-get update
    $ sudo apt-get install rabbitmq-server -y

For virtualenvwrapper installation : -

    $ sudo pip install -U virtualenvwrapper
    $ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
    $ source ~/.bashrc

Make virtualenv : -

    $ mkvirtualenv mobilevault

Install nodejs: -

    $ sudo add-apt-repository ppa:chris-lea/node.js
    $ sudo apt-get update
    $ sudo aptitude purge npm nodejs
    $ sudo apt-get install nodejs -y
    $ sudo npm install -g bower

Clone repo: -

    $ cd ; mkdir -p codebase; cd codebase
    $ git clone https://github.com/mobile-vault/mv-server.git
    $ cd mv-server; git submodule init && git submodule update
    $ mkdir assets/android
    $ mkdir assets/ios

Install requirements: -

    $ pip install -r requirements/requirement.txt
    $ cd media; bower install

Set window.debug = false in index.py

    $ vim ~/codebase/mv-server/media/app/index.html

Symlink Project Directory: -

    $ cd /opt
    $ sudo mkdir -p toppatch/mv
    $ sudo ln -s /home/ubuntu/codebase/mv-server /opt/toppatch/mv/backend
    $ sudo ln -s /home/ubuntu/codebase/mv-server/media /opt/toppatch/mv/media
    $ sudo ls -s /home/ubuntu/codebase/mv-server/assets /opt/toppatch/assets

Setup database : -

    $ sudo -u postgres createuser --superuser ubuntu
    $ sudo -u postgres psql postgres: \password ubuntu
    $ sudo -u postgres createdb -O ubuntu mobilevault
    $ psql mobilevault < ~/codebase/mv-server/db/assets/ddl/install.sql

Initialize DB with default admin values. Goto Db shell using : -

    $ psql mobilevault

then run following commands in db shell: -

    > insert into companies (name, email, address, contact) values ('EFF', 'admin@eff.org', '1984', 'APPLE HQ');

    > update companies set deleted=false where id=1;

    ## Below password hash is for password `George Orwell`
    > insert into logins (password, deleted) values ('DggBEDpcLtW+oJATrIT0VbxvfHJeyIAoDv/R17n7fKeXehKk', false);

    > insert into admin_profile (company_id, email, login_id, name, deleted)  values (1, 'admin@eff.org', 1, 'snowden', false);

Add config parameters accordingly: -

    $ vim ~/codebase/mv-server/config.py

Copy SSL cert to /etc/ssl directory : -

    $ sudo mv star_war_com.pem /etc/ssl/
    $ sudo mv star_war_com.key /etc/ssl/

Add supervisor conf for celery deamon and mobilevault : -

    $ sudo vim /etc/supervisor/conf.d/celeryd.conf
    $ sudo supervisorctl reread
    $ sudo supervisorctl update
    $ sudo supervisorctl restart celery

    $ sudo vim /etc/supervisor/conf.d/mobilevault.conf
    $ sudo supervisorctl reread demo_mdm:\*
    $ sudo supervisorctl update demo_mdm:\*

Create Logger directory:

    $ cd /var/log
    $ sudo mkdir -p celery
    $ sudo mkdir -p /var/log/mobilevault

Add logrotate conf for celery and mobilevault log: -

    $ sudo vim /etc/logrotate.d/mobilevault
    $ sudo vim /etc/logrotate.d/celery

Place Android APK to assets/android : -

    $ copy MobileVaultAgent.apk ~/codebase/mv-server/assets/android/

For iOS assets like PushCert, Private CSR certificate and sample xml config files, go through the documentation added at [mobile-vault](http://mobile-vault.org/ios-keys-and-agent-installation/)

SetUp Nginx server: -

    $ sudo rm /etc/nginx/sites-enabled/default
    $ sudo vim /etc/nginx/sites-available/mobilevault.conf
    $ sudo ln -s /etc/nginx/sites-available/mobilevault.conf /etc/nginx/sites-enabled/mobilevault.conf
    $ sudo nginx -t
    $ sudo service nginx restart
