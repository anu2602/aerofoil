from airflow.sensors.base_sensor_operator import BaseSensorOperator
from aerofoil.models.backfill import Backfill
from airflow.utils.session import create_session


class BackfillSensor(BaseSensorOperator):
    def poke(self, context):
        with create_session() as session:
            backfill_count = session.query(Backfill).filter_by(status="queued").count()
            if backfill_count > 0:
                return True
        return False
