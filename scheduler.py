import boto3
import re
import os
from collections import Counter
import json
import time
import schedule


def scheduler():
    session = boto3.Session(profile_name='default')
    s3= boto3.client('s3', 'us-east-1', aws_access_key_id=session.get_credentials().access_key, aws_secret_access_key=session.get_credentials().secret_key, aws_session_token=session.get_credentials().token)
    s3_1 = boto3.resource(
        service_name = 's3',
        region_name = 'us-east-1',
        aws_access_key_id = session.get_credentials().access_key,
        aws_secret_access_key = session.get_credentials().secret_key,
        aws_session_token = session.get_credentials().token  )  

    bucket = s3_1.Bucket('bucket_name')
    files = list(bucket.objects.all())

    for file in files:
        s3.download_file(Bucket='bucket_name',Key=file.key, Filename=file.key)



    def get_avg(folder,file):
        file_with_folder = folder + '/' + file
        regex = re.compile("Avr[:]\s+\d+\s+\d+\s+(\d+)\s+[|]\s+\d+\s+\d+\s+(\d+)")
        with open(file_with_folder, "r") as f:
            contents = f.read()
            matches = re.findall(regex, contents)
            if not len(matches[0]) == 2:
                print("error parsing")
                return
    
            sbu_comp =int(matches[0][0])
            sbu_deco = int(matches[0][1])
            sbu_map_raw ={
                "compression": sbu_comp,
                "decompression": sbu_deco,
                "total": sbu_comp + sbu_deco
            }
    
            return sbu_map_raw


    def collect_filenames(folder):
        return os.listdir(folder)


    d = {}
    folder = "output_s3"
    files = collect_filenames(folder)
    new_names = []


    for f in files:
        key = f.split('_')[0]
        new_names.append(key)
        d[key] = {'raw': []}

        
    Counter(new_names)
    instance_runs = dict(Counter(new_names))
    instance_runs


    for f in files:
        
        key = f.split('_')[0]
        content = get_avg(folder, f)
        d[key]['raw'].append(content)
        d[key]['avg_total']= int(sum(content['total'] for i in d[key]['raw'])/instance_runs[key])
        d[key]['avg_compression']= int(sum(content['compression'] for i in d[key]['raw'])/instance_runs[key])
        d[key]['avg_decompression']= int(sum(content['decompression'] for i in d[key]['raw'])/instance_runs[key])
        d[key]['total_runs'] = instance_runs[key]
        
        
    f = open("total.json", "w")
    json.dump(d, f)
    f.close()
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print('Json updated at : ',result)
    s3.upload_file('total.json','bucket_name','total.json') 
    print('Json uploaded to s3 bucket')

schedule.every(15).minutes.do(scheduler)

while 1:
    schedule.run_pending()
    time.sleep(1)