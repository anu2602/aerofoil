from sqlalchemy.ext.declarative import declarative_base, declared_attr
from airflow import settings

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    PickleType,
    Index,
    Float,
)

Base = declarative_base()


class Backfill(Base):
    __tablename__ = "aerofoil_backfill"
    id = Column(Integer, primary_key=True)
    dag_id = Column(String(250), index=True, nullable=False)
    task_regex = Column(String(250), nullable=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    clear_previous = Column(Boolean, default=False)
    rerun_failed = Column(Boolean, default=False)
    run_backwards = Column(Boolean, default=False)
    mark_success = Column(Boolean, default=False)

    status = Column(String(10), nullable=False)
    ti_dag_id = Column(String(250))
    ti_run_id = Column(String(250))
    ti_task_id = Column(String(250))
    ti_map_index = Column(Integer)
    cmd = Column(String(500), index=True)

    started_at = Column(DateTime, index=True)
    started_by = Column(String(64))
    terminated_at = Column(DateTime)
    terminated_by = Column(String(64))

    def __init__(self, **kwargs):
        super(Backfill, self).__init__(**kwargs)
        self.cmd = self._build_backfill_cmd()

    def _build_backfill_cmd(self):
        cmd = f"airflow dags backfill -s {self.start_date} -e {self.end_date} -x -y "

        if self.clear_previous:
            cmd += "--reset-dagruns "
        if self.rerun_failed:
            cmd += "--rerun-failed-tasks "
        if self.clear_previous:
            cmd += "--run-backwards"

        if self.task_regex:
            cmd += "-t {self.task_regex}"

        cmd += self.dag_id
        print(cmd)
        return cmd
