from app import app
from app.models import db
from waitress import serve

from settings import DEV

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
    if DEV:
        app.run(port=6572, debug=True)
    else:
        serve(app, host="0.0.0.0", port=6572)
