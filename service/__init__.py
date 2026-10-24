import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)

# Set up security headers using Flask-Talisman
talisman = Talisman(app)

# Set up Cross-Origin Resource Sharing (CORS) policies
CORS(app)

# Load configuration
app.config.from_object("service.config")

# Import the routes after app is created
from service import routes, models, common  # noqa: E402, F401

# Set up logging for production using init_logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # Make sure database tables exist
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")