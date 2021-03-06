#!/usr/bin/env python

"""The setup script."""

from setuptools import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

setup(
    author="SpeakinTelnet",
    author_email="gui.lac@protonmail.com",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A python script to sync a Proxmox Backup Server datastore to USB",
    install_requires=requirements,
    license="License :: OSI Approved :: MIT License",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords="pbs2usb",
    name="pbs2usb",
    packages=['pbs2usb', 'pbs2usb._utils'],
    test_suite="tests",
    url="https://github.com/SpeakinTelnet/pbs2usb",
    version="0.1.4",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pbs2usb=pbs2usb.app:main"
        ]
    }
)
