from flask import Flask
from flask_compress import Compress
from flask_migrate import Migrate
from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os

app = Flask(__name__)
if 'DYNO' in os.environ:
    sslify = SSLify(app)

app.config['COMPRESS_ALGORITHM'] = 'gzip'
Compress(app)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['RECAPTCHA_PUBLIC_KEY'] = os.environ['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = os.environ['RECAPTCHA_PRIVATE_KEY']

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)

from sainakoukpari import routes