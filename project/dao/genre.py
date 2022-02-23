from sqlalchemy.orm.scoping import scoped_session
from project.dao.models.genre import Genre
from flask import request
from project.config import BaseConfig


class GenreDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Genre).filter(Genre.id == pk).one_or_none()

    def get_all(self):
        page = request.args.get('page', default=None, type=int)
        if page is not None:
            return self._db_session.query(Genre).paginate(page, BaseConfig.ITEMS_PER_PAGE, False).items
        else:
            return self._db_session.query(Genre).all()
