# ASCENDA
 
## Getting Started

1. ensure Python 3.9+ is installed
2. checkout the code
3. activate the virtual environment by running the following command
```commandline
> . venv/bin/activate
```
4. run the flask application using the following command
```
python app.py
```
5. run the following command to merge the data
```commandline
curl --location 'http://127.0.0.1:5000/merge' \
--header 'Content-Type: application/json' \
--data '{
    "source_url": "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme"
}'
```
```commandline
curl --location 'http://127.0.0.1:5000/merge' \
--header 'Content-Type: application/json' \
--data '{
    "source_url": "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia"
}'
```

```commandline
curl --location 'http://127.0.0.1:5000/merge' \
--header 'Content-Type: application/json' \
--data '{
    "source_url": "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies"
}'
```
6. run the following command to fetch the selected data. `hotel_id` is the optional command. If not passed, it returns data of all the hotels
```commandline
curl --location 'http://127.0.0.1:5000/get-hotel-info-by-id' \
--header 'Content-Type: application/json' \
--data '{
    "hotel_id": "SjyX"
}'
```
7. run the following command to fetch all the hotels info
```commandline
curl --location --request POST 'http://127.0.0.1:5000/get-all-hotels-info' \
--header 'Content-Type: application/json'
```