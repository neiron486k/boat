from feature.orm import db


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.Text(), unique=False, nullable=True)

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Article %r>' % self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
        }
