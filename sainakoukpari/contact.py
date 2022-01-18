from sqlalchemy import create_engine
import os

db = create_engine(os.environ['DATABASE_ADDRESS'])

with db.connect() as conn:
	conn.execute('TRUNCATE TABLE contact RESTART IDENTITY')