from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gpxutils',

    version='1.0.1',

    description='Tools for working with GPX files',
    long_description=long_description,

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
