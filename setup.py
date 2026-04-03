from pathlib import Path

from setuptools import find_packages, setup


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="maybankpdf2json",
    version="0.1.53",
    author="Nordin",
    author_email="vipnordin@gmail.com",
    description="A package for extracting JSON data from Maybank PDF account statements",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nordinz7/maybankpdf2json",
    packages=find_packages(),
    install_requires=("pdfplumber>=0.7.4",),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
