from setuptools import setup, find_packages

setup(
    name="gmaps_playwright_scraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "playwright",
        "pandas",
        "beautifulsoup4",
        "ollama",
        "langchain",
    ],
    entry_points={
        "console_scripts": [
            "gmaps-scraper=examples.playwright_maps:scrape_google_maps"
        ]
    },
)
