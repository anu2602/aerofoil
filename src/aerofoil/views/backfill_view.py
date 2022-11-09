import os
import socket
import signal
import subprocess

from datetime import datetime
from airflow.utils.db import provide_session

from flask import request, redirect, jsonify, render_template
from flask_appbuilder import BaseView, expose

from aerofoil.models.backfill import Backfill
from aerofoil import AEROFOIL_ROUTE_BASE, AEROFOIL_LOG_BASE
from aerofoil.utils.web_utils import login_required, get_current_user

BACKFILL_HISTORY_LIMIT = 50


class BackfillBaseView(BaseView):
    default_view = "base"

    @expose("/run")
    @login_required
    @provide_session
    def run_backfill(self, session=None):
        dag_name = request.args.get("dag_name")
        task_regex = request.args.get("task_regex")

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        clear_previous = request.args.get(
            "clear_previous", default=False, type=lambda v: v.lower() == "true"
        )
        rerun_failed = request.args.get(
            "rerun_failed", default=False, type=lambda v: v.lower() == "true"
        )
        run_backwards = request.args.get(
            "run_backwards", default=False, type=lambda v: v.lower() == "true"
        )
        mark_success = request.args.get(
            "mark_success", default=False, type=lambda v: v.lower() == "true"
        )

        backfill = Backfill(
            dag_id=dag_name,
            task_regex=task_regex,
            status="queued",
            start_date=start_date,
            end_date=end_date,
            clear_previous=clear_previous,
            rerun_failed=rerun_failed,
            run_backwards=run_backwards,
            mark_success=mark_success,
            started_by=get_current_user(),
            started_at=datetime.now(),
        )

        session.add(backfill)
        session.commit()
        session.expire(backfill)

        return self.history(session)

    @expose("/history")
    @provide_session
    def history(self, session=None):
        mark_success = request.args.get(
            "mark_success", default=False, type=lambda v: v.lower() == "true"
        )
        results = (
            session.query(Backfill)
            .filter_by(mark_success=mark_success)
            .order_by(Backfill.started_at.desc())
            .limit(BACKFILL_HISTORY_LIMIT)
        )
        data = []
        for result in results:
            data_row = {
                "dag_id": result.dag_id,
                "status": result.status,
                "run_datetime": result.started_at.strftime("%b %d %Y %H:%M:%S"),
                "start_date": result.start_date.strftime("%b %d %Y"),
                "end_date": result.end_date.strftime("%b %d %Y"),
                "started_by": result.started_by,
                "log_url": "TODO",
                "kill_ulr": "TODO",
            }
            data.append(data_row)
        return jsonify(data)
        return jsonify({"success": True})


class BackfillView(BackfillBaseView):
    default_view = "base"
    route_base = f"{AEROFOIL_ROUTE_BASE}/backfill"

    @expose("/")
    def base(self):
        return self.render_template("aerofoil/backfill.html", url_base=self.route_base)


class FakeSuccessView(BackfillBaseView):
    default_view = "base"
    route_base = f"{AEROFOIL_ROUTE_BASE}/fake-success"

    @expose("/")
    def base(self):
        return self.render_template(
            "aerofoil/fake_success.html", url_base=self.route_base
        )
