import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find_artist(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def find_album(album):
    """
    Находит в базе альбом с таким же названием
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.album == album).all()
    return albums


def save(album):
    """
    Функция сохраняет введенные данные об альбоме в базе данных
    """
    session = connect_db()
    save_album = Album(year=album["year"], artist=album["artist"], genre=album["genre"], album=album["album"])
    new_album = album["album"]
    session.add(save_album)
    session.commit()
    return f"Данные об альбоме {new_album} успешно сохранены"
