import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "netroc",
    version = "0.1",
    author = "Yasir Suhail",
    description = ("Utility for constructing labels and scores for link prediction in large complex networks"),
    license = "GNU Lesser General Public License (LGPL)",
    keywords = "machine-learning complex-network link-prediction",
    url = "https://github.com/yasirs/netroc",
    packages=['netroc', 'examples'],
    install_requires=['yard'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: LGPL License",
    ],
)
