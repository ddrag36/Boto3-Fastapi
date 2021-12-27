# Boto3-Fastapi

Scheduler.py:
- Downloads files from s3 bucket
- Keeps the most useful insights from these files and do some calculations
- Saves the results in a json file and uploads it to the s3 bucket
- Runs the code every 15 minutes in order to have the most updated files


Api.py:
- Uses FASTAPI
- Compares the local json file with the one in the s3 bucket based on datetime and downloads it if it is more recent
- Uses GET method to read data
- The @app.get("/...") tells FastAPI that the function right below is in charge of handling requests that go to:
  - the path /...
  - using a get method
