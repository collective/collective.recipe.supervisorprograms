# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1.0'

long_description = '\n'.join([
    read('README.rst'),
    read('docs', 'HISTORY.rst')
])

tests_require = [
    'zc.buildout[test]',
    'zope.testing',
]


setup(
    name='collective.recipe.supervisorprograms',
    version=version,
    description='Offers a new syntax to configure collective.recipe.supervisor',
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='zc.buildout buildout recipe supervisor',
    author='Rafael Oliveira',
    author_email='rafaelbco@gmail.com',
    url='http://pypi.python.org/pypi/collective.recipe.supervisorprograms',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
    ],
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    test_suite='collective.recipe.supervisorprograms.tests.test_docs.test_suite',
    entry_points={
        'zc.buildout': [
            'default = collective.recipe.supervisorprograms:Recipe',
            'multiplier = collective.recipe.supervisorprograms:MultiplierRecipe',
            'printer = collective.recipe.supervisorprograms:PrinterRecipe',
        ]},
)
