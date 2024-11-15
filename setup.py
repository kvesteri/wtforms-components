"""
WTForms-Components
------------------

Additional fields, validators and widgets for WTForms.
"""

import os
import re

from setuptools import setup

HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, "wtforms_components", "__init__.py")
    with open(filename) as f:
        contents = f.read()
    pattern = r'^__version__ = "(.*?)"$'
    return re.search(pattern, contents, re.MULTILINE).group(1)


extras_require = {
    "test": [
        "pytest>=2.2.3",
        "flexmock>=0.9.7",
        "ruff==0.7.3",
        "WTForms-Test>=0.1.1",
    ],
    "color": ["colour>=0.0.4"],
    "ipaddress": [],
    "timezone": ["python-dateutil"],
}


# Add all optional dependencies to testing requirements.
for name, requirements in extras_require.items():
    if name != "test":
        extras_require["test"] += requirements


setup(
    name="WTForms-Components",
    version=get_version(),
    url="https://github.com/kvesteri/wtforms-components",
    license="BSD",
    author="Konsta Vesterinen",
    author_email="konsta@fastmonkeys.com",
    description="Additional fields, validators and widgets for WTForms.",
    long_description=__doc__,
    packages=["wtforms_components", "wtforms_components.fields"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "WTForms>=3.1.0",
        "validators>=0.21",
        "intervals>=0.6.0",
        "MarkupSafe>=1.0.0",
    ],
    extras_require=extras_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
)
