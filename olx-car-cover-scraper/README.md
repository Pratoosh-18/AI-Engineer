# OLX Car Cover Scraper

A Python script that scrapes car cover listings from OLX India and saves the results to JSON or CSV files.

## Features

- Searches OLX for car covers (or any other specified query)
- Extracts listing details: title, price, location, date posted, link, and image URL
- Handles pagination to scrape multiple pages of results
- Saves results in either JSON or CSV format
- Includes rate limiting to be respectful to the OLX website

## Requirements

- Python 3.6+
- Required packages: `requests`, `beautifulsoup4`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pratoosh-18/AI-Engineer.git
cd olx-car-cover-scraper
```

2. Set up a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script with default parameters:

```bash
python olx_car_cover_scraper.py
```

This will:
- Search for "car-cover" on OLX India
- Scrape up to 3 pages of results
- Save the results to a JSON file

### Advanced Usage

Customize the search with command-line arguments:

```bash
python olx_car_cover_scraper.py --query "car cover waterproof" --pages 5 --format csv
```

Available arguments:
- `--query`: Search term (default: "car-cover")
- `--pages`: Maximum number of pages to scrape (default: 3)
- `--format`: Output file format, either "json" or "csv" (default: "json")

## Output

The script generates files named in this format:
- `olx_[query]_[timestamp].[format]`

Example:
- `olx_car-cover_20250509_143022.json`

### JSON Format Example

```json
{
  "search_date": "2025-05-09 14:30:22",
  "total_results": 25,
  "listings": [
    {
      "title": "Premium Waterproof Car Cover",
      "price": "₹1,499",
      "location": "Bangalore, Karnataka",
      "date_posted": "Today",
      "link": "https://www.olx.in/item/premium-waterproof-car-cover-ID2345678",
      "image_url": "https://images.olx.in/images/car-cover-123.jpg"
    },
    ...
  ]
}
```

### CSV Format

The CSV output includes the same fields as columns: title, price, location, date_posted, link, and image_url.

## Legal Considerations

Please note that web scraping might be against the terms of service of some websites. This tool is provided for educational purposes only. Use it responsibly and consider the following:

1. Check OLX's robots.txt file and terms of service
2. Use reasonable rate limiting (already implemented in the script)
3. Do not overload the website with too many requests
4. Use the data only for personal, non-commercial purposes

## Limitations

- The script might break if OLX changes their website structure
- OLX might implement measures to prevent scraping
- Some advanced filtering options from the OLX website are not implemented

## Future Improvements

- Add proxy support for distributed scraping
- Implement more advanced filtering options
- Add support for scraping detailed product pages
- Create a command-line interface for easier usage

## License

MIT License