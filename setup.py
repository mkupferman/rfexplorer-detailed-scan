#!/usr/bin/env python

from setuptools import setup

setup(
    name='rfexplorer-detailed-scan',
    version='0.0.1',
    py_modules=['rfexplorerDetailedScan'],
    install_requires=[
        'Click',
        'RFExplorer',
    ],
    entry_points='''
        [console_scripts]
        rfexplorerDetailedScan=rfexplorerDetailedScan:rfexplorerDetailedScan
    ''',
)
