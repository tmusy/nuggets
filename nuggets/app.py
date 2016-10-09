import os

from flask.app import Flask
from flask_restful import Api

from nuggets.config import DefaultConfig
from nuggets.extensions import db
from nuggets.api.account import AccountResource, AccountListResource
from nuggets.api.transaction import TransactionResource, TransactionListResource
from nuggets.api.upload import ImportTransactionsResource


# For import *
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
#     user,
)


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, static_url_path='', instance_path=DefaultConfig.INSTANCE_FOLDER_PATH, instance_relative_config=True)
    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_routes(app)
    configure_api(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)

    # Use instance folder instead of env variables to make deployment easier.
    #app.config.from_envvar('%s_APP_CONFIG' % DefaultConfig.PROJECT.upper(), silent=True)


def configure_extensions(app):
    # flask-sqlalchemy
    # configures the flask app to support SQLAlchemy
    db.init_app(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    from logging.handlers import SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)

    # Testing
    #app.logger.info("testing info.")
    #app.logger.warn("testing warn.")
    #app.logger.error("testing error.")

    mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
                               app.config['MAIL_USERNAME'],
                               app.config['ADMINS'],
                               'O_ops... %s failed!' % app.config['PROJECT'],
                               (app.config['MAIL_USERNAME'],
                                app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(mail_handler)


def configure_hook(app):
    @app.before_first_request
    def create_db():
        pass

    @app.before_request
    def before_request():
        pass


def configure_routes(app):
    """
    Configure routes:
        - home on /
        - token on /api/token

    :param app: Flask app
    """
    @app.route('/')
    def root():
        return app.send_static_file('index.html')


def configure_api(app):
    """

    :param app:
    :return:
    """
    api = Api(app, prefix='/api')
    api.add_resource(AccountListResource, '/v1.0/accounts', endpoint='accounts')
    api.add_resource(AccountResource, '/v1.0/accounts/<string:id>', endpoint='account')
    api.add_resource(TransactionListResource, '/v1.0/transactions', endpoint='transactions')
    api.add_resource(TransactionResource, '/v1.0/transactions/<string:id>', endpoint='transaction')
    api.add_resource(ImportTransactionsResource, '/v1.0/import/transactions', endpoint='import')


def configure_error_handlers(app):
    pass
    # @app.errorhandler(403)
    # def forbidden_page(error):
    #     return render_template("errors/forbidden_page.html"), 403
    #
    # @app.errorhandler(404)
    # def page_not_found(error):
    #     return render_template("errors/page_not_found.html"), 404
    #
    # @app.errorhandler(500)
    # def server_error_page(error):
    #     return render_template("errors/server_error.html"), 500


if __name__ == '__main__':
    app = create_app()
    app.run()
