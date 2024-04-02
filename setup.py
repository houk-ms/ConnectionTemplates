# setup.py
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='azure-iac-generator',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},  # specify the src directory
    license='MIT',
    description='Azure resource infrastructure as code generator',
    long_description=open('README.md').read(),
    install_requires=required,  # read from requirements.txt
)