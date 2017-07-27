## Bucketlist API

### Overview

A bucketlist defined as a list of things a person would like to accomplish during their lifetime.

The bucketlist API is a RESTful API thatprovides various endpoints that make it easy to perform CRUD operations on 
bucketlists as well as their 
constituent bucketlist items.

#### Language
This API is written in `Python 3.6` making use of the Flask Micro-framework and Flask Restplus. It's documentation is 
done using Swagger UI. 

#### Database
We shall be using `Postgres` for storage of all the app data

### Installation and Setup
1. Clone the repository from Github
```commandline
$ git clone https://github.com/edmondatto/CP2-Bucketlist
```
2. Cd into the working directory
```commandline
$ cd CP2-Bucketlist
```
3. Create a virtual environment and activate it. If you don't have virtualenv, install it using `pip install virtualenv` 
then run the commands below.
```commandline
$ virtualenv bucketlist
$ source bucketlist/bin/activate
```
4. Install the applications dependencies
```commandline
$ pip install -r requirements.txt
```

#### Database setup
If you don't already have Postgres installed, set it up on your machine (globally) by running the command below
```commandline
$ brew install potgresql
```
Let's get started setting up your database
1. Start Postgres
```commandline
$ psql postgres
```
2. Create the database
```commandline
# CREATE DATABASE flask_api;
# CREATE DATABSE test_db;
\q
```
Alternatively, run the following in your commandline
```commandline
$ createdb flask_api
$ createdb test_db
```

#### Run Database migrations
```commandline
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

You're all setup now, run the application using the command below
```commandline
$ flask run
```
If everything is working, you should get the output below after running the command
```commandline
 * Serving Flask app "run"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Supported Endpoints


| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/auth/register/` | `POST`  | Register a new user|
|  `/auth/login/` | `POST` | Login and retrieve token|
| `/bucketlists/` | `POST` | Create a new Bucketlist |
| `/bucketlists/` | `GET` | Retrieve all bucketlists for user |
| `/bucketlists/?page=1&per_page=3/` | `GET` | Retrieve three bucketlists per page |
 `/bucketlists/?q=name/` | `GET` | searches a bucketlist by the name|
| `/bucketlists/<id>/` | `GET` |  Retrieve a bucketlist by ID|
| `/bucketlists/<id>/` | `PUT` | Update a bucketlist |
| `/bucketlists/<id>/` | `DELETE` | Delete a bucketlist |
| `/bucketlists/<id>/items/` | `POST` |  Create items in a bucketlist |
| `/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete an item in a bucketlist|
| `/bucketlists/<id>/items/<item_id>/` | `PUT`| update a bucketlist item details|

### Running tests
```commandline
python manage.py test
```