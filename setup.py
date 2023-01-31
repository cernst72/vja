from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["click", "click-aliases", "requests", "parsedatetime", "python-dateutil"]

setup(
    name="vja",
    version="0.0.11",
    author="Christoph Ernst",
    author_email="christoph.ernst72@googlemail.com",
    description="A simple CLI for Vikunja task manager",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ce72/vja/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={'console_scripts': [
        'vja=vja.cli:cli'
    ]},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
