CREATE OR REPLACE DATABASE ATMOSYNC_DB;

USE ATMOSYNC_DB;

CREATE OR REPLACE SCHEMA atmosync_db.raw;      -- landing zone for raw CSV loads
CREATE OR REPLACE SCHEMA atmosync_db.staging;  -- dbt staging + transformation models
CREATE OR REPLACE SCHEMA atmosync_db.marts;    -- final, business-ready tables for PowerBI

CREATE TABLE atmosync_db.raw.container_telemetry (
    event_timestamp   TIMESTAMP_NTZ(0),
    container_id      VARCHAR(20),
    shipment_id       VARCHAR(20),
    commodity         VARCHAR(50),
    origin            VARCHAR(50),
    destination       VARCHAR(50),
    latitude          NUMBER(9,6),
    longitude         NUMBER(9,6),
    temperature        NUMBER(5,2),
    humidity          NUMBER(5,2),
    vibration         NUMBER(6,3),
    pressure          NUMBER(8,2),
    battery_level     NUMBER(5,2),
    door_status       VARCHAR(10),
    light_detected    BOOLEAN,
    gps_speed         NUMBER(6,2),
    spoilage_index    NUMBER(5,2),
    sensor_status     VARCHAR(20),
    alert_level       VARCHAR(20)
);

CREATE OR REPLACE FILE FORMAT csv_container_telemetry
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    TIMESTAMP_FORMAT = 'DD-MM-YYYY HH24:MI:SS'
    NULL_IF = ('', 'NULL')
    EMPTY_FIELD_AS_NULL = TRUE;

select * from atmosync_db.raw.container_telemetry;

//Tried loading the data directly by uploading the csv, but facing issues with timestamp column.
//Hence going for the staging + load approach

CREATE OR REPLACE STAGE atmosync_db.raw.telemetry_stage; --creating staging place for temporary staging of data

//Added the csv file into the stage - telemetry stage using Ingestion -> Add data ->Load files into a stage
//Querying the stage table to see the uploaded file
//Snowflake allows querying staging tables as well, syntax is different though

LIST @atmosync_db.raw.telemetry_stage;

SHOW FILE FORMATS IN DATABASE atmosync_db;

SELECT $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19
FROM @atmosync_db.raw.telemetry_stage/container_telemetry_2.csv
(FILE_FORMAT => 'atmosync_db.raw.csv_container_telemetry') //specify the file format we've created above
LIMIT 10;

//copy the data from staging(atmosync_db.raw.telemetry_stage) to actual table(atmosync_db.raw.container_telemetry)
COPY INTO atmosync_db.raw.container_telemetry
FROM @atmosync_db.raw.telemetry_stage/container_telemetry_2.csv
FILE_FORMAT = (FORMAT_NAME = 'atmosync_db.raw.csv_container_telemetry')
ON_ERROR = 'CONTINUE';

select * from atmosync_db.raw.container_telemetry;