"""
This program builds a blank sqlite db file.
"""

from pathlib import Path
import logging
from sqlalchemy import create_engine
from modules.models import Base

def init_db():
    db_file = Path('test.db')
    if db_file.exists():
        logging.error('db file already exists. Do nothing and quit.')
        return

    engine = create_engine(f'sqlite:///{db_file}', echo=True)
    Base.metadata.create_all(engine)
    logging.info('create db file.')
    return

if __name__ == "__main__":
    init_db()
