#!/usr/bin/env python

from setuptools import setup

setup(
    name="rfexplorer-detailed-scan",
    version="0.0.3",
    py_modules=[
        "rfexplorerDetailedScan",
        "rfexplorerDetailedScanLib",
    ],
    install_requires=[
        "Click",
        "RFExplorer",
    ],
    entry_points="""
        [console_scripts]
        rfexplorerDetailedScan=rfexplorerDetailedScan:rfexplorerDetailedScan
    """,
)
