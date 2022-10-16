# moneyChatBot
A money chat bot that keep track of expenses
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## **General info** 
Money chat bot created to help users keep track on money.
Each transaction been save to database and the user can export the data to Excel file


## **Technologies** 
The project created with:
* python 3.9
* flask
* postgresSQl 
* telegram bot 

## **Setup**
***Make sure you have python and virtualenv in your computer.***


In the project  directory run:  
Linux \ MacOS:
```
$ virtualenv venv && source venv/bin/activate && pip install -r requirements.txt
```
Windows:
```
$ virtualenv venv && venv\Scripts\activate && pip install -r requirements.txt
```

Create .env file as following:
**Replace Value with the real value**

```
PSQL_KEY=Value
API_KEY=Value
TELEGRAM_ID=Value
```

Navigate to project folder and run:
```
$ python run.py
```

#### Keep in mind:
backup.sql file can use to create a database with appropriate values and columns.

**Do not forget to add TELEGRAM_ID value to authorized_users.txt file**