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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u6jmhcginr6i8b:p3948f89c31131fcd385685950ec70da09a8ce8808ee78358104b256e2b3f741b@clhtb6lu92mj2.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/dag2e7pq2p5su2'
    # app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    # for clarification and test: here the secret key is hardcoded
    app.config['SECRET_KEY'] = 'ourcoolcsproject24'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    
    db.init_app(app)

    return app

app = create_app()