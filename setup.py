#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
setup(
    name='ciscotator',
    version='0.1',
    description='Cisco configuration scripting with ssh and serial support',
    long_description=open('README.md').read(),
    url='https://github.com/gcmalloc/ciscotator',
    author='gcmalloc',
    author_email='gcmalloc@gmail.com',
    packages=[
        'ciscotator',
        'ciscotator.con'],
)
