from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = [
    "click>=8.1",
    "click-aliases>=1",
    "requests>=2.32",
    "parsedatetime>=2.6",
    "python-dateutil>=2.8"
]

setup(
    name="vja",
    author="ce72",
    description="A simple CLI for Vikunja task manager",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ce72/vja",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={'console_scripts': [
        'vja=vja.cli:cli'
    ]},
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
