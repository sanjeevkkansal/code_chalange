# Code Challenge answers

---

To run the python scripts need python3. Below are steps to setup virtual environment and activate.

```
python3 -m venv venv
source venv/bin/activate
pip install -r Requirements.txt
```
This can also be run inside docker.

---

Answer 1 - Data Modeling 

--------

For this coding exercise I used SQLite as this is easy to setup and does not require external DB setup. in `answers` folder there are 3 DDL statements.

---
Answer 2 - Ingestion

---------------------

Script `import_data.py` under `src` folder has all required code to ingest data. Configuration are setup as environment variables and can be changed in `config.env`. File `xconfig.py` is using environment variables to setup default configuration.

First change to folder to `src` and run following command.

`python3 import_data.py` 

---

Answer 3 - Data Analysis

-------------------------

Data Models are setup as DDL in `answers` folder. Used SQL for calculation. 

---
Answer 4 - REST API

--------------------

Created API using Flask framework. To run API use follwoing command.

`python3 flask_api.py` 

It is using plain SQL script to get data from DB, but we can use ORM like SQLAlchemy.

for testing API below curls can be used.

get weather data:

```
curl --location --request GET 'http://127.0.0.1:5000/api/weather?wx_date=19850101&wx_station=USC00110072&page=2&count_per_page=5'
```

get yield data:

```
curl --location --request GET 'http://127.0.0.1:5000/api/yield?yld_year=1985&page=1&count_per_page=5'
```

get weather stats data:

```
curl --location --request GET 'http://127.0.0.1:5000/api/weather/stats?wx_year=1985&wx_station=USC00110072&page=1&count_per_page=5'
```
