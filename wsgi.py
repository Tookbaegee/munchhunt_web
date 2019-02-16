# NOTE: This file is for running on a production server. When running in a development environment,
# the FLASK_APP environment variable must be set to 'fsite.py'. 
from fsite import app

if __name__ == "__main__":
    app.run()
