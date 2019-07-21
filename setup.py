import re

from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'sharedlists', '__init__.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S).\
        match(v_file.read()).group(1)


dependencies = [
    #'restfulpy >= 3.3.0',
    'easycli >= 1.3.1, < 2',

    # Deployment
    'gunicorn',
]


setup(
    name='sharedlists',
    version=package_version,
    packages=find_packages(),
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

