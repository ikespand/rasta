#!/usr/bin/env python
"""The setup script.
"""

from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()


with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()
    requirements = [x[:-1] for x in requirements]

setup_requirements = ['setuptools >= 38.6.0', 'twine >= 1.11.0']

setup(
    author="Sandeep Pandey",
    author_email='spandey.ike@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
    description="Description ",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=['rasta', 'geojson', 'gtfs', 'geospatial', 'keplergl'],
    name='rasta',
    packages=find_packages(include=['rasta']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ikespand/rasta',
    version='0.0.1',
    zip_safe=False,
)