import json
import pprint
from airflow import DAG
from datetime import datetime
from airflow.decorators import task
from airflow.utils.session import create_session

from airflow.operators.python_operator import PythonOperator

from aerofoil.models.backfill import Backfill
from aerofoil.operators.bash import AerofoilBashOperator
from aerofoil.sensors.backfill_sensor import BackfillSensor


with DAG(
    "__aerofoil_backfill__",
    description="Aerofloil DAG to run Backfill jobs",
    schedule_interval="* * * * *",
    start_date=datetime(2020, 3, 20),
    catchup=False,
) as dag:

    backfill_sensor = BackfillSensor(task_id="backfill_sensor_task")
    BACKFILL_ID_KEY = "BACKFILL_ID"

    @task
    def find_backfills():
        results = []
        with create_session() as session:
            backfills = session.query(Backfill).filter_by(status="queued")
            for backfill in backfills:
                backfill_info = {}
                backfill_info["bash_command"] = backfill.cmd
                backfill_info["bash_context"] = {BACKFILL_ID_KEY: backfill.id}
                results.append(backfill_info)
                backfill.status = "locked"
            session.commit()
        return results

    backfill_infos = find_backfills()

    def _add_ti_details_to_backfill(context):
        backfill_id = context["bash_context"][BACKFILL_ID_KEY]
        ti = context["task_instance"]
        with create_session() as session:
            backfill = session.query(Backfill).get(backfill_id)
            backfill.status = ti.state
            backfill.ti_dag_id = ti.dag_id
            backfill.ti_task_id = ti.task_id
            backfill.ti_run_id = ti.run_id
            backfill.ti_map_index = ti.map_index
            session.commit()

    def backfill_failed(context):
        _add_ti_details_to_backfill(context)

    def backfill_success(context):
        _add_ti_details_to_backfill(context)

    backfill = AerofoilBashOperator.partial(
        task_id="backfill",
        do_xcom_push=False,
        on_success_callback=backfill_success,
        on_failure_callback=backfill_failed,
    ).expand_kwargs(backfill_infos)

    backfill_sensor >> backfill_infos >> backfill
