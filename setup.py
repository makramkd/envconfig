from setuptools import setup, find_packages
import unittest

import envconfig


def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests/', pattern='test_*.py')
    return test_suite


setup(
    name='pyenvconfig',
    version=envconfig.__version__,
    description='Simple environment variable configuration for Python',
    author='Makram Kamaleddine',
    url='github.com/makramkd/envconfig',
    packages=find_packages(),
    test_suite='setup.test_suite',
)
