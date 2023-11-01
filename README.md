# sqlalchemy-challenge
# Climate App API with Flask
This Flask-based API provides climate data, including temperature statistics, precipitation, and station information for Hawai.

# Features
Retrieve precipitation data for the last 12 months.
Get a list of climate monitoring stations.
Calculate temperature statistics (minimum, average, and maximum) for specified date ranges.

# Getting Started
## Prerequisites
Python 3.x
Required Python packages (Flask, SQLAlchemy, Pandas)

## Installation
Clone the repository.
Navigate to the project directory.
Run the Flask app using python app.py.

# Usage
/api/v1.0/precipitation
Retrieve precipitation data.

/api/v1.0/stations
Get a list of climate monitoring stations.

/api/v1.0/<start> and /api/v1.0/<start>/<end>
Calculate temperature statistics for specified date ranges. Handles date format validation.

Contributing
Contributions are welcome! Report issues or submit pull requests.
