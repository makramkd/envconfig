import os
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
    keywords='environment-variables env-var configuration',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    test_suite='setup.test_suite',
    tests_require=[
        'coverage',
        'flake8',
    ],
)
