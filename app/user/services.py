from .models import User, Role
from feature.orm import db
import bcrypt


class UserService(object):
    def create(self, user: User, flush: bool = True) -> User:
        passwordHash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password = passwordHash
        role = Role.query.filter_by(name='user').first() or Role(name='user')
        user.roles.append(role)
        db.session.add(user)

        if flush:
            db.session.commit()
        return user
