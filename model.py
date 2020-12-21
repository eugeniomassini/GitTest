from app import db


class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing
    username = db.Column(db.String(50), unique=True, nullable=False)
    nam = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return "<User %r>" % self.name


class Role (db.Model):
    id = db.Column(db.Integer,primary_key=True)  # Auto-incrementing
    name = db.Column(db.String(20),nullable=False)
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name