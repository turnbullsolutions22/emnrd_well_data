# Oil & Gas Well Data Scraper and API

This project provides tools for scraping oil and gas well data from the New Mexico Energy, Minerals and Natural Resources Department website and exposing it through a REST API.

## Project Overview

The project consists of three main parts:

1. **Data Collection** - Dataset retrieval from Google Cloud Storage
2. **Web Scraping** - Collecting well data and storing it in SQLite
3. **REST API** - Flask endpoints to query the well data

## Prerequisites

- Python 3.13
- Google Cloud CLI (gsutil)
- Google authenticated email address

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

- `api.py` - Flask API implementation
- `api_numbers.csv` - Initial CSV data containing list of APIs to scrape
- `polygon_results.csv` - Sample polygon search results
- `requirements.txt` - Project dependencies
- `scraper.py` - Web scraping and database loading logic
- `well.py` - SQLModel `Well` class to manage well-related attributes and database interactions
- `well_data.db` - SQLite database containing scraped data

## Usage

### 1. Data Collection

Contact <redacted> with your Google authenticated email to receive the dataset download link.

### 2. Web Scraping

The scraper collects the following data points for each well:
- Operator
- Status
- Well Type
- Work Type
- Directional Status
- Multi-Lateral
- Mineral Owner
- Surface Owner
- Surface Location
- GL Elevation
- KB Elevation
- DF Elevation
- Single/Multiple Completion
- Potash Waiver
- Spud Date
- Last Inspection
- TVD (True Vertical Depth)
- API
- Latitude
- Longitude
- CRS (Coordinate Reference System)

### 3. API Endpoints

#### Get Well Data
```
GET /well?api={api_number}
```
Returns all available data for a specific well API number.

#### Polygon Search
```
GET /polygon?coordinates={coordinates}
```
Returns API numbers for wells located within the specified polygon coordinates.

## Example Polygon Query

The following polygon coordinates can be used to test the API:
```python
[
    (32.81,-104.19),
    (32.66,-104.32),
    (32.54,-104.24),
    (32.50,-104.03),
    (32.73,-104.01),
    (32.79,-103.91),
    (32.84,-104.05),
    (32.81,-104.19)
]
```

## Contributing

Please ensure your code follows these quality guidelines:
- Proper function and class usage
- Clear documentation
- Code readability
- Appropriate error handling

## License

MIT License

Copyright (c) 2025 turnbullsolutions22