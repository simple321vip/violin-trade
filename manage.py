import os

from app import create_app
from app.trader import Test
from flask_migrate import Migrate
import multiprocessing

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
Migrate(app=app)

if __name__ == '__main__':
    parent_process = multiprocessing.Process(target=Test. test)
    parent_process.start()
    # run_parent()
    app.run()
