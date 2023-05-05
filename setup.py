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
    include_package_data=True,
    entry_points={
        'apache_airflow_provider': [
            'provider_info=aerofoil.__init__:get_provider_info'
        ],
        'airflow.plugins': [
            'aerofoil=aerofoil.aerofoil_plugin:AerofoilPlugin'
        ]
    },

    packages=[
        'aerofoil',
        'aerofoil.models',
        'aerofoil.utils',
        'aerofoil.sensors',
        'aerofoil.operators',
        'aerofoil.views'
    ],

    python_requires='~=3.7',
    package_dir={'': 'src'},
)
