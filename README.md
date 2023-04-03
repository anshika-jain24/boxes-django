# boxes-django

## Installation
These were my python configs at the time of making this project:
```
python version: 3.9.6
pip version: 21.1.3
```
Clone this repo and run the following commands on your terminal:
```
$ pip install -r requirements.txt
$ python3 manage.py runserver
```
If the server does not start, try the following commands:
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```

If the server still does not start, google your error :)

### Login Credentials for user:
After your server starts, visit ```localhost:8000/admin``` and use the following credentials to checkout the database
```
username: test
password: spinny
```

```
username: test2
password: spinny
```

test is a staff user and has staff access and test2 is a non-staff user. So to check the staff and non-staff functionalities, you can use these credentials.

## About the Database:

The 'User' db is taken directly from django.contrib.auth

The 'Box' db has the following fields:
1. ```length```    : float; stores the length of the box
2. ```breadth```   : float; stores the length of the box
3. ```height```   : float; stores the length of the box
4. ```area```  : float; stores the length of the box
5. ```volume```   : float; stores the length of the box
6. ```created_by``` : string; stores the username of the user
7. ```created_at``` : DateTime; stores the date and time at which the box is created
8. ```last_updated``` : DateTime; stores the date and time at which the box is last updated

## About the APIs:
There are in total 6 apis in this project.

Note - To check the APIs, you need to provide the Auth credentials in the authentication. Choose basic auth and add username and password of the user

1. GET | (all)<br />
   ```http://127.0.0.1:8000/boxes/list```<br />
Expects: Auth credentials(username and password) and the filters in the body in following format<br />
```
height_more_than     (str)
length_more_than       (str)
```
Other filters can be added in following format
Response: Lists all the boxes in the database<br />
2. GET | (all boxes created by that user)<br />
```http://127.0.0.1:8000/boxes/my-boxes```<br />
Expects: Auth credentials(username and password) and the filters in the body according to which you want to filter the boxes
```
height_more_than     (str)
length_more_than       (str)
```
Response: Displays the details of the boxes created by that user
3. POST | (add a new box)<br />
```http://127.0.0.1:8000/boxes/create```<br />
Expects: The following fields in the body of the api request:
```
length      (str)
breadth      (str)
height       (str)
```
Response: Returns success after the box is added
4. PUT | (updates the box with the given id)<br />
```http://127.0.0.1:8000/boxes/update/<id>```<br />
Expects: The following fields in the body of the api request:
```
length      (str)
breadth      (str)
height       (str)
```
Response: Returns success after updating the box
5. DELETE | (delete the box with the given id)<br />
```http://12.0.0.1:8000/delete/<id>```<br />
Expects: Auth credentials
Response: Returns success if the delete is successful
7. POST | (Register a user)<br />
```http://127.0.0.1:8000/boxes/register```<br />
Expects: The following fields in the body of the api request:
```
username      (str)
email       (str)
password       (str)
```
Response: Returns success, if the creation was succesfull. 
<b>You can test the above mentioned APIs in Postman or anywhere you like! :) </b>


## Made By: 
Anshika Jain<br />
Delhi Technological University (DTU)<br />
