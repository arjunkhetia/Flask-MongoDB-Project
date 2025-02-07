from flask import Flask, render_template, json
# from utilities.logger import logger
import flask_monitoringdashboard as dashboard
# from random import randint
from flask_compress import Compress
from flask_cors import CORS
from routes import register_routes
from werkzeug.exceptions import HTTPException
from flasgger import Swagger
import configparser

compress = Compress()

app = Flask(__name__)
CORS(app)
compress.init_app(app)

# Load configuration from a .cfg file
config = configparser.ConfigParser()
config.read("config/app-config.cfg")

# Apply config values to Flask app
app.config["SECRET_KEY"] = config["DEFAULT"]["SECRET_KEY"]
app.config["DEBUG"] = config.getboolean("DEFAULT", "DEBUG")

# Read host and port from config
host = config["SERVER"]["HOST"]
port = config.getint("SERVER", "PORT")  # Convert to integer

dashboard.config.init_from(file='config/dashboard-config.cfg')

# Add new graph to monitoring dashboard
# def numberOfNewCustomers():
#     return float(randint(1,5))
# numberOfNewCustomers_schedule = {'seconds': 10}
# dashboard.add_graph("Every 10 Seconds", numberOfNewCustomers, "interval", **numberOfNewCustomers_schedule)

# showing different logging levels
# logger.debug("debug log info")
# logger.info("Info log information")
# logger.warning("Warning log info")
# logger.error("Error log info")
# logger.critical("Critical log info")

@app.route("/")
def home():
    return render_template("index.html", data={
        'title': "Home Page",
        'message': "Welcome to Flask!",
        'array': ['1', '2', '3', '4', '5'],
        'user': "Arjun Khetia"
    })

# Register blueprints (modular routes)
register_routes(app)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,  # All rules included
            "model_filter": lambda tag: True,  # All models included
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Server API",
        "description": "API for flask server",
        "version": "1.0.0",
        "contact": {
            "responsibleOrganization": "EmanciTech",
            "responsibleDeveloper": "Arjun Khetia",
            "email": "arjunkhetia@gmail.com",
            "url": "https://arjunkhetia.me",
        },
    },
    "host": "localhost:5000",
    "schemes": ["http", "https"],
    "basePath": "/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

# Initialize Swagger for API documentation
swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Generic Exception Handlers
@app.errorhandler(HTTPException)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

dashboard.bind(app)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=app.config["DEBUG"])  # Enables auto-reload