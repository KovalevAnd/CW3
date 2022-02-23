from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.users_service import UsersService
from project.setup_db import db
from flask import request
from project.dao.models.user import User
from project.views.decorators import auth_required

users_ns = Namespace("user")


@users_ns.route("/")
class UsersView(Resource):
    @users_ns.response(200, "OK")
    @auth_required
    def get(self):
        """Get all users"""
        return UsersService(db.session).get_all_users()


@users_ns.route("/<int:user_id>")
class UsersView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    @auth_required
    def get(self, user_id: int):
        """Get user by id"""
        try:
            return UsersService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User not found")

    @users_ns.response(204, "OK")
    @users_ns.response(404, "User not found")
    @auth_required
    def patch(self, user_id: int):
        user = db.session.query(User).get(user_id)
        req_json = request.json
        user.name = req_json.get("name")
        user.surname = req_json.get("surname")
        user.favorite_genre = req_json.get("favorite_genre")
        db.session.add(user)
        db.session.commit()
        return "204 OK"


@users_ns.route("/password/<int:user_id>")
class UsersView(Resource):
    @users_ns.response(204, "OK")
    @auth_required
    def put(self,  user_id: int):
        user = db.session.query(User).get(user_id)
        req_json = request.json
        print('USER PASS', user.password)
        print('REQ_JSON', req_json)
        if user.password == User.get_hash(str(req_json["password_1"])):
            user.password = User.get_hash(str(req_json["password_2"]))
        else:
            return "Invalid password"

        db.session.add(user)
        db.session.commit()
        return "204 OK"

