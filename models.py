from .. import db

class NoteModel(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(1024), unique = False, nullable = False)
    body = db.Column(db.String(8192), unique = False, nullable = True)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
