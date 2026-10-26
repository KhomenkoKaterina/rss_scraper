# Command-Line RSS Reader

A pure Python command-line utility to fetch, parse, and read RSS feeds. It extracts information from standard XML RSS feeds and can output the results in a readable text format or as structured JSON.

## Features
* **Direct Fetching:** Fetches RSS feeds directly via URL using HTTP requests.
* **Metadata Extraction:** Parses channel metadata (Title, Link, Description, Publish Date, Categories, etc.).
* **Item Parsing:** Extracts individual news items (Title, Author, Date, Link, Description, Categories).
* **Data Cleaning:** Automatically unescapes HTML entities for clean text output.
* **Limit Results:** Supports limiting the number of displayed news items.
* **JSON Export:** Optional JSON output for easy integration into data pipelines or further processing.

## Requirements
* Python 3.8+
* `requests` library

### Installation
1. Clone the repository or download the `rss_reader.py` script.
2. Install the required dependencies:
   ```bash
   pip install requests
