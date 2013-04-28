from setuptools import setup, find_packages
import os

version = '1.0.1'

setup(name='nsi.granulate',
      version=version,
      description="Granulate Content",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ronaldo Amaral Santos / NSI - CEFETCampos',
      author_email='ronaldinho.as@gmail.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['nsi'],
      package_data = {'': ['template/*.*','data/*.*','data/compared_images/*.*','icons/*.*']},
      include_package_data = True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pypdf2table',
          'nsi.svgtool',
          'openxmllib',
          'plone.memoize',
          'lxml',
          'videoShot'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
