from config import Config, TestConfiguration, _Base, set_logger
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from backend.utils.encoder import *
from logging.config import dictConfig


dictConfig(set_logger())

# Define Flask Application.
app = Flask(
    __name__,
    template_folder='frontend/templates',
    static_url_path='/frontend/static',
    static_folder = "frontend/static"
)
cors = CORS(app)

if _Base.ENV == "TESTING":
    print("\nRunning Test Configs")
    app.config.from_object(TestConfiguration)
else:
    print("\nRunning Prod Configs")
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config.from_object(Config)

# Custom JSON Encoder
app.json_provider_class = JSONEncoder

# Configure DB
db = SQLAlchemy(app)

# # Route Imports
# from backend.routes.api import *
# from backend.routes.render import *

# # Model Imports
# from backend.models.models import *

if __name__ == '__main__':
    # Route Imports
    from backend.routes.api import *
    from backend.routes.render import *

    # Model Imports
    from backend.models.models import *
    # import pdb; pdb.set_trace()

    db.create_all()
    app.run(debug=True)
