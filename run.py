from project.dao.models.genre import Genre
from project.dao.models.director import Director
from project.server import db#, create_app
from f import create_app

app = create_app()


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
    }
