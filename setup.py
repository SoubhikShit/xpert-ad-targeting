from setuptools import setup, find_packages
import os

# Read the README file if it exists
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "XPERT AD-TARGETING - Automated POS monitoring and OCR processing application"

# Read requirements from requirements.txt
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

setup(
    name="xpert-ad-targeting",
    version="1.0.0",
    author="XPERT Team",
    author_email="support@xpert.chat",
    description="Automated POS monitoring and OCR processing application",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages() + ["Tesseract-OCR"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "xpert-ad-targeting=Project_Xpert:run",
        ],
    },
    include_package_data=True,
    package_data={
        "Project_Xpert": [
            "*.jpeg",
            "*.jpg",
            "*.png",
        ],
        "Tesseract-OCR": [
            "**/*",
        ],
    },
    zip_safe=False,
    keywords="pos monitoring ocr automation gui",
) 