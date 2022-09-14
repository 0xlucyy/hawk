import os
from config import Config, logger, TestConfiguration, _Base
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, render_template
from backend.utils.encoder import *

# import pdb; pdb.set_trace()

# Define Flask Application
app = Flask(
    __name__,
    template_folder='frontend/templates',
    static_url_path='/frontend/static',
    static_folder = "frontend/static"
)
cors = CORS(app)

if _Base.ENV == "TESTING":
    app.config.from_object(TestConfiguration)
else:
    # Get Config
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_object(Config)
    logger(app)

# Custom JSON Encoder
app.json_provider_class = JSONEncoder

# Configure DB
db = SQLAlchemy(app)

# Route Imports
# from backend.routes.players import *
from backend.routes.api import *
from backend.routes.render import *

# Model Imports
from backend.models.models import *

if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    db.create_all()
    app.run(debug=True)
