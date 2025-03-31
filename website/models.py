from . import db



# created database models

class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),nullable=False,unique=True)
    email = db.Column(db.String(150),unique=True,nullable= False)
    password = db.Column(db.String(150))
    manga = db.relationship('Manga')
    titles_library = db.Column(db.String(150))
    
class Manga(db.Model):
    title=db.Column(db.String(150),primary_key=True)
    author=db.Column(db.String(150))
    summary=db.Column(db.String(150))
    chapters_number=db.relationship('Chapters')
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))


class Chapters(db.Model):
    title = db.Column(db.String(150),primary_key = True)
    chapter_number = db.Column(db.String(150))
    manga_title=db.Column(db.String(150),db.ForeignKey('manga.title'))


