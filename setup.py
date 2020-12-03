# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='Curves',
    url='https://github.com/missing',
    author='Robert Rehammar',
    author_email='robert@rehammar.se',
    packages=find_packages(exclude=['tests*']),
    install_requires=['numpy', 'scipy', 'matplotlib', 'pyqt5'],
    version='0.2',
    license='MIT',
    description='A package to generate parametric curves in 2d',
    long_description=open('README.md').read(),
)
