from setuptools import setup, find_packages
from os.path import dirname
from os.path import realpath
from os.path import join
import io


def open_config_file(*names, **kwargs):
    current_dir = dirname(realpath(__file__))
    return io.open(
        join(current_dir, *names),
        encoding=kwargs.get('encoding', 'utf8')
    )

install_dependencies = open_config_file('requirements.txt').read().splitlines()

setup(
    name='Hawk',
    version='0.1.0',
    author='escobar',
    description='provide insight into ens domains',
    packages=find_packages(),
    install_requires=install_dependencies,
    entry_points={
        'console_scripts': [
            "build_watchlist = backend.src.scripts:build_watchlist",
            "clean_file = backend.src.scripts:clean_file",
            "create_database = backend.src.scripts:create_database",
            "populate_domains = backend.src.scripts:populate_domains",
            # "update_domains = backend.src.scripts:update_domains",
            # "refresh_domains = backend.src.scripts:refresh_domains",            
            "populate_markets = backend.src.scripts:populate_markets",
            "clean_slate = backend.src.scripts:clean_slate",
        ]
    }
)
