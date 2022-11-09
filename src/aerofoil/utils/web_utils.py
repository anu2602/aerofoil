import airflow
from airflow import configuration
from flask_login import current_user
from functools import wraps


def login_required(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if airflow.login:
            return airflow.login.login_required(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return func_wrapper


def get_current_user(raw=True):
    return current_user.username


def is_ssl_enabled():
    ssl_cert = configuration.get("webserver", "web_server_ssl_cert")
    return True if ssl_cert else False
