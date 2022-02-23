from project.dao.models.genre import Genre
from project.dao.models.director import Director
from project.dao.models.user import User
from project.server import db
from f import create_app

app = create_app()


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "User": User,

    }
