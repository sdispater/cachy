# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'cachy/version.py')) as f:
        variables = {}
        exec(f.read(), variables)

        version = variables.get('VERSION')
        if version:
            return version

    raise RuntimeError('No version info found.')


__version__ = get_version()

# Recommended extra packages
recommended = {
    'redis': ['redis'],
    'memcached': ['python-memcached'],
    'memcachedc': ['pylibmc'],
    'memcachedpy3': ['python3-memcached']
}

setup(
    name='cachy',
    license='MIT',
    version=__version__,
    description='Cachy provides a simple yet effective caching library.',
    long_description=open('README.rst').read(),
    author='Sébastien Eustace',
    author_email='sebastien.eustace@gmail.com',
    url='https://github.com/sdispater/cachy',
    download_url='https://github.com/sdispater/cachy/archive/%s.tar.gz' % __version__,
    packages=find_packages(),
    install_requires=[],
    tests_require=['pytest', 'mock', 'flexmock'],
    test_suite='nose.collector',
    extras_require=recommended,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
