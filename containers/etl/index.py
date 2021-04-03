from google.cloud import storage
import pandas as pd
import os

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

bucket = os.environ["BUCKET"]
print("Downloading CSV",end="")
#change here the bucket
download_blob(bucket,"scores.csv","scores.csv")
print("done")

print("Reading Data...")
df = pd.read_csv('scores.csv',sep=';', delimiter=None, header='infer')
#ZONE;P1;P2;FINAL;SCORE;CLASI Current Colums
#We drop some fields
print("Dropping Unnecesary Columns...")
df = df.drop(columns=['SCORE', 'CLASI'])

print("Fixing Column Types...")
df.FINAL = df.FINAL.astype(int)
print("done")

#Just removes unnecesary fields
print("Generating and Uploading Cleaned Data...")
df.to_csv("scores_processed.csv",index=False,sep=';')
upload_blob(bucket,"scores_processed.csv","scores_processed.csv")
print("done")

print("Show new Dataset")
print(df.head(3))
