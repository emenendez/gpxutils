from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='gpxutils',

    version='3.0.0',

    description='Tools for working with GPX files',
    long_description="""
gpxutils
========

Tools for working with GPX files.

gpxclean
--------

Clean GPX tracks and split into multiple files.

gpxpull
-------

Pull files from modern Garmin GPSes, clean, and split. On Windows, with the help of the USB Drive Letter Manager (http://www.uwe-sieber.de/usbdlm_e.html), gpxpull can automatically download and clean GPX files from a USB-connected Garmin GPS.
""",

    url='https://github.com/emenendez/gpxutils',

    author='Eric Menendez',
    author_email='ericmenendez@gmail.com',

    license='AGPLv3+',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Topic :: Utilities',

        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        'Programming Language :: Python :: 3.4',
    ],

    keywords='gpx gps geo spatial utilities',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['gpxpy'],

    entry_points={
        'console_scripts': [
            'gpxclean=gpxutils.gpxclean:main',
            'gpxpull=gpxutils.gpxpull:main',
        ],
    },
)
