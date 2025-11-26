#!/usr/bin/env python3
"""
Setup script for Arch Linux AI CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().strip().split('\n')

setup(
    name="archlinux-ai-cli",
    version="1.0.0",
    description="An intelligent CLI assistant for Arch Linux using AI and Arch Wiki",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dacraezy1",
    url="https://github.com/Dacraezy1/archlinux-ai-cli",
    py_modules=["archlinux-ai-cli"],
    install_requires=requirements,
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "archlinux-ai-cli=archlinux-ai-cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    keywords="arch linux cli ai assistant troubleshooting wiki pacman",
    project_urls={
        "Bug Reports": "https://github.com/Dacraezy1/archlinux-ai-cli/issues",
        "Source": "https://github.com/Dacraezy1/archlinux-ai-cli",
        "Documentation": "https://github.com/Dacraezy1/archlinux-ai-cli#readme",
    },
)
