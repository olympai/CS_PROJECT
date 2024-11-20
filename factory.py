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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uf83oikjpd68ug:p34f86f490652371e7274e08eb8f22f323ae84077f405a392738ea23cdbdf6c58@c3opaibi71ph4s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d2rua5utalol1h'
    app.config['SECRET_KEY'] = 'ourcoolcsproject24'
    
    db.init_app(app)

    return app

app = create_app()