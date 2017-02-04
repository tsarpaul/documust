import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as required_file:
    required = required_file.read().splitlines()

setup(
    name='DocUMust',
    version='0.0.1',
    packages=['documust'],
    description="Lets make sure you don't forget to document this time.",
    author='Paul Litvak',
    author_email='litvakpol@012.net.il',
    install_requires=required,
    include_package_data=True,
    url='https://github.com/tsarpaul/DocUMust',
    license='MIT License',
    keywords=['documentation', 'python', 'tool'],
    entry_points={
        'console_scripts': [
            'documust=documust.cli:handle'
        ]
    },
    classifiers=[
    ],
)
