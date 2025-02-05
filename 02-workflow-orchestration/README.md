# Module 2 Homework: Workflow Orchestration

To run Kestra Container. Run it on main folder (02-workflow-orchestrarion)
type : `sudo docker compose up'

To run Standalon Postgres container, run it on postgres_db folder
type : `sudo docker compose up'

To Connect pgadmin to standalone postgres container
type:
```
sudo docker run -it --rm -p 8000:80 --name=pgadmin -e "PGADMIN_DEFAULT_EMAIL=pgadmin@admin.com" -e "PGADMIN_DEFAULT_PASSWORD=admin" dpage/pgadmin4:latest
```
and then access pgadmin on web browser in port 8000 inside pgadmin use local up addres and port 5050 to access standalone pgadmin

## Question 3: Numbers of Row (yellow, 2020)
```
SELECT COUNT(1)
FROM public.yellow_tripdata as ydata
WHERE ydata.filename LIKE '%2020%'
```

## Question 4: Numbers of Row (green, 2020)
```
SELECT COUNT(1)
FROM public.green_tripdata as gdata
WHERE gdata.filename LIKE '%2020%'
```
