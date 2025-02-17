import datetime as dt

from typing import Optional
from sqlmodel import Field, SQLModel


class Well(SQLModel, table=True):
    """
    Represents a Well database model for storing and retrieving well-related information
    """
    __tablename__ = "api_well_data"

    id: Optional[int] = Field(default=None, primary_key=True)
    api_number: str
    operator_name: Optional[str]
    operator_id: Optional[int]
    status: Optional[str]
    well_type: Optional[str]
    work_type: Optional[str]
    directional_status: Optional[str]
    multi_lateral: Optional[str]
    mineral_owner: Optional[str]
    surface_owner: Optional[str]
    surface_location: Optional[str]
    gl_elevation: Optional[float]
    kb_elevation: Optional[float]
    df_elevation: Optional[float]
    single_mult_completion: Optional[str]
    potash_waiver: Optional[str]
    spud_dt: Optional[dt.date]
    last_inspection_dt: Optional[dt.date]
    tvd: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]
    crs: Optional[str]

    @property
    def div_map(self) -> dict:
        return {
            "operator": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblOperator",
            "status": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblStatus",
            "well_type": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblWellType",
            "work_type": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblWorkType",
            "directional_status": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblDirectionalStatus",
            "multi_lateral": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblMultiLateral",
            "mineral_owner": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblMineralOwner",
            "surface_owner": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblSurfaceOwner",
            "surface_location": "ctl00_ctl00__main_main_ucGeneralWellInformation_Location_lblLocation",
            "gl_elevation": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblGLElevation",
            "kb_elevation": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblKBElevation",
            "df_elevation": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblDFElevationLabel",
            "single_mult_completion": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblCompletions",
            "potash_waiver": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblPotashWaiver",
            "spud_dt": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblSpudDate",
            "last_inspection_dt": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblLastInspectionDate",
            "tvd": "ctl00_ctl00__main_main_ucGeneralWellInformation_lblTrueVerticalDepth",
            "coordinates": "ctl00_ctl00__main_main_ucGeneralWellInformation_Location_lblCoordinates",
            "crs": "",
        }

    def __setattr__(self, attr, value):
        """
        Sets an attribute to the given value and applies any necessary transformations
        """
        # Convert date strings to datetime objects
        if attr == "spud_dt" or attr == "last_inspection_dt":
            value = self.parse_dt(value)

        # Convert number strings to floats
        elif attr == "gl_elevation" or attr == "kb_elevation" or attr == "df_elevation" or attr == "tvd":
            value = float(value) if value else None

        # Transform coordinate string to latitude/longitude values
        elif attr == "coordinates":
            self.parse_coordinates(value)
            return

        # Split the operator name and id
        elif attr == "operator":
            self.parse_operator(value)
            return

        if value:
            super().__setattr__(attr, value)

    @staticmethod
    def parse_dt(value: str) -> dt.date | None:
        """
        Parses a date string in the format 'MM/DD/YYYY' and converts it into a date object
        """
        value_dt = None
        if value:
            try:
                # Try to convert value into a `date` object
                value_dt = dt.datetime.strptime(value.strip(), "%m/%d/%Y").date()
            except ValueError:
                print(f"Failed to parse date from string: '{value}'")
            else:
                return value_dt

    def parse_coordinates(self, coordinates: str) -> None:
        """
        Parses a coordinate string and extracts latitude and longitude values
        """
        if not coordinates:
            return

        try:
            lat, lon = coordinates.split(",")
            if ' ' in lon:
                lon, _ = lon.split(" ")

        except ValueError:
            print(f"Failed to parse coordinates: '{coordinates}'")
            return

        try:
            self.latitude = float(lat)
            self.longitude = float(lon)
        except ValueError:
            print(f"Failed to convert coordinates to float: '{lat}', '{lon}'")
            return
        except TypeError:
            print(f"Failed to convert coordinates to float: '{lat}', '{lon}'")
            return

    def parse_operator(self, operator: str) -> None:
        """
        Parses a given operator string into an operator name and ID
        """
        if not operator:
            return
        try:
            op = operator.split('] ')
            self.operator_name = op[1]
            self.operator_id = int(op[0][1:])
        except ValueError:
            print(f"Failed to parse operator: '{operator}'")
            return
        except IndexError:
            print(f"Failed to parse operator: '{operator}'")
            return
