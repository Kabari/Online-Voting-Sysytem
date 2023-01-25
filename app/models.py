from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.sql.schema import ForeignKey
from flask_login import UserMixin
from flask_migrate import Migrate
import app
db = SQLAlchemy()
migrate = Migrate(db)

class UserModel(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mat_no = db.Column(db.String(8), nullable=False, unique=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    admin =  db.Column(db.Integer,default=0)
    votes = db.relationship('VotesModel', backref='voter', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.mat_no}')"

class VotesModel(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mat_no = db.Column(db.String(8), nullable=False, unique=True)
    voter_id = db.Column(db.Integer, ForeignKey('users.id'))
    post_1 = db.Column(db.Integer, nullable=False )
    post_2 = db.Column(db.Integer, nullable=False)
    post_3 = db.Column(db.Integer, nullable=False)
    post_4 = db.Column(db.Integer, nullable=False)
    post_5 = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Voter('{self.mat_no}')"

class CandidateModel(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mat_no = db.Column(db.String(8), nullable=False, unique=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))
    batch = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    post = db.Column(db.String(80), nullable=False)
    pic_path = db.Column(db.String(120))
    agenda =  db.Column(db.String(300), default="No agenda")

    def __repr__(self):
        return f"Candidate('{self.first_name}','{self.batch}','{self.course}','{self.department}')"

