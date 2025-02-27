# DE_Zoomcamp_2025
### Week 4 Homework

Create External Table in BigQuery
```sh
CREATE OR REPLACE EXTERNAL TABLE `myproject.raw_nyc_tripdata.ext_green_taxi`
OPTIONS (
  format = 'CSV',
  uris = ['gs://my-bucket/nyc-taxi-data/green_tripdata_*.csv.gz']
);

```

Taxi Quarterly Revenue Growth
```sh
SELECT 
    service_type, 
    EXTRACT(YEAR FROM pickup_ts) AS year,
    CONCAT(EXTRACT(YEAR FROM pickup_ts), '/Q', EXTRACT(QUARTER FROM pickup_ts)) AS year_quarter,
    SUM(total_amount) AS revenue
FROM {{ ref('fact_taxi_trips') }}
GROUP BY 1, 2, 3

```