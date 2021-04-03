from google.cloud import storage
import pandas as pd
import os
import requests
import urllib3

#Ignore SSL Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client.from_service_account_json('argok3s.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client.from_service_account_json('argok3s.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def predict(zone,p1,p2):
    r = requests.post('https://'+os.environ["endpoint"]+'/'+os.environ["appname"]+'/predict',\
         json = {'data':[int(zone),int(p1),int(p2)]} \
         ,verify=False)
    return int(r.json()["prediction"])

bucket = os.environ["BUCKET"]
print("Downloading CSV...",end="")
#change here the bucket
download_blob(bucket,"scores_processed.csv","scores_processed.csv")
print("done")

print("Reading Data...",end="")
df = pd.read_csv('scores_processed.csv',sep=';', delimiter=None, header='infer')
print("done")

print("Doing inference...",end="")
df["FINAL_prediction"] = df.apply(lambda x: predict(x["ZONE"],x["P1"],x["P2"]), axis=1)
df.to_csv("inference.csv",index=False,sep=';')
upload_blob(bucket,"inference.csv","inference.csv")
print("done")

print("Showing inference")
print(df.head(5))
print("done")
