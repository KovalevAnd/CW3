from sqlalchemy.orm.scoping import scoped_session
from project.dao.models.movie import Movie
from flask import request
from project.config import BaseConfig


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        page = request.args.get('page', default=None, type=int)
        status = request.args.get('status', default=None, type=str)
        if status == 'new' and page is not None:
            return self._db_session.query(Movie).order_by(Movie.year.desc()).paginate(page, BaseConfig.ITEMS_PER_PAGE, False).items
        if page is not None:
            return self._db_session.query(Movie).paginate(page, BaseConfig.ITEMS_PER_PAGE, False).items
        if status == 'new':
            return self._db_session.query(Movie).order_by(Movie.year.desc())
        else:
            return self._db_session.query(Movie).all()
