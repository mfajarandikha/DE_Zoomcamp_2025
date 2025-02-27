SELECT 
    taxi_type,
    pickup_ts,
    dropoff_ts,
    trip_distance,
    total_amount,
    pickup_location_id,
    dropoff_location_id
FROM {{ ref('stg_green_taxi') }}

UNION ALL

SELECT 
    taxi_type,
    pickup_ts,
    dropoff_ts,
    trip_distance,
    total_amount,
    pickup_location_id,
    dropoff_location_id
FROM {{ ref('stg_yellow_taxi') }}
