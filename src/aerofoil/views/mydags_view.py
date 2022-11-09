from flask import redirect, url_for
from flask_appbuilder import BaseView, expose

from aerofoil import AEROFOIL_ROUTE_BASE
from aerofoil.utils.web_utils import login_required, get_current_user


class MyDagsView(BaseView):
    default_view = "base"
    route_base = f"{AEROFOIL_ROUTE_BASE}/mydags"

    @expose("/")
    def base(self, session=None):
        searchMe = f"%{get_current_user()}%"
        return redirect(url_for("Airflow.index", search=searchMe))
