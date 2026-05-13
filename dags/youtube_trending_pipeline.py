from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

# Note: In a real implementation, we would import our src modules here.
# from src.extract.youtube_api import extract_trending_videos
# from src.transform.bronze_to_silver import process_silver_layer
# from src.transform.silver_to_gold import process_gold_layer
# from src.load.postgres_loader import load_to_analytics_db

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': True, # Setup email config in Airflow
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'youtube_trending_lakehouse_pipeline',
    default_args=default_args,
    description='ETL pipeline for YouTube Trending Data Lake (Medallion Architecture)',
    schedule_interval='@daily',
    start_date=datetime(2023, 10, 1),
    catchup=False,
    tags=['youtube', 'medallion', 'daily'],
) as dag:

    start_pipeline = EmptyOperator(task_id='start_pipeline')

    # PHASE 1: Extract (API -> Bronze)
    extract_to_bronze = PythonOperator(
        task_id='extract_to_bronze_layer',
        python_callable=lambda: print("Extracting data from YouTube API to Bronze (JSON)..."),
        # op_kwargs={'execution_date': '{{ ds }}'}
    )

    # PHASE 2: Transform (Bronze -> Silver)
    transform_to_silver = PythonOperator(
        task_id='transform_to_silver_layer',
        python_callable=lambda: print("Cleaning and converting Bronze JSON to Silver Parquet..."),
        # op_kwargs={'execution_date': '{{ ds }}'}
    )

    # PHASE 3: Transform (Silver -> Gold)
    transform_to_gold = PythonOperator(
        task_id='transform_to_gold_layer',
        python_callable=lambda: print("Aggregating Silver Parquet to Gold Parquet for Analytics..."),
        # op_kwargs={'execution_date': '{{ ds }}'}
    )

    # PHASE 4: Load (Gold -> PostgreSQL Analytics DB)
    load_to_postgres = PythonOperator(
        task_id='load_gold_to_postgres',
        python_callable=lambda: print("Loading Gold datasets into PostgreSQL for Dashboarding..."),
        # op_kwargs={'execution_date': '{{ ds }}'}
    )

    # PHASE 5: Data Quality Checks (Simulated)
    data_quality_check = PythonOperator(
        task_id='run_data_quality_checks',
        python_callable=lambda: print("Running Great Expectations or custom DQ checks on Gold tables...")
    )

    end_pipeline = EmptyOperator(task_id='end_pipeline')

    # Define Dependencies (DAG Flow)
    start_pipeline >> extract_to_bronze >> transform_to_silver >> transform_to_gold >> load_to_postgres >> data_quality_check >> end_pipeline
