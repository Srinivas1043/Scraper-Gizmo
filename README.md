# Google Maps Scraper

A powerful and easy-to-use Python library for scraping data from Google Maps. This library allows you to extract various types of information including business details, reviews, ratings, and more.

## Features

- Search for businesses by location and keywords
- Extract business information (name, address, phone, website, etc.)
- Collect customer reviews and ratings
- Export data to various formats (CSV, JSON)
- Configurable browser automation
- Rate limiting and proxy support
- Error handling and retry mechanisms

## Installation

```bash
pip install gmaps_scraper
```

## Quick Start

```python
from gmaps_scraper import GoogleMapsScraper

# Initialize the scraper
scraper = GoogleMapsScraper()

# Search for businesses
results = scraper.search(
    query="restaurants",
    location="New York, NY",
    limit=10
)

# Get detailed information for each business
for business in results:
    details = scraper.get_business_details(business['place_id'])
    print(details)
```

## Usage Examples

### Search for Businesses

```python
# Basic search
results = scraper.search(
    query="coffee shops",
    location="San Francisco, CA",
    limit=5
)

# Advanced search with filters
results = scraper.search(
    query="hotels",
    location="Paris, France",
    limit=10,
    min_rating=4.0,
    open_now=True
)
```

### Get Business Details

```python
# Get comprehensive business information
details = scraper.get_business_details(place_id="ChIJ...")
print(details)
```

### Collect Reviews

```python
# Get reviews for a business
reviews = scraper.get_reviews(
    place_id="ChIJ...",
    limit=100,
    min_rating=3
)
```

## Configuration

The scraper can be configured with various options:

```python
scraper = GoogleMapsScraper(
    headless=True,  # Run browser in headless mode
    proxy="http://your-proxy:8080",  # Use proxy
    timeout=30,  # Set timeout in seconds
    retry_count=3  # Number of retries on failure
)
```

## Rate Limiting

The library implements rate limiting to avoid being blocked:

- Default delay between requests: 2 seconds
- Configurable delays and randomization
- Automatic retry on detection of rate limiting

## Error Handling

The library includes comprehensive error handling:

- Automatic retry on common errors
- Custom exceptions for different error types
- Detailed error messages and logging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Be sure to read and comply with Google Maps' terms of service before use.


