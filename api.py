from fastapi import FastAPI, Path,HTTPException
import json
import boto3
import botocore
import os
import stat
import os.path
from datetime import datetime, timezone
import time


app = FastAPI()

def compare():
    
    session = boto3.Session(profile_name='default')
    s3= boto3.client('s3', 'us-east-1', aws_access_key_id=session.get_credentials().access_key, aws_secret_access_key=session.get_credentials().secret_key, aws_session_token=session.get_credentials().token)
    s3_1 = boto3.resource(
        service_name = 's3',
        region_name = 'us-east-1',
        aws_access_key_id = session.get_credentials().access_key,
        aws_secret_access_key = session.get_credentials().secret_key,
        aws_session_token = session.get_credentials().token  )  
    try:
        s3_1.Object('bucketname', 'total.json').load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("File does not exists")
    else:
        if os.path.exists('total.json') == False:
            s3.download_file('bucket_name','total.json','total.json')
        response = s3.head_object(
            Bucket='bucket_name',
            Key='total.json',
        )
        t =response['ResponseMetadata']['HTTPHeaders']['last-modified']
        date_time_file_s3 = datetime.strptime(t, '%a, %d %b %Y %H:%M:%S %Z')
        fileStatsObj = os.stat ('total.json' )
        modificationTime = time.ctime ( fileStatsObj [ stat.ST_MTIME ] )
        date_time_local_file = datetime.strptime(modificationTime, '%a %b %d %H:%M:%S %Y')
        if date_time_file_s3 > date_time_local_file:
            s3.download_file('bucket_name','total.json','total.json')
       
  
    

@app.get("/")
def index():
    compare()
    with open('total.json') as f:
        data = json.load(f)
    return data
   

@app.get("/get-instances/{instance_name}")
def get_instances(instance_name: str = Path(None, description = "Instance name results you want to view")):
    compare()
    with open('total.json') as f:
        data = json.load(f)
    return data[instance_name]


