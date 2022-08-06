# python-sample-app
Basic application developed in python, sql alchemy and nginx to use in all labs and POCs involving docker, container, kubernetes, aws, etc. 

I'm sure there must be things to improve in the application, but as I'm not a dev, it's great :sweat_smile: **Feel free to suggest improvements**

With this application you will understand some **Python** :snake: and **Docker** :whale2: concepts:

* API
* Loggers
* Python and databse with SQLAlchemy to facilitate the process
* Debug logs with python
* Docker compose
* Container networks
* Communication between containers
* Docker Secrets
* Docker Volumes

## The following dependencies were used to run the application:

In some cases you may get an error installing the mysqlclient dependency, so run the following command before running requirements:
```sh
sudo apt-get install -y python3.7-dev
```

* Flask==2.1.0
* Flask-SQLAlchemy==2.4.4
* flask_mysqldb==0.2.0
* SQLAlchemy<1.4
* debugpy==1.2.1
* werkzeug== 2.0.3

Run this command to install the dependencies:
```sh
sudo pip install -r character-service/requirements.txt 
```

## The application runs 3 containers configured with dockerfile:

* **nginx:** Web server to call backend
* **character-service:** Backend with all logic process
* **db:** basic config of database

To run an application with multiple containers, use docker compose as shown below:
```sh
sudo docker compose build
sudo docker compose up -d
```
Run this command to stop all containers:
```sh
sudo docker compose down
```
## Test the application:

Import the postman collection in "postman" folder and run the requests to validate CRUD operations
