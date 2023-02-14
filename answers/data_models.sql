-- For data modeling providing DDL. For wx_data adding year, month and day in table to make sure
-- query can be used on those fields. We could get these from wx_date but manipulation might take some computing.
-- Here computing v/s storage I felt storage is cheaper option.

-- wx_data definition

CREATE TABLE wx_data(
wx_date int,
wx_year int,
wx_month int,
wx_day int,
wx_station varchar(11),
temp_max int,
temp_min int,
precipitation int,
UNIQUE (wx_date, wx_station) ON CONFLICT IGNORE );

-- corn_yield definition

CREATE TABLE corn_yield(
yld_year int,
yield int,
UNIQUE (yld_year) ON CONFLICT IGNORE );


-- wx_data_avg_yearly definition

CREATE TABLE wx_avg_data_yearly (
wx_station TEXT,
wx_year INTEGER,
temp_max_avg_yearly REAL,
temp_min_avg_yearly REAL,
precipitation_avg_yearly REAL);