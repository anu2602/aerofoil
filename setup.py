from distutils.core import setup
from setuptools import find_packages, setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='apache-airflow-providers-aerofoil',
    version='1.0.0',
    description='A convenient add-on for Apache Airflow',
    long_description=read('README.md'),
    author='Anuradha Chowdhary',
    author_email='mail@achowdhary.com',
    entry_points{
        'apache_airflow_provider': [
            'provider_info=aerofoil.__init__:get_provider_info'
        ],
        'airflow_plugins': [
            'aerofoil=aerofoil.aerofoil_plugin:AerofoilPlugin'
        ]
    },

    packages=[
        'aerofoil',
        'aerofoil.templates',
        'aerofoil.hooks',
        'aerofoil.operators',
        'aerofoil.sensors',
        'aerofoil.utils'
    ],

    install_requires=[
        'apache-airflow'
        '[postgres, jdbc, celery,ssh] => 2.2.3'
    ],

    python_requires='~=3.7',
    package_dir={'': 'src'},
    include_package_data=True
)