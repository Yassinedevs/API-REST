from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
import sentry_sdk

sentry_sdk.init(
    dsn="https://6d007338709ed8a6f7b31e9034810ec7@o4506740100300800.ingest.sentry.io/4506740103643136",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)

# Définir la variable BASE_URL ici
BASE_URL = 'http://127.0.0.1:5000'  # Remplacez cela par votre domaine réel

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/swapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "une-cle-efficace"
app.config['BASE_URL'] = BASE_URL
db.init_app(app)
