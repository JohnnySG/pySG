#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Johnny
# @Date:   2016-05-21 14:36:50
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-20 15:35:18
# ----------------------------------------

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pysg',
      version='0.1',
      description='Finite Element Routine for Shear Lag',
      long_description=readme(),
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Finite Element Analysis :: Beam'],
      keywords='FEA, shear lag',
      url='http://github.com/storborg/funniest',
      author='Johnny Song',
      author_email='sg19910914@gmail.com',
      license='MIT',
      packages=['pysg'],
      install_requires=['numpy'],
      # dependency_links=[
      #     'http://github.com/user/repo/tarball/master#egg=package-1.0'
      # ],
      test_suite='nose.collector',
      tests_require=['nose'],
      # scripts=['bin/funniest-joke.py'],
      # entry_points={
      #     'console_scripts': ['funniest-joke=funniest.command_line:main'],
      # },
      include_package_data=True,
      # library_dirs=['/usr/X11R6/lib'],
      # libraries=['X11', 'Xt'],
      zip_safe=False)
