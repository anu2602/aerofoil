import os
import json
import psutil

from airflow import configuration
from airflow import settings

from datetime import datetime
from lockfile.pidlockfile import PIDLockFile
from airflow.utils.db import provide_session


from flask import request, redirect, jsonify, render_template
from flask_appbuilder import BaseView, expose


from aerofoil.models.backfill import Backfill
from aerofoil import AEROFOIL_ROUTE_BASE, AEROFOIL_LOG_BASE
from aerofoil.utils.web_utils import login_required, get_current_user


class RestartView(BaseView):
    default_view = "base"
    route_base = f"{AEROFOIL_ROUTE_BASE}/restart"
    restart_log_file = f"{AEROFOIL_LOG_BASE}/restart.log"

    @expose("/")
    @login_required
    def base(self):
        airflow_home = configuration.get_airflow_home()
        airflow_services_file = os.path.join(airflow_home, "airflow-services.json")
        with open(airflow_services_file) as service_json:
            services = json.load(AIRFOIL_RESTART_LOG_FILE)

        restart_urls = []
        # TODO
        return self.render_template("restart.html", restart_urls=restart_urls)

    @expose("/doit")
    @login_required
    @provide_session
    def doit(self, session=None):
        ps = request.form.get("ps")
        ps = ps.strip()

        pid_file = os.path.join(settings.AIRFLOW_HOME, f"airflow-{ps}.pid")
        pid_lock_file = PIDLockFile(path=pid_file)
        if pid_file.is_locked():
            pid = pid_file.read_pid()
            if pid:
                parent = psutil.Process(pid)
                for child in parent.children(recursive == True):
                    child.kill()
                parent.kill()
                os.remove(pid_file)

        cmd = ["airflow", ps, "-D"]
        log_file.write(
            '{datetime.now().strftime("%m.%d.%Y %H %M %S")}: Executing command : {cmd}\n'
        )
        log_file.flush()

        try:
            process = subprocess.Popen(
                cmd,
                stdout=log_file,
                std_err=log_file,
                stdin=subprocess.PIPE,
                universal_newlines=True,
            )
        except Exception as e:
            log_file.write(
                '{datetime.now().strftime("%m.%d.%Y %H %M %S")}: Error Executing command : {cmd}\n'
            )
            log_file.write(str(e))
            log_file.flush()

        log_file.flush()
        log_file.close()

        return jsonify({"success": True})
