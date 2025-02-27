import os
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.utils.dates import days_ago

# Constants
BUCKET_NAME = "airflow-bucket-demo"
PROJECT_ID = "my-gcp-project"
LOCAL_PATH = "/opt/airflow/data"

# URLs for NYC Taxi Data
FILES = {
    "green_tripdata_2019-01.csv.gz": "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz",
    "yellow_tripdata_2019-01.csv.gz": "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz",
    "fhv_tripdata_2019-01.csv.gz": "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz",
}

# Function to download files
def download_files():
    os.makedirs(LOCAL_PATH, exist_ok=True)
    for file_name, url in FILES.items():
        file_path = os.path.join(LOCAL_PATH, file_name)

        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded {file_name} to {file_path}")

# Define DAG
dag = DAG(
    "download_and_upload_gcs",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
)

# Task 1: Download Files
download_task = PythonOperator(
    task_id="download_files",
    python_callable=download_files,
    dag=dag,
)

# Task 2: Upload Files to GCS
upload_tasks = []
for file_name in FILES.keys():
    upload_task = LocalFilesystemToGCSOperator(
        task_id=f"upload_{file_name}",
        src=os.path.join(LOCAL_PATH, file_name),
        dst=f"nyc-taxi/{file_name}",
        bucket=BUCKET_NAME,
        mime_type="application/gzip",
        dag=dag,
    )
    upload_tasks.append(upload_task)

# Set task dependencies
download_task >> upload_tasks
