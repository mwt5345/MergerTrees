from setuptools import setup

with open("README.md",'r') as f:
    long_description = f.read()

setup(
   name='MergerTrees',
   version='0.1',
   description='Analysis of merger trees',
   license="MIT",
   long_description=long_description,
   author='Michael W. Toomey',
   author_email='michael_toomey@brown.edu',
   packages=['mt'],
)
