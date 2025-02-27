SELECT 
    *,
    TIMESTAMP_SECONDS(CAST(pickup_datetime AS INT64)) AS pickup_ts,
    TIMESTAMP_SECONDS(CAST(dropoff_datetime AS INT64)) AS dropoff_ts
FROM {{ source('raw_nyc_tripdata', 'ext_green_taxi') }}
