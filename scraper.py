from bs4 import BeautifulSoup
import requests
from sqlmodel import Session, SQLModel, create_engine, select
import sqlalchemy.exc
import sqlalchemy.orm.exc
from time import sleep
import traceback

from well import Well


engine = create_engine("sqlite:///well_data.db")
SQLModel.metadata.create_all(engine)

def scrape_well_data(api_number: str) -> BeautifulSoup | None:
    """
    Scrape well data from New Mexico Energy, Minerals, and Natural Resources Department
    """
    url = "https://wwwapps.emnrd.nm.gov/OCD/OCDPermitting/Data/WellDetails.aspx"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    params = {
        'api': api_number
    }

    try:
        # Make the request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        # Parse the HTML
        well_data = BeautifulSoup(response.text, 'html.parser')


    except requests.exceptions.RequestException as e:
        print(f"A request error occurred while scraping the well data for API number {api_number}: {e}"
              f"{traceback.format_exc()}")

    except Exception as e:
        print(f"An error occurred while scraping the well data for API number {api_number}: {e}"
              f"{traceback.format_exc()}")

    else:
        print(f"Scraped the well data for API number {api_number}")
        return well_data


def parse_well_data(well_data: BeautifulSoup, api_number: str) -> Well | None:
    """
    Parses well data from scrape and extracts attributes to map them to a Well object
    """
    if not well_data:
        return None

    try:
        # Initialize Well object
        well = Well(api_number=api_number)

        for attr, div in well.div_map.items():
            # Find element by ID
            value = well_data.find("span", id=div)
            if value:
                setattr(well, attr, value.get_text(strip=True))
            else:
                setattr(well, attr, None)

    except Exception as e:
        print(f"An error occurred while parsing the well data for API number {api_number}: {e}"
              f"{traceback.format_exc()}")
        return None

    else:
        print(f"Parsed the well data for API number {well.api_number}")
        return well


def save_well_data(well: Well) -> Well | None:
    """
    Saves well data into the database, updating existing records if necessary
    """
    try:
        with Session(engine) as session:
            # Check if the well already exists
            statement = select(Well).where(Well.api_number == well.api_number)
            well_exists = session.exec(statement).first()

            # UPSERT the well data
            if well_exists:
                well.id = well_exists.id
                session.merge(well)
            else:
                session.add(well)

            session.commit()

            well_upserted = session.exec(statement).first()

    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"A SQLAlchemy error occurred while saving the well data for API number {well.api_number}: {e}"
              f"{traceback.format_exc()}")

    except Exception as e:
        print(f"An error occurred while saving the well data for API number {well.api_number}: {e}"
              f"{traceback.format_exc()}")

    else:
        print(f"Saved the well data for API number {well_upserted.api_number}")
        return well_upserted

def main() -> None:
    """
    Reads API numbers from a CSV file, scrapes well data for each API number, parses the data,
    and saves the processed well information
    """
    try:
        with open('api_numbers.csv', 'r', encoding='utf-8-sig') as file:
            api_numbers = file.read().splitlines()

        for api_number in api_numbers:
            well_data = scrape_well_data(api_number)

            if not well_data:
                raise Exception(f"Failed to scrape well data for API number {api_number}")

            well = parse_well_data(well_data, api_number)

            if not well:
                raise Exception(f"Failed to parse well data for API number {api_number}")
            save_well_data(well)

            # We don't want to hammer the API (in this case it is not actually an API)
            sleep(1)

    except Exception as e:
        print(f"An error occurred while saving the well data for API number {well.api_number}: {e}"
              f"{traceback.format_exc()}")

if __name__ == "__main__":
    main()