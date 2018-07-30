from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gpx-lite",
    version="0.0.2",
    author='Olga Kholkovskaia',
    author_email='olga.kholkovskaia@gmail.com',
    license='MIT',
    description="Simple parser for gpx tracks, segments, and points with latitude, longitude, and time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/aicenter/gpx_lite',
    packages=['gpx_lite'],
    install_requires=['typing>=3.6.2'],
    classifiers=(
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
