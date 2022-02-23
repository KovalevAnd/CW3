from sqlalchemy.orm.scoping import scoped_session
from project.dao.models.director import Director
from flask import request
from project.config import BaseConfig


class DirectorDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Director).filter(Director.id == pk).one_or_none()

    def get_all(self):
        page = request.args.get('page', default=None, type=int)
        if page is not None:
            return self._db_session.query(Director).paginate(page, BaseConfig.ITEMS_PER_PAGE, False).items
        else:
            return self._db_session.query(Director).all()
