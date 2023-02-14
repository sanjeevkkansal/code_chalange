import pandas as pd
import os
import glob
import sqlite3 as db
import logging
import sys
import time

from src.xconfig import DefaultConfig as config

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("import_data")

db_context = db.connect(config.DATABASE_PATH)
db_cursor = db_context.cursor()


class ImportData:

    def create_tables(self):
        logger.info("Creating Table")
        wx_data_table = """
        CREATE TABLE IF NOT EXISTS wx_data(
        wx_date int,
        wx_year int,
        wx_month int,
        wx_day int,
        wx_station varchar(11),
        temp_max int,
        temp_min int,
        precipitation int,
        UNIQUE (wx_date, wx_station) ON CONFLICT IGNORE )
        """

        corn_yield_table = """
        CREATE TABLE IF NOT EXISTS corn_yield(
        yld_year int,
        yield int,
        UNIQUE (yld_year) ON CONFLICT IGNORE )
        """

        wx_avg_data_yearly_table = """
        CREATE TABLE IF NOT EXISTS wx_avg_data_yearly (
        wx_station TEXT,
        wx_year INTEGER,
        temp_max_avg_yearly REAL,
        temp_min_avg_yearly REAL,
        precipitation_avg_yearly REAL)
        """
        db_cursor.execute(wx_data_table)
        db_cursor.execute(corn_yield_table)
        db_cursor.execute(wx_avg_data_yearly_table)

    def import_weather_data(self):
        start_time = time.time()
        wx_total_rows = 0
        wx_added_rows = 0
        data_files = glob.glob(os.path.join(config.WX_DATA_FOLDER, "*.txt"))
        logger.info(f"Weather data total files: {len(data_files)}")
        count = 0
        total_files = len(data_files)
        for f in data_files:
            count += 1
            logger.info(f"Processing {count} of total weather files: {total_files}")
            # read the csv file
            df = pd.read_csv(f, sep='\t', engine='python', header=None)
            df.columns = ['wx_date', 'temp_max', 'temp_min', 'precipitation']
            df["wx_station"] = os.path.basename(f)[:-4]
            df["wx_year"] = df["wx_date"].apply(lambda r: int(str(r)[:4]))
            df["wx_month"] = df["wx_date"].apply(lambda r: int(str(r)[4:-2]))
            df["wx_day"] = df["wx_date"].apply(lambda r: int(str(r)[-2:]))
            df["temp_max"] = df["temp_max"].replace(-9999, None)
            df["temp_min"] = df["temp_min"].replace(-9999, None)
            df["precipitation"] = df["precipitation"].replace(-9999, None)
            inserted_rows = df.to_sql(name='wx_data', con=db_context, if_exists='append', index=False)
            total_rows = df[df.columns[0]].count()
            wx_total_rows += total_rows
            wx_added_rows += inserted_rows
            # logger.info(f"Added {inserted_rows} of {total_rows} rows")
        logger.info(f"Total added {wx_added_rows} of {wx_total_rows} rows")
        logger.info("--- To ingest weather data it took %s seconds ---" % (time.time() - start_time))

    def import_yield_data(self):
        path = config.YLD_DATA_FILE
        # read the csv file
        df = pd.read_csv(path, sep='\t', engine='python', header=None)
        df.columns = ['yld_year', 'yield']
        inserted_rows = df.to_sql(name='corn_yield', con=db_context, if_exists='append', index=False)
        total_rows = df[df.columns[0]].count()
        logger.info(f"Added {inserted_rows} of {total_rows} rows")
        # print(df)

    def import_avg_data(self):
        df = pd.read_sql_query("select wx_station, wx_year, AVG(temp_max) as temp_max_avg_yearly, "
                               "AVG(temp_min) as temp_min_avg_yearly, AVG(precipitation) as precipitation_avg_yearly "
                               "from wx_data group by wx_station, wx_year", con=db_context)
        total_rows = df[df.columns[0]].count()
        inserted_rows = df.to_sql(name='wx_avg_data_yearly', con=db_context, if_exists='replace', index=False)
        logger.info(f"Added {inserted_rows} of {total_rows} rows in wx_yearly_avg_data")


if __name__ == '__main__':
    import_data = ImportData()
    import_data.create_tables()
    import_data.import_weather_data()
    import_data.import_yield_data()
    import_data.import_avg_data()
