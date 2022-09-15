from pathlib import Path
from typing import List

from setuptools import setup

from flake8_hangover import __version__

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()


def get_install_requires() -> List[str]:
    """Get list of required packages from Pipfile."""
    with open('Pipfile', 'r') as f:
        pipfile = f.read()
    lines = pipfile.split('[packages]', 1)[1].split('[dev-packages]', 1)[0]
    pkg_lines = list(filter(None, map(lambda x: x.split('#', 1)[0].strip(), lines.splitlines())))
    return list(map(lambda x: x.replace(' = "*"', ''), pkg_lines))


setup(
    name='flake8-hangover',
    version=__version__,
    description='flake8 plugin to prevent specific hanging indentations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/deniskrumko/flake8-hangover',
    install_requires=get_install_requires(),
    author='dkrumko@gmail.ru',
    packages=['flake8_hangover'],
    package_data={
        'flake8_hangover': ['py.typed'],
    },
    python_requires=">=3.8",
    license='MIT',
    entry_points={
        'flake8.extension': ['FHO = flake8_hangover:Plugin', ],
    },
)
