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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u6n3ohfjmrl1e3:pd140fdef8081ecf86007e1e131b8175252f355578b48e8c3c336810b352630a6@c9tiftt16dc3eo.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d2hqvl8rdvqoj7'
    app.config['SECRET_KEY'] = 'ourcoolcsproject24'
    
    db.init_app(app)

    return app

app = create_app()