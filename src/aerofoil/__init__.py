import os
from airflow import configuration

AEROFOIL_LABEL = 'Aerofoil'
AEROFOIL_ROUTE_BASE = '/aerofoil'

airflow_base_log = configuration.get('logging', 'base_log_folder')
AEROFOIL_LOG_BASE = os.path.join(airflow_base_log, 'aerofoil')
AEROFOIL_LOG_BASE = f'{AEROFOIL_ROUTE_BASE}/logs'


def get_provider_info():
    return {
        'package-name': "apache-airflow-providers-aerofoil",
        'name': "Aerofoil",
        'description': "Various admin tools for Airflow",
        'version': ['1.0.0']
    }
