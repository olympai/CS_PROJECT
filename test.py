from db_config import db
from db_config.db_tables import FlatMate, Preferences, Offer
from factory import app

def alter():
    app.app_context().push()
    for i in [503]:
        Offer.query.filter_by(user_id=i).delete()
    db.session.commit()
    return 'DONE'