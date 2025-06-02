### Overview
This project demonstrates a complete data engineering workflow to ingest, process, and analyze structured cricket match data, including every ball bowled and match outcomes. The pipeline is designed to handle granular delivery-level data for both teams and supports exploratory analysis to uncover key trends and performance metrics. It showcases skills in data ingestion, transformation, and analytical reporting using modern data engineering tools.
### Stages of data ingestion pipeline:
1. Downloading the json files for all One-Day Internationals from [here](https://cricsheet.org/downloads/) to `cricket-analytics/data/`
2. Creating the following tables (if not exists) in SQLite. The structure of the tables can be viewed in `cricket-analytics/configs/DDL.py` 
    * `match_results` - This table stores all the ODI match results.
    * `match_ball_by_ball` - This table stores ball-by-ball innings data for all the ODI matches.
    * `player_universe` - This table stores the universe of players, along with their unique identifier in registry, across all ODI matches.
3. Inserting data from the downloaded json files in `cricket-analytics/data/` folder to the 3 tables mentioned in step 2.

### Steps to run the code:
 
- Open terminal and navigate to the python project `cricket-analytics`
- Create a database file `cricket-analytics-sqlite.db` for SQLite. Please use the command
```commandline
touch cricket-analytics-sqlite.db
```
- Create a virtual environment. Please use the command
```commandline
python -m venv venv
```
- Activate the virtual environment. Please use the command
```commandline
source venv/bin/activate
```
- Install the requirements in the `requirements.txt` file. Please use the command
```commandline
pip install -r requirements.txt
```
- Execute the `main.py` file. Please use the command
```commandline
python main.py
```
- Logs will start appearing in the file `output.log`. Please check this file while the pipeline is running, to verify if the code is running fine. Open a new terminal, navigate to the project `cricket-analytics`. After that please use the command
```commandline
tail -f -n10 output.log
```

### Notes -
- About the log file:
   - The file `output.log` file will contain all the logs.
   - We are keeping a history of the json filename and the corresponding `match_type` and `match_type_number`. This can be useful if we are seeing anomalies in data after loading it into database. We can search the `output.log` file for the specific match and reference its json file.
- As every json file is parsed and data is uploaded to the SQLite tables, the file is deleted from the `cricket-analytics/data/` folder. This can be avoided if we don't want to delete the json files. For example, we can upload the files to cold storage.


### Steps to query uploaded data in SQLite:
- Once the pipeline has run successfully, we have to open terminal and navigate to the python project `cricket-analytics`
- Connect to SQLite using `cricket-analytics-sqlite.db`. Please use the command
```commandline
sqlite3 cricket-analytics-sqlite.db
```
- The following command should show the table names `match_results`, `match_ball_by_ball`, `player_universe`
```commandline
.tables
```
- Use the following command to get headers along with the result of a query we execute.
```commandline
.headers on
```
- We can now execute queries on the data to see the output on the terminal.
```commandline
select * from match_results limit 10;
```

### SQL Insights:
- The win records (percentage win and total wins) for each team by year and gender, excluding ties,
matches with no result, and matches decided by the DLS method in the event that, for whatever
reason, the planned innings can’t be completed.
- Which male and female teams had the highest win percentages in 2019?
- Which players had the highest strike rate as batsmen in 2019? (Note to receive full credit, you
need to account for handling extras properly.)

The queries are present as `.sql` files in the folder `cricket-analytics/SQL/` 
