import os
import jinja2
import aerofoil


from airflow import configuration
from airflow.plugins_manager import AirflowPlugin

from aerofoil.views.backfill_view import BackfillView
from aerofoil.views.backfill_view import FakeSuccessView
from aerofoil.views.reset_view import ResetDagView
from aerofoil.views.restart_view import RestartView
from aerofoil.views.mydags_view import MyDagsView
from aerofoil.views.version_view import VersionView

from flask import Blueprint
from aerofoil import AEROFOIL_LABEL, AEROFOIL_LOG_BASE

view_backfill = BackfillView()
view_fs = FakeSuccessView()
view_mydags = MyDagsView()
view_reset_dag = ResetDagView()
view_restart = RestartView()
view_version = VersionView()

aerofoil_bp = Blueprint(
    "aerofoil_plugin",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/aerofoil",
)

backfill_pkg = {
    "name": "Backfill",
    "category": AEROFOIL_LABEL,
    "view": view_backfill
}

fs_pkg = {
    "name": "Fake Success",
    "category": AEROFOIL_LABEL,
    "view": view_fs
}

reset_pkg = {
    "name": "Reset Dag",
    "category": AEROFOIL_LABEL,
    "view": view_reset_dag
}

restart_pkg = {
    "name": "Restart Services",
    "category": AEROFOIL_LABEL,
    "view": view_restart,
}

mydags_pkg = {
    "name": "MyDags",
    "category": AEROFOIL_LABEL,
    "view": view_mydags
}

versions_pkg = {
    "name": "Dags Version",
    "category": AEROFOIL_LABEL,
    "view": view_version,
}


class AerofoilPlugin(AirflowPlugin):
    name = AEROFOIL_LABEL
    appbuilder_views = [backfill_pkg, fs_pkg, reset_pkg, mydags_pkg]
    appbuilder_menu_items = []
    flask_blueprints = [aerofoil_bp]
