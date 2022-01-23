from setuptools import setup

from os import path

with open(
    path.join(path.abspath(path.dirname(__file__)), "README.md"),
    encoding="utf-8",
) as f:
    long_description = f.read()

setup(
    name="djsp",
    version="0.1.0",
    author="Cesar Godoi",
    author_email="cesar.godoi@gmail.com",
    packages=["djsp"],
    package_dir={"djsp": "djsp"},
    include_package_data=True,
    description="Django Start Project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cesargodoi/djsp",
    project_urls={
        "source code": "https://github.com/cesargodoi/djsp",
    },
    license="GNU GPLv3",
    entry_points={"console_scripts": ["djsp=djsp.cli:main"]},
    install_requires=["jinja2", "Click"],
)
