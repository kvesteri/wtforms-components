"""
WTForms-Components
------------------

Additional fields, validators and widgets for WTForms.
"""

from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

setup(
    name='WTForms-Components',
    version='0.7.1',
    url='https://github.com/kvesteri/wtforms-components',
    license='BSD',
    author='Konsta Vesterinen',
    author_email='konsta@fastmonkeys.com',
    description='Additional fields, validators and widgets for WTForms.',
    long_description=__doc__,
    packages=[
        'wtforms_components',
        'wtforms_components.fields'
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'WTForms>=1.0.4',
        'SQLAlchemy>=0.8.0',
        'SQLAlchemy-Utils>=0.16.0',
    ],
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
