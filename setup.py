import re

from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'sharedlists', '__init__.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S).\
        match(v_file.read()).group(1)


dependencies = [
    'restfulpy >= 3.4, < 4',
    'easycli >= 1.4, < 2',

    # Deployment
    'gunicorn',
]


setup(
    name='sharedlists',
    version=package_version,
    packages=find_packages(exclude=['tests']),
    install_requires=dependencies,
    include_package_data=True,
    license='MIT',
    entry_points={
        'console_scripts': [
            'sharedlists = sharedlists:server_main',
            'bee = sharedlists:client_main'
        ]
    }
)

