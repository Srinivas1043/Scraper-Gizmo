from setuptools import setup, find_packages

setup(
    name="gmaps_playwright_scraper",          # Required
    version="0.1.0",                           # Required
    author="Srinivas Muralidharan",
    description="Scraper using Playwright + LLaMA to extract Google Maps results",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "playwright",
        "pandas",
        "beautifulsoup4",
        "ollama",
        "langchain"
    ],
)
