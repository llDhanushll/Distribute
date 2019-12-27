from setuptools import setup
import sys

if sys.version_info < (3,5):
    sys.exit('Sorry, Python < 3.7 is not supported')

VERSION = "0.0.1"


setup(
    name="vanetSignature",
    version=VERSION,
    author="Dhanush",
    author_email="dhanushdazz@gmail.com",
    description="A python package for hmac",
    long_description='Vanet Signatures using hmac',
    url="",
    packages=['vanetSign'],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)