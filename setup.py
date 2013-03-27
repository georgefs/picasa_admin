#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages
import picasa_admin as distmeta

setup(
    version=distmeta.__version__,
    description=distmeta.__doc__,
    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    url=distmeta.__homepage__,
    #
    name='picasa_admin',
    packages=find_packages(),
    install_requires=[
        'django-ztask==0.1.5',
        'gdata==1.3.3',
    ]
)
