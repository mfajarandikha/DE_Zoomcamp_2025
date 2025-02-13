# DE_Zoomcamp_2025
### Homework Module 3

# Create Extranal Table
```sh
CREATE EXTERNAL TABLE `fiery-catwalk-440706-k8.taxi_project.external_table`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://fiery-catwalk-440706-k8-bqtemp/yellow_tripdata_2024-01.parquet', 
          'gs://fiery-catwalk-440706-k8-bqtemp/yellow_tripdata_2024-02.parquet',
          'gs://fiery-catwalk-440706-k8-bqtemp/yellow_tripdata_2024-03.parquet',
          'gs://fiery-catwalk-440706-k8-bqtemp/yellow_tripdata_2024-04.parquet',
          'gs://fiery-catwalk-440706-k8-bqtemp/yellow_tripdata_2024-05.parquet',
          'gs://fiery-catwalk-440706-k8-bqtemp/yellow_tripdata_2024-06.parquet']
);
```

# Create Regular Table
```sh
CREATE TABLE `fiery-catwalk-440706-k8.taxi_project.regular_table` AS
SELECT *
FROM `fiery-catwalk-440706-k8.taxi_project.external_table`;
```

1. Count Rows
```sh
SELECT COUNT(*) FROM
FROM `fiery-catwalk-440706-k8.taxi_project.external_table`;
```

2. Estimated Amount of data
```sh
SELECT
  COUNT(DISTINCT PULocationID)
FROM `fiery-catwalk-440706-k8.taxi_project.external_table`;

AND

SELECT
  COUNT(DISTINCT PULocationID)
FROM `fiery-catwalk-440706-k8.taxi_project.regular_table`;
```

3. Records have a fare_amount of 0
```sh
SELECT COUNT(*) AS num_records_with_zero_fare
FROM `fiery-catwalk-440706-k8.taxi_project.regular_table`
WHERE fare_amount = 0;
```

# Create partition table
```sh
CREATE OR REPLACE TABLE `fiery-catwalk-440706-k8`.`taxi_project`.`optimized`
PARTITION BY DATE(tpep_dropoff_datetime)  
CLUSTER BY VendorID  
AS
SELECT * FROM `fiery-catwalk-440706-k8`.`taxi_project`.`regular_table`
```

4.  Estimated processed bytes before and after partitioned
```sh
SELECT DISTINCT VendorID FROM `fiery-catwalk-440706-k8.taxi_project.optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

AND

SELECT DISTINCT VendorID FROM `fiery-catwalk-440706-k8.taxi_project.regular_table`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
