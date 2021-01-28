from google.cloud import storage
import pandas as pd

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

print("Downloading CSV",end="")
download_blob("argok3s","scores.csv","scores.csv")
print("done")

print("Reading Data...")
df = pd.read_csv('scores.csv',sep=';', delimiter=None, header='infer')
print(df.head(3))
df.FINAL = df.FINAL.astype(int)
print("done")

print("Creating Dataframe...",end="")
feature_cols = ["ZONE","P1","P2"]
X = df.loc[:, feature_cols]
y = df.FINAL
print("done")

print("Generating model...",end="")
import numpy as np
from sklearn.linear_model import LinearRegression

clf = LinearRegression().fit(X, y)
print("prediction",clf.predict([[25,19,18]]),end="")
print("done")

print("Uploading model to Cloud Storage...",end="")
from joblib import dump
dump(clf, 'scores.model')
upload_blob("argok3s","scores.model","scores.model")
print("done")