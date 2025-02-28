# -*- coding: utf-8 -*-
"""Airflow_team2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KVq0YVc81-w8LO5f4VnTPRLWpdTXOnB0
"""

"""
DAG to download GitHub data from the API.
"""

import datetime

import airflow
from airflow.operators.bash import BashOperator

_DAG_ID = "download_github_data_for_SOL_6hour_gap"
_DAG_DESCRIPTION = (
    "Download GitHub data for SOL every 6 hours and save to Postgres"
)
# Specify when often to execute the DAG.
_SCHEDULE = "05 0,6,12,18 * * *"

# Pass default parameters for the DAG.
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

# Create a DAG.
dag = airflow.DAG(
    dag_id=_DAG_ID,
    description=_DAG_DESCRIPTION,
    max_active_runs=1,
    default_args=default_args,
    schedule_interval=_SCHEDULE,
    catchup=False,
    start_date=datetime.datetime(2023, 4, 10, 0, 0, 0),
)




bash_command1 = [
    # Sleep 5 seconds to ensure the bar is finished.
    "sleep 5",
    "&&",
    "/cmamp/sorrentum_sandbox/examples/ml_projects/SorrIssue21_Team2_Implement_sandbox_for_GitHub_2/download_to_db_team2.py",	
    "--pair SOL",
    "--target_table 'github_main'",
    #"--start_timestamp {{ data_interval_start }} ",
    #"--end_timestamp {{ data_interval_end }}",
    "-v DEBUG"
]

bash_command2 = [
    # Sleep 5 seconds to ensure the bar is finished.
    "sleep 5",
    "&&",
    "/cmamp/sorrentum_sandbox/examples/ml_projects/SorrIssue21_Team2_Implement_sandbox_for_GitHub_2/download_to_db_team2.py",	
    "--pair SOL",
    "--target_table 'github_issues'",
    #"--start_timestamp {{ data_interval_start }} ",
    #"--end_timestamp {{ data_interval_end }}",
    "-v DEBUG"
]

bash_command3 = [
    # Sleep 5 seconds to ensure the bar is finished.
    "sleep 5",
    "&&",
    "/cmamp/sorrentum_sandbox/examples/ml_projects/SorrIssue21_Team2_Implement_sandbox_for_GitHub_2/download_to_db_team2.py",	
    "--pair SOL",
    "--target_table 'github_commits'",
    #"--start_timestamp {{ data_interval_start }} ",
    #"--end_timestamp {{ data_interval_end }}",
    "-v DEBUG"
]

downloading_main = BashOperator(
    task_id="download_main",
    depends_on_past=False,
    bash_command=" ".join(bash_command1),
    dag=dag,
)

downloading_issues = BashOperator(
    task_id="downloading_issues",
    depends_on_past=False,
    bash_command=" ".join(bash_command2),
    dag=dag,
)

downloading_commits = BashOperator(
    task_id="downloading_commits",
    depends_on_past=False,
    bash_command=" ".join(bash_command3),
    dag=dag,
)


downloading_main >> downloading_issues >> downloading_commits
