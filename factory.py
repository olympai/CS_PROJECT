# this is the factory file
# it initializes the python flask app

# our convention: first add external dependencies ...
from flask import Flask

# ... than internal dependencies
from db_config import db
from utils.utils import correct_uri

# creates our flask app
def create_app():
    app = Flask(__name__)  
    # connect to the database
    # app.config['SQLALCHEMY_DATABASE_URI'] = correct_uri(os.environ.get('DATABASE_URL'))
    # for clarification and test: here the database URI is hardcoded
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u21fm5hco9rlre:p1708e307e0693a7c7b14f621f7250c7a6099a87641a1560cbb8daaa091333094@c9tiftt16dc3eo.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d84um7ga402mvs'
    # app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    # for clarification and test: here the secret key is hardcoded
    app.config['SECRET_KEY'] = 'ourcoolcsproject24'
    
    db.init_app(app)

    return app

app = create_app()