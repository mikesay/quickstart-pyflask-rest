# -*- coding: UTF-8 -*-
import os
from flask import Flask, Blueprint, url_for
from flask_cors import CORS #https://flask-cors.readthedocs.io/en/2.1.0/
from api import settings
from api.endpoints.jenkins_job import ns as jenkins_job_namespace
from api.endpoints.health import ns as health_namespace
from api.restplus import api
from flask_restplus import apidoc
from utils.common_utils import LogUtil

app = Flask(__name__)
CORS(app)

LogUtil.init_root_logger("api")
app_logger = LogUtil.get_named_logger("api")


def configure_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/pyapi')
    api.init_app(blueprint)
    api.add_namespace(jenkins_job_namespace)
    api.add_namespace(health_namespace)
    flask_app.register_blueprint(blueprint)

    custom_apidoc = apidoc.Apidoc('restplus_custom_doc', __name__,
                                  template_folder='templates',
                                  static_folder=os.path.dirname(apidoc.__file__) + '/static',
                                  static_url_path='/')
    
    @custom_apidoc.add_app_template_global
    def swagger_static(filename):
        return url_for('restplus_custom_doc.static', filename=filename)
    
    flask_app.register_blueprint(custom_apidoc, url_prefix='/pyapi/ui')

initialize_app(app)

if __name__ == "__main__":
    server_name = "{}:{}".format(settings.FLASK_SERVER_HOST,settings.FLASK_SERVER_PORT)
    app_logger.info('>>>>> Starting development server at http://{}/pyapi/ <<<<<'.format(server_name))
    app.config['SERVER_NAME'] = server_name
    app.run(debug=True)
