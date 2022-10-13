import os
import time
import socket
import logging
import subprocess

from datetime import datetime

from airflow.utils.db import provide_session
from airflow.jobs.base_job import BaseJob
from airflow.models import DagRun, TaskInstance, TaskFail, TaskReschedule

from flask import request, redirect, jsonify, render_template
from flask_appbuilder import BaseView, expose

from aerofoil.models.reset_dag import ResetDagAudit
from aerofoil import AEROFOIL_ROUTE_BASE, AEROFOIL_LOG_BASE
from aerofoil.utils.web_utils import login_required, get_current_user

RESET_HISTORY_LIMIT = 50


class ResetDagView(BaseView):
    default_view = "base"
    route_base = f"{AEROFOIL_ROUTE_BASE}/resetdag"

    @expose("/")
    def base(self):
        return self.render_template("aerofoil/reset.html", url_base=self.route_base)

    @expose("/doit", methods=["POST"])
    @login_required
    @provide_session
    def doit(self, session=None):
        dag_id = request.form.get("dag_name")
        reset_reason = request.form.get("reset_reason")

        ti_delete = TaskInstance.__table__.delete().where(TaskInstance.dag_id == dag_id)
        tf_delete = TaskFail.__table__.delete().where(TaskFail.dag_id == dag_id)
        tr_delete = TaskReschedule.__table__.delete().where(
            TaskReschedule.dag_id == dag_id
        )
        dr_delete = TaskReschedule.__table__.delete().where(DagRun.dag_id == dag_id)
        bj_delete = BaseJob.__table__.delete().where(BaseJob.dag_id == dag_id)

        session.execute(ti_delete)
        session.execute(tf_delete)
        session.execute(tr_delete)
        session.execute(dr_delete)
        session.execute(bj_delete)

        resetAudit = ResetDagAudit()
        resetAudit.dag_id = dag_id
        resetAudit.reset_type = "DagRun"
        resetAudit.reset_reason = reset_reason
        resetAudit.reset_by = get_current_user()
        resetAudit.reset_date = datetime.now()
        session.add(resetAudit)
        session.commit()

        return self.history(session)

    @expose("/history")
    @provide_session
    @login_required
    def history(self, session=None):
        results = (
            session.query(ResetDagAudit)
            .order_by(ResetDagAudit.reset_date.desc())
            .limit(RESET_HISTORY_LIMIT)
        )
        data = []
        for result in results:
            data_row = {
                "dag_id": result.dag_id,
                "reset_by": result.reset_by,
                "reset_date": result.reset_date.strftime("%b %d %Y %H:%M:%S"),
                "reset_reason": result.reset_reason,
            }
            data.append(data_row)
        return jsonify(data)
