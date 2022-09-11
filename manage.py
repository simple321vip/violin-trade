import os

from flask_cors import CORS

from app import create_app
from app.trader.violin_trader import run_child
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
CORS(app, supports_credentials=True)
Migrate(app=app)


if __name__ == '__main__':

    run_child()
    app.run(use_reloader=False)

