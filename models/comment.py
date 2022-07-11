from datetime import datetime

from models.settings import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    post = db.relationship("Post")

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # database relationship
    author = db.relationship("User")  # orm relationship

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    @classmethod
    def create(self, comment, post, author):
        newComment = self(comment=comment, post=post, author=author)
        db.add(newComment)
        db.commit()
        return newComment

    @classmethod
    def deleted(self):
        self.deleted_at = datetime.utcnow()
        db.add(self)
        db.commit()
        return None
