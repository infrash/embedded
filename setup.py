from setuptools import setup, find_packages
import os
import re

# Read version from _version.py
with open(os.path.join('src', 'infrash_embedded', '_version.py'), 'r') as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

# Read README.md for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name="infrash_embedded",
    version=version,
    description="Energy optimization tool for embedded systems, particularly MSP430 microcontrollers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tom Softreck",
    author_email="info@softreck.dev",
    url="https://github.com/infrash_embedded/infrash_embedded",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'energy-optimizer=infrash_embedded.cli:main',
        ],
    },
)