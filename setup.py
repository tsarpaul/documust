import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as required_file:
    required = required_file.read().splitlines()

setup(
    name='smart-deploy',
    version='0.2.0.5',
    packages=['smart_deploy'],
    description='A solution for automating your serverless lambda deployment!',
    author='Paul Litvak',
    author_email='litvakpol@012.net.il',
    install_requires=required,
    include_package_data=True,
    url='https://github.com/tsarpaul/serverless-smart-deploy',
    license='MIT License',
    keywords=['automate', 'serverless', 'deploy'],
    entry_points={
        'console_scripts': [
            'smart-deploy=smart_deploy.cli:handle'
        ]
    },
    classifiers=[
    ],
)
