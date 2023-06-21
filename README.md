# Boto3-Fastapi

### Scheduler.py:
- Downloads files from AWS S3 bucket
- Keeps the most useful insights from these files for calculations
- Saves the results in a json file and uploads it to the s3 bucket
- Runs the code every 15 minutes in order to have the most updated files


### Api.py:
- Uses FastAPI
- Compares the local json file with the one in the AWS S3 bucket based on datetime and downloads it if it is more recent
- Uses GET method to read data
