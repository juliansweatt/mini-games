# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="PlethoraPy",
    version="0.1dev",
    description="Nostalgic games from the pre- and early-internet wrapped in a pygame UI",
    author="Dylan McClure, Lucas Zavalía, Julian Sweatt, Caleb Smith, Michael Heron",
    url="https://github.com/juliansweatt/mini-games",
    license="MIT",
    include_package_data=True,
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={ "console_scripts": ["plethora = arcade.plethoraAPI:main"], },
    install_requires=[ "pygame", ],
)

