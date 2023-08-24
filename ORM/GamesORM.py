from importlib import resources

from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ORM.session import get_session

Base = declarative_base()
url = 'postgresql://test:test@localhost/testdb'

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player1 = Column(String)
    player2 = Column(String)
    level = Column(Integer)
    points = Column(Integer)
    tag = Column(String)

    def insert(self, player1, player2, level, points, tag):
        """Добавляет игру в games"""
        session = get_session()
        new_game = Game(player1=player1, player2=player2, level=level, points=points, tag=tag)
        session.add(new_game)
        session.commit()

    def select(self, game_id):
        """Конкретный селект - одна строка"""
        session = get_session()
        game = session.query(Game).get(game_id)
        return game

    def select_all(self):
        """Селект всех строк"""
        session = get_session()
        games = session.query(Game).all()
        return games

    def select_tags(self):
        """Селект тегов с дистинктом"""
        session = get_session()
        tags = session.query(Game.tag).distinct().all()
        return tags

    def select_max_points(self, tag):
        """Селект максимума очков по выбранному тегу"""
        session = get_session()
        points = session.query(func.max(Game.points)).filter(Game.tag == tag).all()
        points = points[0][0]
        return points

    def select_max_level(self, tag):
        """Селект максимального уровня по выбранному тегу"""
        session = get_session()
        level = session.query(func.max(Game.level)).filter(Game.tag == tag).all()
        level = level[0][0]
        return level

    def select_new_players(self):
        """Собираем всех уникальных игроков для добавления новых в players"""
        session = get_session()
        p1 = session.query(Game.player1).distinct().all()
        p2 = session.query(Game.player2).distinct().all()
        _players = []
        for p in p1:
            _players.append(p)
        for p in p2:
            _players.append(p)
        return _players

    def update(self, player1=None, player2=None, level=None, points=None, tag=None):
        """Апдейт строки"""
        session = get_session()
        if player1:
            self.player1 = player1
        if player2:
            self.player2 = player2
        if level:
            self.level = level
        if points:
            self.points = points
        if tag:
            self.tag = tag

        session.commit()

    def delete(self):
        session = get_session()
        session.delete(self)
        session.commit()

    def insert_game(self):
        """Основной метод для добавления игры в games"""
        p1 = input("Player #1: ")
        p2 = input("Player #2: ")
        players = [p1, p2]
        players.sort()
        score = int(input("Score: "))
        level = int(input("Level: "))
        tag = players[0][:5] + players[1][:5]
        self.insert(p1, p2, level, score, tag)


