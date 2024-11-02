# this is the factory file
# it initializes the python flask app

# our convention: first add external dependencies ...
from flask import Flask

# ... than internal dependencies
from db_config import db

# creates our flask app
def create_app():
    app = Flask(__name__)  
    # connect to the database
    app.config['SQLALCHEMY_DATABASE_URI'] = '__database_uri__'
    app.config['SECRET_KEY'] = 'ourcoolcsproject24'
    
    db.init_app(app)

    return app

app = create_app()