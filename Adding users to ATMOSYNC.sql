SHOW GRANTS TO USER DESHMUKHCHAITANYA30;
SHOW GRANTS TO USER HIMABINDURAO3;
SHOW GRANTS TO USER KARTHIGATHIRUPPATHI29;

CREATE ROLE atmosync_dev;

GRANT USAGE ON WAREHOUSE atmosync TO ROLE atmosync_dev; --usage only, can only look, not change

GRANT USAGE ON DATABASE atmosync_db TO ROLE atmosync_dev; --usage only

--privileges on schemas
GRANT ALL PRIVILEGES ON SCHEMA atmosync_db.raw TO ROLE atmosync_dev; 
GRANT ALL PRIVILEGES ON SCHEMA atmosync_db.staging TO ROLE atmosync_dev;
GRANT ALL PRIVILEGES ON SCHEMA atmosync_db.marts TO ROLE atmosync_dev;

--privileges on tables in schemas
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA atmosync_db.raw TO ROLE atmosync_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA atmosync_db.staging TO ROLE atmosync_dev;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA atmosync_db.marts TO ROLE atmosync_dev;

--privileges on future tables in schemas
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA atmosync_db.raw TO ROLE atmosync_dev;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA atmosync_db.staging TO ROLE atmosync_dev;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA atmosync_db.marts TO ROLE atmosync_dev;

--all 3 teammates are sysadmin, so granting this dev role to sysadmin
GRANT ROLE atmosync_dev TO ROLE sysadmin;

--granting the role to each teammate
GRANT ROLE atmosync_dev TO USER DESHMUKHCHAITANYA30;
GRANT ROLE atmosync_dev TO USER HIMABINDURAO3;
GRANT ROLE atmosync_dev TO USER KARTHIGATHIRUPPATHI29;

ALTER USER DESHMUKHCHAITANYA30 SET DEFAULT_ROLE = atmosync_dev;
ALTER USER HIMABINDURAO3 SET DEFAULT_ROLE = atmosync_dev;
ALTER USER KARTHIGATHIRUPPATHI29 SET DEFAULT_ROLE = atmosync_dev;