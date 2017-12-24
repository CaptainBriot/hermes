import os

import setuptools

version = {}
exec(open(os.path.join('pantheon', 'hermes', 'version.py')).read(), version)
tests_require = ['nose', 'coverage', 'pylint']
install_require = []

setuptools.setup(
    name='pantheon-hermes',
    version=version['__version__'],
    description='Crypto-currency mining framework.',
    python_requires='>=3.5',
    packages=setuptools.find_packages(),
    install_require=install_require,
    test_suite='nose.collector',
    tests_require=tests_require,
    extras_require={'test': tests_require, 'all': install_require+tests_require}
)
