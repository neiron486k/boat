from feature.orm import db
from flask_login import UserMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
                       )


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def has_role(self, role: str):
        return bool(len([r for r in self.roles if r.name == role]))

    def __repr__(self):
        return '<User %r>' % self.email

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
        }


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return '<Role %s>' % self.name

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
