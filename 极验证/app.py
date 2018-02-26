from flask import Flask
from datetime import timedelta
from flask_cache import Cache
from routes.index import main as routes_index


def configured_app():
    app = Flask(__name__)
    app.register_blueprint(routes_index)
    app.secret_key = 'cnd1fvfd'
    app.permanent_session_lifetime = timedelta(days=3)
    return app


cache = Cache(configured_app(), config={'CACHE_TYPE': 'simple'})


if __name__ == '__main__':
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
        threaded=True,
    )
    app.run(**config)
