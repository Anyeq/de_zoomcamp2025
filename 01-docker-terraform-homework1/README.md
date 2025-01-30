# Modul 1 Homework: Docker & SQL

## Question 1: Understanding docker first run
What's the version of 'pip' int the image?
Access Docker:
`sudo docker run -it --entrypoint bash python:3.12.8`
Checking python version inside image:
`pip --version`

## Question 3: Trip Segmentation Count
```
SELECT 
COUNT(CASE WHEN trip_distance <= 1 THEN 1 END) as Upto1mile, 
COUNT(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 END) as from1to3,
COUNT(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 END) as from3to7,
COUNT(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 END) as from7to10,
COUNT(CASE WHEN trip_distance > 10 THEN 1 END) as More10
FROM public.green_taxi_trips102019
```

## Question 4: Longest Trip for Each day
```
SELECT DATE(lpep_pickup_datetime), MAX(trip_distance) as max_distance
FROM public.green_taxi_trips102019
WHERE lpep_pickup_datetime::date IN ('2019-10-11', '2019-10-24', '2019-10-26', '2019-10-31')
GROUP BY DATE(lpep_pickup_datetime)
```

## Question 5: Three biggest pickup zones
```
SELECT 
DATE(lpep_pickup_datetime) AS date,
SUM(total_amount) AS total_amount,
"PULocationID" AS loc_id
FROM public.green_taxi_trips102019
WHERE DATE(lpep_pickup_datetime)='2019-10-18'
GROUP BY date, loc_id
ORDER BY total_amount DESC
LIMIT 3
```

## Question 6: Largest Tip
```
SELECT 
subquery."Zone",
subquery.max_tip_amount
FROM (
	SELECT
	tzlook."Zone",
	MAX(gtdata.tip_amount) AS max_tip_amount
	FROM public.green_taxi_trips102019 gtdata
	INNER JOIN taxi_zone_lookup tzlook ON gtdata."DOLocationID"=tzlook."LocationID"
	WHERE gtdata."PULocationID"=74
	GROUP BY tzlook."Zone"
) AS subquery
ORDER BY subquery.max_tip_amount DESC
LIMIT 1
```
