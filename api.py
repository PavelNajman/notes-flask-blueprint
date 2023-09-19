from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import NoteModel
from .schemas import NoteSchema

blp = Blueprint("Notes", "notes", description="Operations on notes.")

@blp.route("/note/<int:note_id>")
class Note(MethodView):
    @jwt_required()
    @blp.response(200, NoteSchema)
    def get(self, note_id):
        note_owner = get_jwt_identity()
        note = NoteModel.find_by_id(note_id, note_owner)
        if note:
            return note
        abort(404, message="Note not found.")

    @jwt_required(fresh=True)
    @blp.arguments(NoteSchema)
    @blp.response(200, NoteSchema)
    def put(self, note_data, note_id):
        note_owner = get_jwt_identity()
        note = NoteModel.find_by_id(note_id, note_owner)
        if not note:
            abort(404, message="Note not found.")
        note.title = note_data["title"]
        note.body = note_data["body"]
        try:
            note.insert_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occured while updating the note.")
        return note
        
    @jwt_required(fresh=True)
    @blp.response(200, NoteSchema)
    def delete(self, note_id):
        note_owner = get_jwt_identity()
        note = NoteModel.find_by_id(note_id, note_owner)
        if note:
            note.delete_from_db()
            return note
        abort(404, message="Note not found.")

@blp.route("/note")
class NoteList(MethodView):
    @jwt_required()
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        return NoteModel.find_by_owner(get_jwt_identity())

    @jwt_required(fresh=True)
    @blp.arguments(NoteSchema)
    @blp.response(201, NoteSchema)
    def post(self, note_data):
        note_data["owner"] = get_jwt_identity()
        note = NoteModel(**note_data)
        try:
            note.insert_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating the note.")
        return note
