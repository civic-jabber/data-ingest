from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from civic_jabber_ingest.regs.va import load_va_regulations

default_args = {
    "owner": "civic-jabber",
    "depends_on_past": False,
    "start_date": datetime.today() - timedelta(days=1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


dag = DAG(
    "civic-jabber-states", default_args=default_args, schedule_interval="0 4 * * *"
)


load_va = PythonOperator(
    task_id="va-regulations-load", python_callable=load_va_regulations, dag=dag
)
