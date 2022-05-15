import os

from dotenv import load_dotenv
from flask import Flask, current_app
from flask_ckeditor import CKEditor

from .database import db

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True,
                )
    ckeditor = CKEditor(app)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        DATABASE=os.path.join(app.instance_path, "dailyUpdates.sqlite"),

    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # initialize the db
    with app.app_context():
        db.initApp(app)

    # ckeditor.init_app(app)

    # from flask_login import LoginManager
    # login_manager = LoginManager()
    # login_manager.init_app(app)

    from .routes import home
    app.register_blueprint(home.bp, name="home")
    app.add_url_rule("/", endpoint="index")

    from .routes import auth
    app.register_blueprint(auth.bp)

    from .routes import dailyNews
    app.register_blueprint(dailyNews.bp)

    from .routes import agency
    app.register_blueprint(agency.bp)

    from .routes import blog
    app.register_blueprint(blog.bp)

    from .routes import portfolio
    app.register_blueprint(portfolio.bp)

    from .routes import about
    app.register_blueprint(about.bp)

    return app
