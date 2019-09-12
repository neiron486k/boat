from .models import User
from feature.orm import db
import bcrypt


class UserService(object):
    def create(self, data: dict, flush: bool = True) -> User:
        data.pop('confirm')
        user = User(**data)
        passwordHash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password = passwordHash
        db.session.add(user)
        if flush:
            db.session.commit()
        return user
