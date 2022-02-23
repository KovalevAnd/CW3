from flask_restx import abort, Namespace, Resource


from project.setup_db import db
from flask import request
from project.dao.models.user import User
from project.config import BaseConfig
import jwt
import datetime
import calendar

auth_ns = Namespace("auth")


@auth_ns.route('/register')
class AuthView(Resource):

    def post(self):
        req_json = request.json
        ent = User(**req_json)
        ent.password = User.get_hash(req_json.get("password"))
        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"/users/{ent.id}"}


@auth_ns.route('/login')
class AuthView(Resource):

    def post(self):
        req_json = request.json
        ent = User(**req_json)
        ent.password = User.get_hash(req_json.get("password"))
        with db.session.begin():
            user = db.session.query(User).filter(User.email == ent.email, User.password ==
                                                 ent.password).scalar()
        if user is not None:
            data = {
                'email': user.email,
                'password': user.password
            }
            result_token = {
                'access_token': self.generate_access_token(data, BaseConfig.SECRET_KEY, BaseConfig.ALGO),
                'refresh_token': self.generate_refresh_token(data, BaseConfig.SECRET_KEY, BaseConfig.ALGO)
            }
            return result_token, 201
        else:
            return abort(401)

    def generate_access_token(self, data, secret, algo):
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        return jwt.encode(data, secret, algorithm=algo)

    def generate_refresh_token(self, data, secret, algo):
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        return jwt.encode(data, secret, algorithm=algo)

    def put(self):
        req_json = request.json
        if self.check_token(req_json['refresh_token'], BaseConfig.SECRET_KEY, BaseConfig.ALGO):
            pld = jwt.decode(req_json['refresh_token'], BaseConfig.SECRET_KEY, BaseConfig.ALGO)
            data = {
                'email': pld['email'],
                'password': pld['password']
            }
            result_token = {
                'access_token': self.generate_access_token(data, BaseConfig.SECRET_KEY, BaseConfig.ALGO),
                'refresh_token': self.generate_refresh_token(data, BaseConfig.SECRET_KEY, BaseConfig.ALGO)
            }
            return result_token, 201
        else:
            return abort(401)

    def check_token(self, token, secret, algo):
        try:
            jwt.decode(token, secret, algorithms=algo)
            return True
        except Exception as e:
            return False
