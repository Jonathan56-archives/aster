try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

config = {
    'description': 'Mars Logistic',
    'author': 'Jonathan Coignard',
    'author_email': 'jcoignard@lbl.gov',
    'version': '0.0.0',
    'install_requires': required,
    'packages': ['aster'],
    'name': 'aster',
    'package_data': {'': ['*.csv']},  # Add the drivecycle matlab data
    'include_package_data': True,
}

setup(**config)
