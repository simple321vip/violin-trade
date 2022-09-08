import os

from app import create_app
from app.trader.violin_trader import run_parent
from flask_migrate import Migrate
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(1)

executor.submit(run_parent)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
Migrate(app=app)


if __name__ == '__main__':
    app.run()
