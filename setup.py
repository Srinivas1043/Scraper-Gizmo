from setuptools import setup, find_packages

setup(
    name="gmaps_scraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.15.0",
        "beautifulsoup4>=4.12.0",
        "webdriver-manager>=4.0.0",
        "pandas>=2.0.0",
        "requests>=2.31.0",
    ],
    author="Srinivas Muralidharan",
    author_email="sm1043@gmail.com",
    description="A Python library for scraping data from Google Maps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/srinivas1043/gmaps_scraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 