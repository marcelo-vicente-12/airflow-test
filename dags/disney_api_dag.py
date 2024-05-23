from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
import pandas as pd
import urllib.request, json
from datetime import datetime, timedelta
from io import BytesIO

api_url = "https://api.disneyapi.dev/character"
s3_bucket = "mvs-sync"
s3_path = "input/disney/character/"

default_args = {
    'owner' : 'airflow',
    'depends_on_past' : False,
    'email': ['marcelo.vicente@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,    
    'retries' : 0,
    'retry_delay': timedelta(minutes=2),
}

def get_data(api_url):
    with urllib.request.urlopen(api_url) as url:
        url_data = json.load(url)
        
    df = pd.DataFrame(url_data['data'])
    print("df.head: ) ", df.head())    

    return df

def has_data(ti):
    df = ti.xcom_pull(task_ids='get_data')

    return 'saving_raw_data' if ( len(df.index) > 0 ) else 'alarm_dag'

def alarm_dag():
    print("Disney API não trouxe nenhum dado.")
    raise ValueError("Disney API não trouxe nenhum dado.")

def saving_raw_data(s3_bucket, s3_path, ti):
    s3 = S3Hook()

    df_disney = ti.xcom_pull(task_ids='get_data')
    df_disney.info()
    print(len(df_disney.index))
      
    # salvando dados no S3
    out_buffer = BytesIO()
    s3_filename = datetime.now().strftime('%Y%m%d_%H%M%S%f')
    s3_key = s3_path + s3_filename + '.parquet'
    df_disney.to_parquet(out_buffer, index=False, compression="snappy")
    s3.load_bytes(bytes_data=out_buffer.getvalue(), bucket_name=s3_bucket, replace=True, key=s3_key)

with DAG('disney_api', schedule_interval='*/5 * * * *', default_args=default_args, catchup=False, start_date=datetime.now()) as dag:
    get_data = PythonOperator(
        task_id = 'get_data',
        python_callable=get_data,
        op_args=[api_url]
    )

    has_data = BranchPythonOperator(
        task_id = 'has_data',
        python_callable = has_data
    )

    alarm_dag = PythonOperator(
        task_id = 'alarm_dag',
        python_callable=alarm_dag
    )

    saving_raw_data = PythonOperator(
        task_id = 'saving_raw_data',
        python_callable=saving_raw_data,
        op_args=[s3_bucket, s3_path]
    )

get_data >> has_data >> [alarm_dag, saving_raw_data] 