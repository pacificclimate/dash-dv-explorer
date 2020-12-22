import sys
from setuptools import setup, find_packages

setup(
    name="dve",
    description="A climate model hybrid reconstruction tool using station data",
    keywords="geography fields regression climate meteorology",
    packages=find_packages(),
    version="0.1dev",
    url="http://www.pacificclimate.org/",
    author="Nic Annau",
    author_email="nannau@uvic.ca",
    zip_safe=True,
    scripts=[
        "dve/layout.py",
        "dve/generate_iso_lines.py",
        "dve/polygons.py",
        "dve/processing.py",
        "dve/colorbar.py",
    ],
    install_requires=["dash", "shapely", "geopandas", "xarray"],
    package_dir={"dve": "dve"},
    package_data={"climpyrical": ["tests/data/*", "climpyrical/"]},
    classifiers="""

Intended Audience :: Science/Research
License :: GNU General Public License v3 (GPLv3)
Operating System :: OS Independent
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Scientific/Engineering
Topic :: Software Development :: Libraries :: Python Modules""".split(
        "\n"
    ),
)