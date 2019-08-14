from setuptools import setup, find_packages

setup(
    name="misc-downloaders",
    version="0.1",
    packages=find_packages(),
    install_requires=["Click"],
    entry_points="""
    [console_scripts]
    misc_downloaders=cli:cli
    """)
