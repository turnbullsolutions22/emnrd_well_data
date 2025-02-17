from flask import Flask, jsonify, request, Response
from shapely.geometry import Point, Polygon
from sqlmodel import Session, SQLModel, create_engine, select

from well import Well

app = Flask(__name__)
engine = create_engine("sqlite:///well_data.db")
SQLModel.metadata.create_all(engine)


@app.route('/well', methods=['GET'])
def get_well() -> tuple[Response, int]:
    """
    Endpoint to retrieve data for a specific well by API number
    Example: /well?api-number=1234567890
    """
    # Get the `api` query parameter
    api_number = request.args.get('api-number', None)

    if api_number is None:
        return jsonify({"error": "API number is required as a query parameter"}), 400

    try:
        # Use SQLModel with a session to query the database
        with Session(engine) as session:
            # Build and execute the query
            query = select(Well).where(Well.api_number == api_number)
            result = session.exec(query).first()

            # If no result found
            if not result:
                return jsonify({"error": f"No well found with API number {api_number}"}), 404

            # Convert the result to a dictionary
            return jsonify(result.dict()), 200

    except Exception as e:
        # Handle unexpected exceptions
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app.route('/wells/in-polygon', methods=['GET'])
def get_wells_in_polygon() -> tuple[Response, int]:
    """
    Fetches API numbers within a specified polygon.
    Example: /wells/in-polygon?coordinates=32.81,-104.19,32.66,-104.32,32.54,-104.24
    """

    try:
        # Get coordinates from query parameter
        coordinates_str = request.args.get('coordinates', None)

        if coordinates_str is None:
            return jsonify({
                "error": "coordinates parameter is required"
            }), 400

        # Parse the coordinates string into list of tuples
        try:
            # Split the string into individual numbers
            coords_list = [float(x) for x in coordinates_str.split(',')]

            # Convert to list of (lat, lon) tuples
            if len(coords_list) % 2 != 0:
                return jsonify({
                    "error": "Invalid coordinates format: odd number of values"
                }), 400

            coordinates = [(coords_list[i], coords_list[i + 1])
                           for i in range(0, len(coords_list), 2)]

            # Verify polygon is closed
            if coordinates[0] != coordinates[-1]:
                coordinates.append(coordinates[0])

        except ValueError:
            return jsonify({
                "error": "Invalid coordinates format. Expected comma-separated numbers"
            }), 400

        # Create polygon and find wells
        polygon = Polygon(coordinates)

        if not polygon.is_valid:
            return jsonify({
                "error": "Invalid polygon: The coordinates do not form a valid polygon"
            }), 400

        # Query wells within polygon
        with Session(engine) as session:
            wells = session.exec(select(Well)).all()
            wells_in_polygon = []

            for well in wells:
                well_point = Point(well.latitude, well.longitude)
                if polygon.contains(well_point):
                    wells_in_polygon.append(well.api_number)

        return jsonify(wells_in_polygon), 200

    except Exception as e:
        return jsonify({
            "error": "An error occurred",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
