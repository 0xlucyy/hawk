from config import Config, TestConfiguration, _Base, set_logger
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from backend.utils.encoder import JSONEncoder
from logging.config import dictConfig
# import pdb; pdb.set_trace()


# Set logging conditions
# https://flask.palletsprojects.com/en/2.2.x/logging/#basic-configuration
dictConfig(set_logger())

# Define Flask Application.
app = Flask(
    __name__,
)
cors = CORS(app)

if _Base.ENV == "live":
    app.logger.info("Running Prod Configs")
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_object(Config)
else:
    app.logger.info("Running Test Configs")
    app.config.from_object(TestConfiguration)

# Configure DB
db = SQLAlchemy(app)

if __name__ == '__main__':
    # Route Imports
    from backend.routes.api import *
    from backend.routes.render import *

    # Model Imports
    from backend.models.models import *

    # Create all tables.
    db.create_all()

    # Custom JSON Encoder.
    app.json_encoder = JSONEncoder
    # app.json_provider_class = JSONEncoder 
    # app.json = JSONEncoder

    app.run(debug=True)
