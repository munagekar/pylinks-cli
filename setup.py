import os
from typing import List

from setuptools import setup


def generate_install_requires() -> List[str]:
    # Path agnostic way to open requirements
    abspath = os.path.abspath(__file__)
    project_root = os.path.dirname(abspath)
    req_path = os.path.join(project_root, "requirements.txt")

    with open(req_path) as f:
        required = f.read().splitlines()

    # Remove comments
    return list(filter(lambda x: not x.startswith('#'), required))


setup(
    name='pyli',
    version='0.1.0',
    packages=['pyli'],
    entry_points={
        'console_scripts': [
            'pyli = pyli.__main__:main'
        ],
    },
    install_requires=generate_install_requires(),
)
