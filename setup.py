# setup.py
"""
Setup script for the CSV to JSON converter package.
"""

from setuptools import setup, find_packages

setup(
    name='csv-to-json-converter',
    version='1.0.0',
    description='A Python tool to convert CSV files to JSON format',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    py_modules=['csv_to_json_converter'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'csv2json=csv_to_json_converter:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
