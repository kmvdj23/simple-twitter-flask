from app.controllers import app
from app.models.model import db, Account, Tweet

def init_db():
    db.app = app
    db.drop_all()
    db.create_all()



if __name__ == '__main__':
    init_db()
