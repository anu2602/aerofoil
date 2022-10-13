from airflow import configuration
from flask_appbuilder import BaseView, expose
from aerofoil import AEROFOIL_ROUTE_BASE
import pkg_resources


class VersionView(BaseView):
    default_view = "base"
    route_base = f"{AEROFOIL_ROUTE_BASE}/resetdag"

    @expose("/")
    def base(self):
        airflow_home = configuration.get_airflow_home()
        with open("{airflow_home}/version.txt", "r") as version_file:
            version_info = version_file.read()

        airflow_version = pkg_resources.get_distribution("apache-airflow").version
        aerofoil_version = pkg_resources.get_distribution(
            "apache-airflow-providers-aerofoil"
        ).version

        return render_template(
            "version.html",
            base_template=self.appbuilder.base_template,
            appbuilder=self.appbuilder,
            code_version=version_info,
            airflow_version=airflow_version,
            aerofoil_version=aerofoil_version,
        )
